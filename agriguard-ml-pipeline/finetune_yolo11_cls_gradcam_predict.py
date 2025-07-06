import argparse
import torch
import torch.nn.functional as F
from torchvision import transforms
from ultralytics import YOLO
#from torchcam.methods import GradCAM
from torchcam.methods import GradCAMpp
from torchcam.utils import overlay_mask
from PIL import Image
import json
from pathlib import Path


def find_last_conv_layer(model: torch.nn.Module) -> str:
    """Trouve le dernier layer Conv2d dans un modèle PyTorch."""
    conv_layers = []

    def recurse(module, prefix=''):
        for name, child in module.named_children():
            full_name = f"{prefix}.{name}" if prefix else name
            if isinstance(child, torch.nn.Conv2d):
                conv_layers.append((full_name, child))
            recurse(child, full_name)

    recurse(model)

    if not conv_layers:
        raise ValueError("Aucun layer Conv2d trouvé dans le modèle.")
    
    return conv_layers[-1][0]


def load_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    img = Image.open(image_path).convert("RGB")
    return transform(img).unsqueeze(0), img


def apply_gradcam(model, image_tensor, class_idx, original_image, save_path="gradcam_result.jpg"):
    from torchcam.methods import GradCAM
    from torchvision import transforms
    from torchcam.utils import overlay_mask
    import torch.nn.functional as F

    image_tensor = image_tensor.clone().detach().requires_grad_(True)

    # Trouver le dernier layer conv
    target_layer = find_last_conv_layer(model.model)

    # Initialiser Grad-CAM
    cam_extractor = GradCAMpp(model.model, target_layer=target_layer)

    device = next(model.model.parameters()).device
    image_tensor = image_tensor.to(device)

    with torch.set_grad_enabled(True):
        logits = model.model(image_tensor)

        # CORRECTION ici :
        if isinstance(logits, tuple):  # YOLO peut renvoyer un tuple
            logits = logits[0]

    # Calcul des probabilités
    probs = F.softmax(logits, dim=1)[0]

    # Appliquer Grad-CAM
    # Appliquer Grad-CAM
    cam = cam_extractor(class_idx, probs.unsqueeze(0))

    # cam[0] est un tensor 2D ou 3D adapté
    cam_tensor = cam[0]
    cam_tensor = cam_tensor - cam_tensor.min()
    cam_tensor = cam_tensor / (cam_tensor.max() + 1e-8)
    cam_image = transforms.ToPILImage()(cam_tensor.cpu())



    # Superposer sur l’image originale
    overlayed = overlay_mask(original_image, cam_image, alpha=0.95)
    overlayed.save(save_path)

    cam_image.save("gradcam_results/heatmap_alone.jpg")

    return save_path



def predict(model_path, image_path, output_cam_path="gradcam_result.jpg"):
    # Chargement du modèle
    model = YOLO(model_path)
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.model.to(device)

    # Chargement et prétraitement de l'image
    image_tensor, original_image = load_image(image_path)
    image_tensor = image_tensor.to(device)

    # Prédiction via l'API ultralytics pour obtenir les noms de classes
    result = model.predict(image_path, imgsz=224, device=device.index if device.type == 'cuda' else 'cpu')[0]
    class_idx = int(result.probs.top1)
    class_name = result.names[class_idx]
    confidence = float(result.probs.top1conf)

    # Appliquer Grad-CAM avec passage direct dans model.model
    cam_img_path = apply_gradcam(model, image_tensor, class_idx, original_image, save_path=output_cam_path)

    # Structure finale à retourner
    output = {
        "image_path": image_path,
        "predicted_class_index": class_idx,
        "predicted_class_name": class_name,
        "confidence": round(confidence, 4),
        "all_class_probabilities": {
            result.names[i]: round(float(score), 4)
            for i, score in enumerate(result.probs.data.tolist())
        },
        "gradcam_path": cam_img_path
    }

    return output


def main():
    parser = argparse.ArgumentParser(description="Classification avec YOLOv11s-CLS et Grad-CAM")
    parser.add_argument("--model", type=str, default="yolo_classification/finetune_experiment/weights/best.pt", help="Chemin vers le modèle YOLO")
    parser.add_argument("--image", type=str, required=True, help="Chemin vers l'image à prédire")
    parser.add_argument("--cam_output", type=str, default="gradcam_results/gradcam_result.jpg", help="Fichier de sortie pour la heatmap")

    args = parser.parse_args()

    result = predict(args.model, args.image, args.cam_output)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
