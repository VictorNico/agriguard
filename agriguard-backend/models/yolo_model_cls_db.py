# models/yolo_model_cls.py (Version mise à jour)
import torch
from ultralytics import YOLO
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import os

# Import du gestionnaire de base de données
from .database_manager import DatabaseManager

class MaizeDiseaseClassifier:
    """Classificateur de maladies du maïs avec support MongoDB/JSON"""

    def __init__(self, model_path: str, json_fallback_path: str = None,
                 mongodb_url: str = "mongodb://localhost:27017/",
                 database_name: str = "agriguard_db"):
        """
        Initialiser le classificateur

        Args:
            model_path: Chemin vers le modèle YOLO
            json_fallback_path: Chemin vers le fichier JSON de fallback
            mongodb_url: URL MongoDB
            database_name: Nom de la base de données
        """
        self.model_path = model_path
        self.model = None
        self.class_names = []

        # Initialiser le gestionnaire de base de données
        self.db_manager = DatabaseManager(
            mongodb_url=mongodb_url,
            database_name=database_name,
            json_fallback_path=json_fallback_path or "data/diseases_database.json"
        )

        # Charger le modèle YOLO
        self._load_model()

    def _load_model(self):
        """Charger le modèle YOLO"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Modèle non trouvé: {self.model_path}")

            self.model = YOLO(self.model_path)

            # Récupérer les noms de classes depuis le modèle
            if hasattr(self.model, 'names'):
                self.class_names = list(self.model.names.values())
            else:
                # Fallback: utiliser les classes de la base de données
                self.class_names = self.db_manager.get_all_diseases()

            print(f"✅ Modèle chargé: {len(self.class_names)} classes")

        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
            self.model = None
            self.class_names = []

    def classify(self, image_array: np.ndarray) -> Dict[str, Any]:
        """
        Classifier une image

        Args:
            image_array: Image sous forme de array numpy

        Returns:
            Dict contenant les résultats de classification
        """
        if self.model is None:
            return {
                "success": False,
                "error": "Modèle non chargé",
                "timestamp": datetime.now().isoformat()
            }

        try:
            # Prédiction avec YOLO
            results = self.model(image_array, verbose=False)

            if not results or len(results) == 0:
                return {
                    "success": False,
                    "error": "Aucune prédiction obtenue",
                    "timestamp": datetime.now().isoformat()
                }

            result = results[0]

            # Extraire les probabilités
            if hasattr(result, 'probs') and result.probs is not None:
                probs = result.probs.data.cpu().numpy()

                # Classe prédite
                predicted_class_id = int(np.argmax(probs))
                confidence = float(probs[predicted_class_id])

                # Vérifier que l'ID est valide
                if predicted_class_id >= len(self.class_names):
                    return {
                        "success": False,
                        "error": f"ID de classe invalide: {predicted_class_id}",
                        "timestamp": datetime.now().isoformat()
                    }

                predicted_class = self.class_names[predicted_class_id]

                # Top 5 prédictions
                top5_indices = np.argsort(probs)[-5:][::-1]
                top5_predictions = [
                    {
                        "class": self.class_names[i] if i < len(self.class_names) else f"unknown_{i}",
                        "class_id": int(i),
                        "confidence": float(f"{float(str(probs[i])):.2f}"),
                        "confidence_percentage": float(f"{float(str(probs[i] * 100)):.2f}")
                    }
                    for i in top5_indices
                ]

                # Obtenir les informations détaillées sur la maladie
                disease_info = self.db_manager.get_disease_info(predicted_class)

                return {
                    "success": True,
                    "timestamp": datetime.now().isoformat(),
                    "classification": {
                        "predicted_class": predicted_class,
                        "class_id": predicted_class_id,
                        "confidence": float(f"{float(str(confidence)):.2f}"),
                        "confidence_percentage": float(f"{float(str(confidence*100)):.2f}"),
                        "top5_predictions": top5_predictions
                    },
                    "disease_info": disease_info
                }

            else:
                return {
                    "success": False,
                    "error": "Pas de probabilités dans les résultats",
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la classification: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def classify_batch(self, images: List[np.ndarray]) -> List[Dict[str, Any]]:
        """
        Classifier plusieurs images

        Args:
            images: Liste d'images sous forme de arrays numpy

        Returns:
            Liste des résultats de classification
        """
        results = []

        for i, image in enumerate(images):
            try:
                result = self.classify(image)
                results.append(result)
            except Exception as e:
                results.append({
                    "success": False,
                    "error": f"Erreur image {i}: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                })

        return results

    def get_disease_info(self, disease_class: str) -> Optional[Dict[str, Any]]:
        """
        Obtenir les informations détaillées d'une maladie

        Args:
            disease_class: Classe de la maladie

        Returns:
            Informations sur la maladie ou None
        """
        return self.db_manager.get_disease_info(disease_class)

    def get_treatment_recommendations(self, disease_class: str, urgency_filter: str = None) -> List[Dict[str, Any]]:
        """
        Obtenir les recommandations de traitement

        Args:
            disease_class: Classe de la maladie
            urgency_filter: Filtre par urgence (optionnel)

        Returns:
            Liste des recommandations de traitement
        """
        return self.db_manager.get_treatment_recommendations(disease_class, urgency_filter)

    def get_vector_info(self, disease_class: str) -> List[Dict[str, Any]]:
        """
        Obtenir les informations sur les vecteurs

        Args:
            disease_class: Classe de la maladie

        Returns:
            Liste des vecteurs
        """
        return self.db_manager.get_vector_info(disease_class)

    def get_model_info(self) -> Dict[str, Any]:
        """
        Obtenir les informations du modèle

        Returns:
            Informations sur le modèle et la base de données
        """
        return self.db_manager.get_model_info()

    def get_diseases_database(self) -> Dict[str, Any]:
        """
        Obtenir la base de données complète des maladies

        Returns:
            Base de données des maladies
        """
        return self.db_manager.get_diseases_database()

    def __del__(self):
        """Destructor pour fermer la connexion à la base de données"""
        if hasattr(self, 'db_manager'):
            self.db_manager.close()