import os
import cv2
import random
from tqdm import tqdm
from collections import defaultdict
import albumentations as A
import matplotlib.pyplot as plt
from albumentations.augmentations.transforms import *

# Configuration
DATASET_DIR = "dataset"
TARGET_SIZE = (256, 256)
EXTENSIONS = (".jpg", ".jpeg", ".png")
AUG_PREFIX = "aug"
SHOW_SAMPLES = 5  # nombre de comparaisons à afficher après génération

# Pipeline d’augmentation
transform = A.Compose([
     A.RandomBrightnessContrast(p=0.5),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.2),
    A.RandomRotate90(p=0.5),
    A.Rotate(limit=30, p=0.8),
    A.HueSaturationValue(p=0.4),
    A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
    A.Blur(blur_limit=3, p=0.2),
    A.GaussianBlur(blur_limit=3, p=0.2),  # Alternative à Blur, à garder si tu veux mixer
    A.MotionBlur(p=0.2),
    A.ElasticTransform(p=0.1),
    A.RandomResizedCrop(height=224, width=224, scale=(0.8, 1.0), p=0.4),
    A.Resize(224, 224) 
])

def collect_images(dataset_dir):
    class_counts = defaultdict(int)
    image_paths = defaultdict(list)

    for class_name in os.listdir(dataset_dir):
        class_dir = os.path.join(dataset_dir, class_name)
        if not os.path.isdir(class_dir):
            continue
        for fname in os.listdir(class_dir):
            if fname.lower().endswith(EXTENSIONS):
                path = os.path.join(class_dir, fname)
                image_paths[class_name].append(path)
                class_counts[class_name] += 1

    return class_counts, image_paths

def balance_dataset(dataset_dir, transform):
    class_counts, image_paths = collect_images(dataset_dir)
    max_count = max(class_counts.values())

    print("\n📊 Répartition initiale :")
    for c, count in class_counts.items():
        print(f"- {c}: {count} images")
    print(f"\n🎯 Cible : {max_count} images par classe")

    samples_for_visual = []

    for class_name, count in class_counts.items():
        if count >= max_count:
            print(f"✅ Classe '{class_name}' déjà équilibrée.")
            continue

        needed = max_count - count
        print(f"\n➕ Génération de {needed} images pour '{class_name}'...")

        src_images = image_paths[class_name]
        class_dir = os.path.join(dataset_dir, class_name)
        idx = 0

        pbar = tqdm(total=needed)
        while idx < needed:
            img_path = random.choice(src_images)
            img = cv2.imread(img_path)
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Appliquer l’augmentation
            augmented = transform(image=img)["image"]

            if idx < SHOW_SAMPLES:
                samples_for_visual.append((img, augmented))

            # Sauvegarde
            save_path = os.path.join(class_dir, f"{AUG_PREFIX}_{idx+1:05d}.jpg")
            cv2.imwrite(save_path, cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR))
            idx += 1
            pbar.update(1)

        pbar.close()

    return samples_for_visual

# def show_samples(samples):
#     print("\n Affichage de quelques exemples avant/après augmentation...")
#     plt.figure(figsize=(12, len(samples) * 3))
#     for i, (original, augmented) in enumerate(samples):
#         plt.subplot(len(samples), 2, 2*i + 1)
#         plt.imshow(original)
#         plt.title("Image originale")
#         plt.axis("off")

#         plt.subplot(len(samples), 2, 2*i + 2)
#         plt.imshow(augmented)
#         plt.title("Image augmentée")
#         plt.axis("off")
#     plt.tight_layout()
#     plt.show()

def main():
    samples = balance_dataset(DATASET_DIR, transform)
    #show_samples(samples)

if __name__ == "__main__":
    main()