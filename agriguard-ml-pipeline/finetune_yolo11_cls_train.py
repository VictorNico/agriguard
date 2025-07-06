import os
from ultralytics import YOLO
import torch

# Configuration
MODEL_PATH = "yolov11s-cls.pt"  # Chemin vers votre modèle pré-entraîné
DATA_PATH = "path/to/your/dataset"  # Chemin vers votre dataset
EPOCHS = 100
BATCH_SIZE = 16
IMG_SIZE = 224
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def prepare_dataset_structure():
    """
    Votre dataset doit avoir cette structure :
    dataset/
    ├── train/
    │   ├── class1/
    │   │   ├── image1.jpg
    │   │   └── image2.jpg
    │   └── class2/
    │       ├── image3.jpg
    │       └── image4.jpg
    └── val/
        ├── class1/
        │   ├── image5.jpg
        │   └── image6.jpg
        └── class2/
            ├── image7.jpg
            └── image8.jpg
    """
    print("Structure du dataset attendue :")
    print("dataset/")
    print("├── train/")
    print("│   ├── class1/")
    print("│   └── class2/")
    print("└── val/")
    print("    ├── class1/")
    print("    └── class2/")

def fine_tune_yolo():
    """Fine-tuning du modèle YOLOv11s-cls"""
    
    # Vérifier si le modèle existe
    if not os.path.exists(MODEL_PATH):
        print(f"Erreur: Le modèle {MODEL_PATH} n'existe pas.")
        print("Téléchargez le modèle avec: yolo download yolov11s-cls.pt")
        return
    
    # Vérifier si le dataset existe
    if not os.path.exists(DATA_PATH):
        print(f"Erreur: Le dataset {DATA_PATH} n'existe pas.")
        prepare_dataset_structure()
        return
    
    print(f"Utilisation du device: {DEVICE}")
    print(f"Modèle: {MODEL_PATH}")
    print(f"Dataset: {DATA_PATH}")
    
    # Charger le modèle pré-entraîné
    model = YOLO(MODEL_PATH)
    
    # Lancer le fine-tuning
    results = model.train(
        data=DATA_PATH,
        epochs=EPOCHS,
        batch=BATCH_SIZE,
        imgsz=IMG_SIZE,
        device=DEVICE,
        project="yolo_classification",
        name="finetune_experiment",
        save=True,
        verbose=True,
        patience=10,  # Early stopping
        lr0=0.01,  # Learning rate initial
        warmup_epochs=3,
        augment=True,
        mixup=0.1,
        copy_paste=0.1
    )
    
    print("Fine-tuning terminé !")
    print(f"Meilleur modèle sauvegardé dans: {results.save_dir}")
    
    return results

def validate_model(model_path):
    """Valider le modèle fine-tuné"""
    model = YOLO(model_path)
    
    # Validation sur le dataset de validation
    results = model.val(data=DATA_PATH, split='val')
    
    print(f"Précision top-1: {results.top1:.3f}")
    print(f"Précision top-5: {results.top5:.3f}")
    
    return results

def predict_single_image(model_path, image_path):
    """Prédiction sur une image unique"""
    model = YOLO(model_path)
    
    # Prédiction
    results = model(image_path)
    
    # Afficher les résultats
    for result in results:
        probs = result.probs
        print(f"Classe prédite: {result.names[probs.top1]}")
        print(f"Confiance: {probs.top1conf:.3f}")
        print(f"Top 5 classes: {probs.top5}")
    
    return results

def main():
    """Fonction principale"""
    print("=== Fine-tuning YOLOv11s-cls ===")
    
    # Lancer le fine-tuning
    results = fine_tune_yolo()
    
    if results:
        # Chemin vers le meilleur modèle
        best_model = os.path.join(results.save_dir, "weights", "best.pt")
        
        # Validation du modèle
        #print("\n=== Validation du modèle ===")
        #validate_model(best_model)
        
        # Exemple de prédiction (remplacez par le chemin de votre image)
        predict_single_image(best_model, "/home/fordjou/agriguard/agriguard-ml/ml_pipeline/test_dataset/MLN/3224.JPEG")

if __name__ == "__main__":
    # Paramètres à ajuster selon vos besoins
    MODEL_PATH = "yolov11s-cls.pt"
    DATA_PATH = "dataset_split"  # Remplacez par votre chemin
    EPOCHS = 50  # Ajustez selon vos besoins
    BATCH_SIZE = 16  # Ajustez selon votre GPU
    
    main()