import os
import shutil
import random

def extract_files_balanced(source_dir, dest_dir, num_files, exclude_folders):
    os.makedirs(dest_dir, exist_ok=True)

    # Récupère les sous-dossiers valides
    subfolders = [f.path for f in os.scandir(source_dir) if f.is_dir() and f.name not in exclude_folders]
    file_pool = {sub: [f for f in os.listdir(sub) if os.path.isfile(os.path.join(sub, f))] for sub in subfolders}

    copied_files = 0
    used_names = set()

    while copied_files < num_files:
        progress = False  # Pour détecter s’il reste des fichiers à extraire

        for subfolder in subfolders:
            if copied_files >= num_files:
                break

            if file_pool[subfolder]:
                file = random.choice(file_pool[subfolder])
                file_pool[subfolder].remove(file)

                src = os.path.join(subfolder, file)
                dst = os.path.join(dest_dir, file)

                # Gérer les doublons
                base, ext = os.path.splitext(file)
                i = 1
                while dst in used_names or os.path.exists(dst):
                    dst = os.path.join(dest_dir, f"{base}_{i}{ext}")
                    i += 1

                try:
                    shutil.copy(src, dst)
                    used_names.add(dst)
                    copied_files += 1
                    progress = True
                    print(f'✅ {copied_files}: {src} → {dst}')
                except Exception as e:
                    print(f'❌ Erreur: {e}')

        if not progress:
            print("⚠️ Plus assez de fichiers à extraire dans les sous-dossiers.")
            break

    print(f'\n✅ Total : {copied_files} fichiers copiés dans "{dest_dir}".')

def main():
    source_directory = 'Plant_leaf_diseases_dataset_without_augmentation/Plant_leave_diseases_dataset_without_augmentation'
    destination_directory = 'detection/autre'
    nombre_de_fichiers = 18805
    exclude_folders = [
        'Corn_Cercospora_leaf_spot Gray_leaf_spot',
        'Corn_Common_rust',
        'Corn_healthy',
        'Corn_Northern_Leaf_Blight'
    ]

    extract_files_balanced(source_directory, destination_directory, nombre_de_fichiers, exclude_folders)

if __name__ == "__main__":
    main()