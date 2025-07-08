import os
import shutil

def flatten_and_copy(source_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    used_names = set()

    count = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            src_path = os.path.join(root, file)
            base, ext = os.path.splitext(file)

            # Crée un nom unique pour éviter les conflits
            new_name = file
            i = 1
            while new_name in used_names or os.path.exists(os.path.join(dest_dir, new_name)):
                new_name = f"{base}_{i}{ext}"
                i += 1

            used_names.add(new_name)
            dest_path = os.path.join(dest_dir, new_name)

            try:
                shutil.copy2(src_path, dest_path)
                count += 1
                print(f"✅ {src_path} → {dest_path}")
            except Exception as e:
                print(f"❌ Erreur lors de la copie de {src_path} : {e}")

    print(f"\n✅ {count} fichiers copiés dans : {dest_dir}")

def main():
    # 🔧 À modifier selon ton besoin
    source_directory = "dataset/maize_disease"  # Chemin vers le dossier source
    # destination_directory = "dataset_splited"  # Chemin vers le dossier de
    destination_directory = "detection/maize_leave"

    flatten_and_copy(source_directory, destination_directory)

if __name__ == "__main__":
    main()
