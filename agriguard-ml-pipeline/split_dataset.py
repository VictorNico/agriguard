import os
import random
import shutil
from pathlib import Path
from tqdm import tqdm

# === Configuration ===
INPUT_DIR = "dataset/maize_disease"              # dossier d'origine avec les classes
OUTPUT_DIR = "dataset_split"       # dossier de sortie
SPLIT_RATIOS = {
    "train": 0.7,
    "val": 0.2,
    "test": 0.1
}
SEED = 42

def split_dataset(input_dir, output_dir, ratios):
    random.seed(SEED)

    classes = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

    for split in ["train", "val", "test"]:
        for class_name in classes:
            os.makedirs(os.path.join(output_dir, split, class_name), exist_ok=True)

    print(f"📂 Classes détectées : {classes}\n")

    for class_name in classes:
        class_dir = os.path.join(input_dir, class_name)
        images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(images)

        total = len(images)
        train_end = int(total * ratios["train"])
        val_end = train_end + int(total * ratios["val"])

        splits = {
            "train": images[:train_end],
            "val": images[train_end:val_end],
            "test": images[val_end:]
        }

        print(f"🔹 Classe '{class_name}' : {total} images → train={len(splits['train'])}, val={len(splits['val'])}, test={len(splits['test'])}")

        for split, split_images in splits.items():
            for img_name in tqdm(split_images, desc=f"{split}/{class_name}"):
                src_path = os.path.join(class_dir, img_name)
                dst_path = os.path.join(output_dir, split, class_name, img_name)
                shutil.copy2(src_path, dst_path)

    print("\n✅ Dataset divisé avec succès dans :", output_dir)

if __name__ == "__main__":
    split_dataset(INPUT_DIR, OUTPUT_DIR, SPLIT_RATIOS)