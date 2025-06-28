import cv2
import numpy as np
from PIL import Image
import os

def process_image(image_path, target_size=(640, 640)):
    """
    Traite l'image pour la détection YOLO

    Args:
        image_path (str): Chemin vers l'image
        target_size (tuple): Taille cible (largeur, hauteur)

    Returns:
        numpy.ndarray: Image traitée
    """
    try:
        # Charger l'image avec OpenCV
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Impossible de charger l'image: {image_path}")

        # Convertir BGR vers RGB (OpenCV charge en BGR par défaut)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Redimensionner tout en gardant le ratio d'aspect
        image = resize_with_padding(image, target_size)

        # Normalisation et amélioration optionnelle
        image = enhance_image(image)

        return image

    except Exception as e:
        print(f"Erreur traitement image: {e}")
        return None

def resize_with_padding(image, target_size):
    """
    Redimensionne l'image en gardant le ratio d'aspect et ajoute du padding

    Args:
        image (numpy.ndarray): Image source
        target_size (tuple): Taille cible (largeur, hauteur)

    Returns:
        numpy.ndarray: Image redimensionnée avec padding
    """
    h, w = image.shape[:2]
    target_w, target_h = target_size

    # Calculer le ratio de redimensionnement
    ratio = min(target_w / w, target_h / h)

    # Nouvelles dimensions
    new_w = int(w * ratio)
    new_h = int(h * ratio)

    # Redimensionner
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Créer une image avec padding
    padded = np.full((target_h, target_w, 3), 114, dtype=np.uint8)  # Couleur grise

    # Centrer l'image redimensionnée
    y_offset = (target_h - new_h) // 2
    x_offset = (target_w - new_w) // 2

    padded[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized

    return padded

def enhance_image(image):
    """
    Améliore la qualité de l'image pour une meilleure détection

    Args:
        image (numpy.ndarray): Image source

    Returns:
        numpy.ndarray: Image améliorée
    """
    # Conversion en LAB pour améliorer le contraste
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    # Égalisation d'histogramme adaptatif sur le canal L
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    # Recombiner les canaux
    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)

    # Réduction du bruit (optionnel)
    # enhanced = cv2.bilateralFilter(enhanced, 9, 75, 75)

    return enhanced

def validate_image(image_path):
    """
    Valide si l'image est correcte pour le traitement

    Args:
        image_path (str): Chemin vers l'image

    Returns:
        dict: Résultat de validation
    """
    result = {
        "valid": False,
        "errors": [],
        "info": {}
    }

    try:
        # Vérifier si le fichier existe
        if not os.path.exists(image_path):
            result["errors"].append("Fichier introuvable")
            return result

        # Charger avec PIL pour validation
        with Image.open(image_path) as img:
            # Informations de base
            result["info"] = {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "file_size": os.path.getsize(image_path)
            }

            # Validations
            if result["info"]["file_size"] > 10 * 1024 * 1024:  # 10MB max
                result["errors"].append("Fichier trop volumineux (>10MB)")

            if img.size[0] < 100 or img.size[1] < 100:
                result["errors"].append("Image trop petite (<100x100)")

            if img.mode not in ['RGB', 'RGBA', 'L']:
                result["errors"].append(f"Mode couleur non supporté: {img.mode}")

            # Si pas d'erreurs, image valide
            if not result["errors"]:
                result["valid"] = True

    except Exception as e:
        result["errors"].append(f"Erreur lecture image: {str(e)}")

    return result

def create_thumbnail(image_path, thumb_size=(200, 200)):
    """
    Crée une miniature de l'image

    Args:
        image_path (str): Chemin vers l'image source
        thumb_size (tuple): Taille de la miniature

    Returns:
        PIL.Image: Image miniature ou None
    """
    try:
        with Image.open(image_path) as img:
            # Convertir en RGB si nécessaire
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Créer miniature en gardant le ratio
            img.thumbnail(thumb_size, Image.Resampling.LANCZOS)

            return img

    except Exception as e:
        print(f"Erreur création miniature: {e}")
        return None

def extract_image_features(image):
    """
    Extrait des caractéristiques de l'image pour l'analyse

    Args:
        image (numpy.ndarray): Image source

    Returns:
        dict: Caractéristiques extraites
    """
    features = {}

    try:
        # Statistiques de base
        features["brightness"] = np.mean(image)
        features["contrast"] = np.std(image)

        # Histogramme des couleurs
        hist_r = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([image], [1], None, [256], [0, 256])
        hist_b = cv2.calcHist([image], [2], None, [256], [0, 256])

        features["color_distribution"] = {
            "red_peak": int(np.argmax(hist_r)),
            "green_peak": int(np.argmax(hist_g)),
            "blue_peak": int(np.argmax(hist_b))
        }

        # Détection de flou (variance du Laplacien)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        features["sharpness"] = cv2.Laplacian(gray, cv2.CV_64F).var()

        # Dominance de couleur verte (pour végétation)
        green_dominance = np.mean(image[:, :, 1]) / (np.mean(image) + 1e-6)
        features["vegetation_indicator"] = green_dominance

    except Exception as e:
        print(f"Erreur extraction features: {e}")
        features["error"] = str(e)

    return features

def batch_process_images(image_paths, target_size=(640, 640)):
    """
    Traite plusieurs images en lot

    Args:
        image_paths (list): Liste des chemins d'images
        target_size (tuple): Taille cible

    Returns:
        list: Liste des images traitées
    """
    processed_images = []

    for path in image_paths:
        processed = process_image(path, target_size)
        if processed is not None:
            processed_images.append({
                "path": path,
                "image": processed,
                "features": extract_image_features(processed)
            })
        else:
            print(f"Échec traitement: {path}")

    return processed_images

# Utilitaires pour debug et visualisation
def save_processed_image(image, output_path):
    """
    Sauvegarde une image traitée

    Args:
        image (numpy.ndarray): Image à sauvegarder
        output_path (str): Chemin de sortie
    """
    try:
        # Convertir RGB vers BGR pour OpenCV
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, image_bgr)
        return True
    except Exception as e:
        print(f"Erreur sauvegarde: {e}")
        return False

def draw_detection_boxes(image, detections):
    """
    Dessine les boîtes de détection sur l'image

    Args:
        image (numpy.ndarray): Image source
        detections (list): Liste des détections avec bbox

    Returns:
        numpy.ndarray: Image avec boîtes dessinées
    """
    result_image = image.copy()

    for detection in detections:
        if "bbox" in detection:
            x1, y1, x2, y2 = map(int, detection["bbox"])

            # Couleur selon la confiance
            confidence = detection.get("confidence", 0.5)
            if confidence > 0.7:
                color = (0, 255, 0)  # Vert - haute confiance
            elif confidence > 0.5:
                color = (255, 165, 0)  # Orange - moyenne confiance
            else:
                color = (255, 0, 0)  # Rouge - faible confiance

            # Dessiner la boîte
            cv2.rectangle(result_image, (x1, y1), (x2, y2), color, 2)

            # Ajouter le label
            label = f"{detection.get('class', 'Unknown')}: {confidence:.2f}"
            cv2.putText(result_image, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return result_image