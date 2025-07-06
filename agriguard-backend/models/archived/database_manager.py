# database_manager.py
from pymongo import MongoClient
from typing import Optional, Dict, List, Any
import json
import os
from datetime import datetime

class DatabaseManager:
    """Gestionnaire de base de données qui peut utiliser MongoDB ou fallback sur JSON"""

    def __init__(self, mongodb_url: str = "mongodb://localhost:27017/",
                 database_name: str = "agriguard_db",
                 json_fallback_path: str = "data/diseases_database.json"):
        self.mongodb_url = mongodb_url
        self.database_name = database_name
        self.json_fallback_path = json_fallback_path
        self.client = None
        self.db = None
        self.use_mongodb = False

        # Essayer de se connecter à MongoDB
        self._init_mongodb()

        # Si MongoDB non disponible, charger JSON
        if not self.use_mongodb:
            self._load_json_fallback()

    def _init_mongodb(self):
        """Initialiser la connexion MongoDB"""
        try:
            self.client = MongoClient(self.mongodb_url, serverSelectionTimeoutMS=5000)
            # Test de connexion
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            self.use_mongodb = True
            print("✅ MongoDB connecté avec succès")
        except Exception as e:
            print(f"⚠️  MongoDB non disponible: {e}")
            print("   Utilisation du fallback JSON")
            self.use_mongodb = False

    def _load_json_fallback(self):
        """Charger les données depuis le fichier JSON"""
        try:
            with open(self.json_fallback_path, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)
            print("✅ Données JSON chargées avec succès")
        except Exception as e:
            print(f"❌ Erreur lors du chargement JSON: {e}")
            self.json_data = {"diseases": {}, "classes": {}, "legacy_pests": {}}

    def get_disease_info(self, disease_class: str) -> Optional[Dict[str, Any]]:
        """Obtenir les informations d'une maladie"""
        if self.use_mongodb:
            return self._get_disease_from_mongodb(disease_class)
        else:
            return self._get_disease_from_json(disease_class)

    def _get_disease_from_mongodb(self, disease_class: str) -> Optional[Dict[str, Any]]:
        """Récupérer une maladie depuis MongoDB"""
        try:
            disease = self.db.diseases.find_one({
                "disease_id": disease_class,
                "is_active": True
            })

            if disease:
                return self._format_disease_for_api(disease)
            return None
        except Exception as e:
            print(f"Erreur MongoDB: {e}")
            return None

    def _get_disease_from_json(self, disease_class: str) -> Optional[Dict[str, Any]]:
        """Récupérer une maladie depuis JSON"""
        # Chercher dans diseases
        if disease_class in self.json_data.get("diseases", {}):
            disease_data = self.json_data["diseases"][disease_class]
            return self._format_json_disease_for_api(disease_class, disease_data, "disease")

        # Chercher dans classes (comme "saine")
        if disease_class in self.json_data.get("classes", {}):
            class_data = self.json_data["classes"][disease_class]
            return self._format_json_disease_for_api(disease_class, class_data, "healthy_state")

        # Chercher dans legacy_pests
        if disease_class in self.json_data.get("legacy_pests", {}):
            pest_data = self.json_data["legacy_pests"][disease_class]
            return self._format_json_disease_for_api(disease_class, pest_data, "pest")

        return None

    def _format_disease_for_api(self, disease: Dict[str, Any]) -> Dict[str, Any]:
        """Formater une maladie MongoDB pour l'API"""
        return {
            "name": disease["name"]["fr"],
            "scientific_name": disease["name"].get("scientific", ""),
            "description": disease["description"]["fr"],
            "category": "disease" if disease["type"] != "etat_sain" else "healthy_state",
            "urgency": disease["urgency"],
            "symptoms": disease["symptoms"]["fr"],
            "crops": disease["crops_affected"],
            "pathogens": disease.get("pathogens", []),
            "vectors": disease.get("vectors", []),
            "prevention_measures": disease.get("prevention_measures", []),
            "impact": disease.get("impact", {}).get("description", ""),
            "geographic_distribution": disease.get("geographic_distribution", ""),
            "treatment_options": disease.get("treatment_options", []),
            "recommendations": disease.get("prevention_measures", [])
        }

    def _format_json_disease_for_api(self, disease_class: str, disease_data: Dict[str, Any], category: str) -> Dict[str, Any]:
        """Formater une maladie JSON pour l'API"""
        return {
            "name": disease_data.get("name", ""),
            "scientific_name": disease_data.get("scientific_name", ""),
            "description": disease_data.get("description", ""),
            "category": category,
            "urgency": disease_data.get("urgency", "medium"),
            "symptoms": disease_data.get("symptoms", []),
            "crops": disease_data.get("crops", []),
            "pathogens": disease_data.get("pathogens", []),
            "vectors": disease_data.get("vectors", []),
            "prevention_measures": disease_data.get("prevention", []),
            "impact": disease_data.get("impact", ""),
            "geographic_distribution": disease_data.get("geographic_distribution", ""),
            "treatment_options": disease_data.get("treatment", []),
            "recommendations": disease_data.get("recommendations", [])
        }

    def get_treatment_recommendations(self, disease_class: str, urgency_filter: str = None) -> List[Dict[str, Any]]:
        """Obtenir les recommandations de traitement"""
        if self.use_mongodb:
            return self._get_treatments_from_mongodb(disease_class, urgency_filter)
        else:
            return self._get_treatments_from_json(disease_class, urgency_filter)

    def _get_treatments_from_mongodb(self, disease_class: str, urgency_filter: str = None) -> List[Dict[str, Any]]:
        """Récupérer les traitements depuis MongoDB"""
        try:
            disease = self.db.diseases.find_one({
                "disease_id": disease_class,
                "is_active": True
            })

            if disease and "treatment_options" in disease:
                treatments = disease["treatment_options"]

                # Filtrer par urgence si spécifié
                if urgency_filter:
                    treatments = [t for t in treatments if t.get("priority") == urgency_filter]

                return treatments

            return []
        except Exception as e:
            print(f"Erreur MongoDB: {e}")
            return []

    def _get_treatments_from_json(self, disease_class: str, urgency_filter: str = None) -> List[Dict[str, Any]]:
        """Récupérer les traitements depuis JSON"""
        disease_info = self._get_disease_from_json(disease_class)
        if disease_info:
            treatments = disease_info.get("treatment_options", [])

            # Filtrer par urgence si spécifié
            if urgency_filter:
                treatments = [t for t in treatments if t.get("priority") == urgency_filter]

            return treatments

        return []

    def get_vector_info(self, disease_class: str) -> List[Dict[str, Any]]:
        """Obtenir les informations sur les vecteurs"""
        if self.use_mongodb:
            return self._get_vectors_from_mongodb(disease_class)
        else:
            return self._get_vectors_from_json(disease_class)

    def _get_vectors_from_mongodb(self, disease_class: str) -> List[Dict[str, Any]]:
        """Récupérer les vecteurs depuis MongoDB"""
        try:
            disease = self.db.diseases.find_one({
                "disease_id": disease_class,
                "is_active": True
            })

            if disease:
                return disease.get("vectors", [])

            return []
        except Exception as e:
            print(f"Erreur MongoDB: {e}")
            return []

    def _get_vectors_from_json(self, disease_class: str) -> List[Dict[str, Any]]:
        """Récupérer les vecteurs depuis JSON"""
        disease_info = self._get_disease_from_json(disease_class)
        if disease_info:
            return disease_info.get("vectors", [])

        return []

    def get_all_diseases(self) -> List[str]:
        """Obtenir la liste de toutes les maladies"""
        if self.use_mongodb:
            return self._get_all_diseases_from_mongodb()
        else:
            return self._get_all_diseases_from_json()

    def _get_all_diseases_from_mongodb(self) -> List[str]:
        """Récupérer toutes les maladies depuis MongoDB"""
        try:
            diseases = self.db.diseases.find(
                {"is_active": True},
                {"disease_id": 1}
            )
            return [d["disease_id"] for d in diseases]
        except Exception as e:
            print(f"Erreur MongoDB: {e}")
            return []

    def _get_all_diseases_from_json(self) -> List[str]:
        """Récupérer toutes les maladies depuis JSON"""
        all_diseases = []
        all_diseases.extend(self.json_data.get("diseases", {}).keys())
        all_diseases.extend(self.json_data.get("classes", {}).keys())
        all_diseases.extend(self.json_data.get("legacy_pests", {}).keys())
        return all_diseases

    def get_diseases_database(self) -> Dict[str, Any]:
        """Obtenir la base de données complète"""
        if self.use_mongodb:
            return self._get_database_from_mongodb()
        else:
            return self._get_database_from_json()

    def _get_database_from_mongodb(self) -> Dict[str, Any]:
        """Récupérer la base complète depuis MongoDB"""
        try:
            diseases = list(self.db.diseases.find({"is_active": True}))

            # Formater pour l'API
            formatted_diseases = {}
            for disease in diseases:
                formatted_diseases[disease["disease_id"]] = self._format_disease_for_api(disease)

            return {
                "diseases": formatted_diseases,
                "source": "mongodb",
                "total": len(formatted_diseases)
            }
        except Exception as e:
            print(f"Erreur MongoDB: {e}")
            return {"diseases": {}, "source": "mongodb_error", "total": 0}

    def _get_database_from_json(self) -> Dict[str, Any]:
        """Récupérer la base complète depuis JSON"""
        return {
            "diseases": self.json_data,
            "source": "json",
            "total": len(self.json_data.get("diseases", {})) +
                    len(self.json_data.get("classes", {})) +
                    len(self.json_data.get("legacy_pests", {}))
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Obtenir les informations du modèle"""
        all_diseases = self.get_all_diseases()

        return {
            "model_loaded": True,
            "classes_supported": all_diseases,
            "diseases_in_db": len(all_diseases),
            "database_source": "mongodb" if self.use_mongodb else "json",
            "metadata": self._get_metadata()
        }

    def _get_metadata(self) -> Dict[str, Any]:
        """Obtenir les métadonnées"""
        if self.use_mongodb:
            try:
                # Récupérer quelques métadonnées depuis MongoDB
                sample_disease = self.db.diseases.find_one({"is_active": True})
                if sample_disease and "metadata" in sample_disease:
                    return sample_disease["metadata"]
            except:
                pass

        # Fallback vers JSON ou métadonnées par défaut
        return self.json_data.get("metadata", {
            "version": "1.0",
            "data_source": "json_fallback",
            "last_updated": datetime.now().isoformat()
        })

    def close(self):
        """Fermer la connexion MongoDB"""
        if self.client:
            self.client.close()
            print("🔌 Connexion MongoDB fermée")