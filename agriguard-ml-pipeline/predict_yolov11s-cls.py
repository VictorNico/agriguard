import argparse
import json
from pathlib import Path
from ultralytics import YOLO
from PIL import Image
import torch


def load_model(model_path: str):
    """Charge le modèle YOLOv11s-cls entraîné."""
    model = YOLO(model_path)
    return model


def predict_image(model, image_path: str, conf_threshold: float = 0.5):
    """Effectue la prédiction sur une image et retourne un dictionnaire structuré."""
    
    if not Path(image_path).exists():
        raise FileNotFoundError(f"L'image {image_path} n'existe pas.")

    results = model.predict(source=image_path, imgsz=224, device='cuda' if torch.cuda.is_available() else 'cpu')
    result = results[0]
    probs = result.probs

    top1_index = int(probs.top1)
    top1_conf = float(probs.top1conf)

    # Si la confiance est trop faible
    if top1_conf < conf_threshold:
        response = {
            "image_path": image_path,
            "predicted_class_index": None,
            "predicted_class_name": None,
            "confidence": top1_conf,
            "message": f"Aucune classe prédite avec une confiance suffisante (< {conf_threshold})",
            "all_class_probabilities": {
                result.names[i]: round(float(score), 4)
                for i, score in enumerate(probs.data.tolist())
            }
        }
    else:
        # Prédiction normale
        response = {
            "image_path": image_path,
            "predicted_class_index": top1_index,
            "predicted_class_name": result.names[top1_index],
            "confidence": round(top1_conf, 4),
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
    parser.add_argument("--conf-thres", type=float, default=0.5, help="Seuil de confiance minimal (default=0.5)")

    args = parser.parse_args()

    model = load_model(args.model)
    result = predict_image(model, args.image, conf_threshold=args.conf_thres)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()