import os

# === CONFIGURATION ===
ROOT_DIR = "Plant_leaf_diseases_dataset_without_augmentation/Plant_leave_diseases_dataset_without_augmentation"  # Chemin vers le dossier contenant les sous-dossiers
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png')  # Extensions à renommer
START_INDEX = 1  # Index de départ pour la numérotation

def rename_files_in_subfolders(root_dir):
    for class_name in os.listdir(root_dir):
        subfolder_path = os.path.join(root_dir, class_name)
        
        if not os.path.isdir(subfolder_path):
            continue  # Ignore les fichiers éventuels au niveau racine

        print(f"📁 Traitement du dossier : {class_name}")
        files = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f)) and f.lower().endswith(VALID_EXTENSIONS)]
        
        for idx, filename in enumerate(sorted(files), start=START_INDEX):
            old_path = os.path.join(subfolder_path, filename)
            ext = os.path.splitext(filename)[1].lower()
            new_name = f"{class_name}_{idx:04d}{ext}"
            new_path = os.path.join(subfolder_path, new_name)
            
            os.rename(old_path, new_path)
            print(f"  🔄 {filename} → {new_name}")

    print("\n✅ Tous les fichiers ont été renommés.")

if __name__ == "__main__":
    rename_files_in_subfolders(ROOT_DIR)
