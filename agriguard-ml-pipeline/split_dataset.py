import os
import random
import shutil
import csv
from tqdm import tqdm

# === Configuration ===
INPUT_DIR = "dataset"  # Dossier contenant les sous-dossiers de classes
OUTPUT_DIR = "dataset_split"         # Dossier de sortie
LOG_CSV_PATH = os.path.join(OUTPUT_DIR, "renaming_log.csv")
STATS_PATH = os.path.join(OUTPUT_DIR, "split_stats.txt")
SPLIT_RATIOS = {
    "train": 0.7,
    "val": 0.15,
    "test": 0.15
}
SEED = 42  # Pour reproductibilité

def split_dataset(input_dir, output_dir, ratios):
    random.seed(SEED)
    os.makedirs(output_dir, exist_ok=True)

    # Préparation du fichier CSV
    csv_file = open(LOG_CSV_PATH, mode='w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["ancien_nom", "nouveau_nom", "classe", "split"])

    stats = {}  # Pour stocker les statistiques

    # Détection des classes
    classes = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
    print(f"📂 Classes détectées : {classes}\n")

    # Création de la structure de sortie
    for split in ["train", "val", "test"]:
        for class_name in classes:
            os.makedirs(os.path.join(output_dir, split, class_name), exist_ok=True)

    # Traitement de chaque classe
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
            stats.setdefault(split, {})
            stats[split][class_name] = len(split_images)

            for idx, img_name in enumerate(tqdm(split_images, desc=f"{split}/{class_name}")):
                src_path = os.path.join(class_dir, img_name)
                ext = os.path.splitext(img_name)[1].lower()
                new_name = f"{class_name}_{idx:04d}{ext}"
                dst_path = os.path.join(output_dir, split, class_name, new_name)
                shutil.copy2(src_path, dst_path)

                # Écrire dans le CSV
                csv_writer.writerow([img_name, new_name, class_name, split])

    csv_file.close()
    print(f"\n✅ CSV de renommage enregistré ici : {LOG_CSV_PATH}")

    # Écrire les statistiques
    with open(STATS_PATH, 'w', encoding='utf-8') as stats_file:
        total_images = 0
        for split in ["train", "val", "test"]:
            stats_file.write(f"\n🔸 Split : {split}\n")
            for class_name, count in stats.get(split, {}).items():
                stats_file.write(f"  - {class_name}: {count} images\n")
                total_images += count
        stats_file.write(f"\n📊 Total d'images traitées : {total_images} images\n")

    print(f"📈 Statistiques enregistrées dans : {STATS_PATH}")
    print("\n✅ Dataset divisé, renommé et journalisé avec succès.")

if __name__ == "__main__":
    split_dataset(INPUT_DIR, OUTPUT_DIR, SPLIT_RATIOS)
