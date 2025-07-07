import argparse
import json
from pathlib import Path
from ultralytics import YOLO
from PIL import Image
import torch


def load_model(model_path: str):
    """
    Charge le modèle YOLOv11s-cls entraîné.
    """
    model = YOLO(model_path)
    return model


def predict_image(model, image_path: str):
    """
    Effectue la prédiction sur une image et retourne un dictionnaire structuré.
    """
    # Vérification de l'existence du fichier
    if not Path(image_path).exists():
        raise FileNotFoundError(f"L'image {image_path} n'existe pas.")

    # Prédiction
    results = model.predict(source=image_path, imgsz=224, device='cuda' if torch.cuda.is_available() else 'cpu')

    # Résultat de classification
    result = results[0]
    probs = result.probs  # Probabilités pour chaque classe

    # Structure de la réponse
    response = {
        "image_path": image_path,
        "predicted_class_index": int(probs.top1),
        "predicted_class_name": result.names[probs.top1],
        "confidence": round(float(probs.top1conf), 4),
        "all_class_probabilities": {
            result.names[i]: round(float(score), 4)
            for i, score in enumerate(probs.data.tolist())
        }
    }

    return response


def main():
    parser = argparse.ArgumentParser(description="Prédiction d'image avec YOLOv11s-CLS")
    parser.add_argument("--model", type=str, default="yolo_classification/finetune_experiment/weights/best.pt", help="Chemin vers le modèle YOLO entraîné")
    parser.add_argument("--image", type=str, required=True, help="Chemin vers l'image à classer")

    args = parser.parse_args()

    model = load_model(args.model)
    result = predict_image(model, args.image)

    # Affichage en format JSON lisible
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()