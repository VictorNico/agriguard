from ultralytics import YOLO
import cv2
import numpy as np
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Union
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MaizeDiseaseClassifier:
    def __init__(self, model_path='weights/best.pt', disease_db_path='data/diseases_database.json'):
        """
        Classificateur de maladies du maïs basé sur YOLO

        Args:
            model_path: Chemin vers le modèle YOLO
            disease_db_path: Chemin vers la base de données des maladies
        """
        self.model_path = model_path
        self.disease_db_path = disease_db_path
        self.model = None
        self.model_loaded = False
        self.disease_db = {}

        # Mapping des classes (à adapter selon votre modèle)
        self.class_mapping = {
            0: "saine",
            1: "MLN",
            2: "MSV"
        }

        self.load_model()
        self.load_disease_database()

    def load_model(self):
        """Charge le modèle YOLO"""
        try:
            model_full_path = os.path.join(os.getcwd(), self.model_path)
            self.model = YOLO(model_full_path)
            self.model_loaded = True
            logger.info("✅ Modèle YOLO Classification chargé avec succès")
        except Exception as e:
            logger.error(f"❌ Erreur chargement modèle: {e}")
            self.model_loaded = False

    def load_disease_database(self):
        """Charge la base de données des maladies depuis le JSON"""
        try:
            with open(os.path.join(os.getcwd(),self.disease_db_path), 'r', encoding='utf-8') as f:
                self.disease_db = json.load(f)
            logger.info("✅ Base de données des maladies chargée avec succès")
        except FileNotFoundError:
            logger.error(f"❌ Fichier de base de données non trouvé: {self.disease_db_path}")
            self.disease_db = {}
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erreur parsing JSON: {e}")
            self.disease_db = {}

    def classify(self, image: Union[str, np.ndarray]) -> Dict:
        """
        Classifie une image pour détecter la maladie du maïs

        Args:
            image: Image à classifier (numpy array, chemin fichier, ou PIL Image)

        Returns:
            dict: Informations complètes sur la classification et recommandations
        """
        if not self.model_loaded:
            return {
                "success": False,
                "error": "Modèle non chargé",
                "timestamp": datetime.now().isoformat()
            }

        try:
            # Lancer la classification
            results = self.model(image)

            if not results:
                return {
                    "success": False,
                    "error": "Aucun résultat de classification",
                    "timestamp": datetime.now().isoformat()
                }

            result = results[0]
            probs = result.probs

            if probs is None:
                return {
                    "success": False,
                    "error": "Aucune probabilité calculée",
                    "timestamp": datetime.now().isoformat()
                }

            # Classe avec la plus haute probabilité
            top_class_id = int(probs.top1)
            top_confidence = float(probs.top1conf)

            predicted_class = self.class_mapping.get(top_class_id, result.names.get(top_class_id,f"unknown_class_{top_class_id}"))

            # Top 5 des prédictions si disponible
            top5_predictions = []
            if hasattr(probs, 'top5') and probs.top5 is not None:
                top5_indices = probs.top5
                top5_confidences = probs.top5conf

                for i, (class_idx, conf) in enumerate(zip(top5_indices, top5_confidences)):
                    class_idx = int(class_idx)
                    conf = float(conf)
                    class_name = self.class_mapping.get(class_idx, f"unknown_class_{class_idx}")

                    top5_predictions.append({
                        "rank": i + 1,
                        "class": class_name,
                        "class_id": class_idx,
                        "confidence": round(conf, 4)
                    })

            # Construire la réponse complète
            response = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "classification": {
                    "predicted_class": predicted_class,
                    "class_id": top_class_id,
                    "confidence": round(top_confidence, 4),
                    "confidence_percentage": round(top_confidence * 100, 2),
                    "top5_predictions": top5_predictions
                }
            }

            # Ajouter les informations détaillées sur la maladie/état
            disease_info = self.get_disease_info(predicted_class)
            if disease_info:
                response["disease_info"] = disease_info

            return response

        except Exception as e:
            logger.error(f"Erreur classification: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def classify_batch(self, images: List[Union[str, np.ndarray]]) -> List[Dict]:
        """
        Classifie plusieurs images en une fois

        Args:
            images: Liste d'images à classifier

        Returns:
            list: Liste des résultats de classification
        """
        if not self.model_loaded:
            error_response = {
                "success": False,
                "error": "Modèle non chargé",
                "timestamp": datetime.now().isoformat()
            }
            return [error_response] * len(images)

        batch_results = []

        try:
            results = self.model(images)

            for i, result in enumerate(results):
                try:
                    probs = result.probs
#                     print(result.names)
                    if probs is not None:
                        top_class_id = int(probs.top1)
                        top_confidence = float(probs.top1conf)
                        predicted_class = self.class_mapping.get(top_class_id, f"unknown_class_{top_class_id}")

                        response = {
                            "success": True,
                            "timestamp": datetime.now().isoformat(),
                            "image_index": i,
                            "classification": {
                                "predicted_class": predicted_class,
                                "class_id": top_class_id,
                                "confidence": round(top_confidence, 4),
                                "confidence_percentage": round(top_confidence * 100, 2)
                            }
                        }

                        # Ajouter les informations sur la maladie
                        disease_info = self.get_disease_info(predicted_class)
                        if disease_info:
                            response["disease_info"] = disease_info

                        batch_results.append(response)
                    else:
                        batch_results.append({
                            "success": False,
                            "error": "Aucune probabilité calculée",
                            "image_index": i,
                            "timestamp": datetime.now().isoformat()
                        })

                except Exception as e:
                    batch_results.append({
                        "success": False,
                        "error": str(e),
                        "image_index": i,
                        "timestamp": datetime.now().isoformat()
                    })

        except Exception as e:
            logger.error(f"Erreur classification batch: {e}")
            error_response = {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            return [error_response] * len(images)

        return batch_results

    def get_disease_info(self, disease_class: str) -> Optional[Dict]:
        """
        Retourne des informations détaillées sur la maladie/état détecté

        Args:
            disease_class: Classe de la maladie

        Returns:
            dict: Informations complètes sur la maladie
        """
        if not self.disease_db:
            return None

        # Chercher dans les maladies
        if disease_class in self.disease_db.get("diseases", {}):
            disease_data = self.disease_db["diseases"][disease_class].copy()
            return self._format_disease_response(disease_data, "disease")

        # Chercher dans les classes (état sain)
        elif disease_class in self.disease_db.get("classes", {}):
            class_data = self.disease_db["classes"][disease_class].copy()
            return self._format_disease_response(class_data, "healthy_state")

        return None

    def _format_disease_response(self, data: Dict, category: str) -> Dict:
        """
        Formate la réponse avec les informations de la maladie

        Args:
            data: Données de la maladie/classe
            category: Catégorie (disease ou healthy_state)

        Returns:
            dict: Réponse formatée
        """
        formatted_response = {
            "category": category,
            "name": data.get("name", ""),
            "scientific_name": data.get("scientific_name", ""),
            "description": data.get("description", ""),
            "urgency": data.get("urgency", "unknown"),
            "symptoms": data.get("symptoms", []),
            "crops": data.get("crops", []),
            "impact": data.get("impact", ""),
            "geographic_distribution": data.get("geographic_distribution", "")
        }

        # Ajouter les informations spécifiques aux maladies
        if category == "disease":
            formatted_response.update({
                "pathogens": data.get("pathogens", []),
                "vectors": data.get("vectors", []),
                "treatment_options": data.get("treatment", []),
                "prevention_measures": data.get("prevention", [])
            })
        elif category == "healthy_state":
            formatted_response.update({
                "recommendations": data.get("recommendations", [])
            })

        return formatted_response

    def get_treatment_recommendations(self, disease_class: str, urgency_filter: str = None) -> List[Dict]:
        """
        Retourne les recommandations de traitement pour une maladie

        Args:
            disease_class: Classe de la maladie
            urgency_filter: Filtrer par priorité (critical, high, medium, low)

        Returns:
            list: Liste des traitements recommandés
        """
        disease_info = self.get_disease_info(disease_class)

        if not disease_info or "treatment_options" not in disease_info:
            return []

        treatments = disease_info["treatment_options"]

        if urgency_filter:
            treatments = [t for t in treatments if t.get("priority") == urgency_filter]

        return sorted(treatments, key=lambda x: {
            "critical": 0, "high": 1, "medium": 2, "low": 3
        }.get(x.get("priority", "low"), 3))

    def get_vector_info(self, disease_class: str) -> List[Dict]:
        """
        Retourne les informations sur les vecteurs d'une maladie

        Args:
            disease_class: Classe de la maladie

        Returns:
            list: Liste des vecteurs
        """
        disease_info = self.get_disease_info(disease_class)

        if not disease_info or "vectors" not in disease_info:
            return []

        return disease_info["vectors"]

    def get_model_info(self) -> Dict:
        """
        Retourne les informations sur le modèle et la base de données

        Returns:
            dict: Informations système
        """
        return {
            "model_loaded": self.model_loaded,
            "model_path": self.model_path,
            "database_path": self.disease_db_path,
            "classes_supported": list(self.class_mapping.values()),
            "diseases_in_db": list(self.disease_db.get("diseases", {}).keys()),
            "metadata": self.disease_db.get("metadata", {})
        }

# Exemple d'utilisation
if __name__ == "__main__":
    # Initialiser le classificateur
    classifier = MaizeDiseaseClassifier('weights/best.pt', 'disease_database.json')

    # Vérifier le statut du système
    model_info = classifier.get_model_info()
    print("=== Informations Système ===")
    print(f"Modèle chargé: {model_info['model_loaded']}")
    print(f"Classes supportées: {model_info['classes_supported']}")
    print(f"Maladies en base: {model_info['diseases_in_db']}")

    # Classifier une image (exemple)
    # image_path = "path/to/your/maize_leaf.jpg"
    # result = classifier.classify(image_path)

    # if result["success"]:
    #     print(f"\n=== Résultat Classification ===")
    #     classification = result["classification"]
    #     print(f"Classe prédite: {classification['predicted_class']}")
    #     print(f"Confiance: {classification['confidence_percentage']:.2f}%")
    #
    #     if "disease_info" in result:
    #         disease_info = result["disease_info"]
    #         print(f"\n=== Informations Maladie ===")
    #         print(f"Nom: {disease_info['name']}")
    #         print(f"Urgence: {disease_info['urgency']}")
    #         print(f"Symptômes: {', '.join(disease_info['symptoms'])}")
    #
    #         # Obtenir les recommandations de traitement
    #         treatments = classifier.get_treatment_recommendations(
    #             classification['predicted_class'],
    #             urgency_filter="high"
    #         )
    #
    #         if treatments:
    #             print(f"\n=== Traitements Recommandés (Priorité Élevée) ===")
    #             for treatment in treatments:
    #                 print(f"- {treatment['product']}: {treatment['description']}")
    #                 print(f"  Dosage: {treatment['dosage']}")
    #                 print(f"  Timing: {treatment['timing']}")
    # else:
    #     print(f"Erreur: {result['error']}")