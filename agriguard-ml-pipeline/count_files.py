import os

def count_files(directory):
    total_files = 0
    for root, dirs, files in os.walk(directory):
        total_files += len(files)
    return total_files

# Remplacez 'votre_dossier' par le chemin de votre dossier
dossier = 'Plant_leaf_diseases_dataset_without_augmentation'
nombre_de_fichiers = count_files(dossier)

print(f'Total de fichiers dans le dossier "{dossier}": {nombre_de_fichiers}')