import os
import shutil
import random

def extract_files_balanced(source_dir, dest_dir, num_files, exclude_folders, rename_func=None):
    # Crée le dossier de destination s'il n'existe pas
    os.makedirs(dest_dir, exist_ok=True)

    # Récupère tous les sous-dossiers
    subfolders = [f.path for f in os.scandir(source_dir) if f.is_dir() and f.name not in exclude_folders]
    files_to_copy = []

    # Récupère des fichiers de chaque sous-dossier
    for subfolder in subfolders:
        files = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]
        if files:
            # Ajoute un fichier aléatoire de ce sous-dossier
            files_to_copy.append(random.choice(files))

    # Mélange les fichiers à copier
    random.shuffle(files_to_copy)

    # Limite le nombre de fichiers à copier
    files_to_copy = files_to_copy[:num_files]

    # Copie les fichiers dans le dossier de destination
    for file in files_to_copy:
        source_file = os.path.join(subfolder, file)
        if os.path.exists(source_file):
            try:
                # Génère le nouveau nom de fichier si une fonction de renommage est fournie
                new_file_name = rename_func(file) if rename_func else file
                destination_file = os.path.join(dest_dir, new_file_name)
                
                shutil.copy(source_file, destination_file)
                print(f'Fichier copié : "{source_file}" -> "{destination_file}"')
            except Exception as e:
                print(f'Erreur lors de la copie de "{source_file}": {e}')
        else:
            print(f'Le fichier n\'existe pas : "{source_file}"')

    print(f'{len(files_to_copy)} fichiers ont été copiés dans "{dest_dir}".')

def main():
    source_directory = 'Plant_leaf_diseases_dataset_without_augmentation/Plant_leave_diseases_dataset_without_augmentation'  # Remplacez par votre dossier source
    destination_directory = 'non_maize_plant_village'  # Remplacez par votre dossier de destination
    nombre_de_fichiers = 18840  # Spécifiez le nombre de fichiers à extraire
    exclude_folders = ['Corn___Cercospora_leaf_spot Gray_leaf_spot', 'Corn___Common_rust', 'Corn___healthy', 'Corn___Northern_Leaf_Blight']

    # Exemple de fonction de renommage : ajoute un préfixe
    def rename_file(original_name):
        base, ext = os.path.splitext(original_name)
        return f'prefix_{base}{ext}'

    extract_files_balanced(source_directory, destination_directory, nombre_de_fichiers, exclude_folders, rename_file)

if __name__ == "__main__":
    main()