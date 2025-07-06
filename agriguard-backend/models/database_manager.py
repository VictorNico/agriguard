# database_manager.py
from pymongo import MongoClient
from typing import Optional, Dict, List, Any
import json
import os
from datetime import datetime
from bson import ObjectId


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

    def _format_json_disease_for_api(self, disease_class: str, disease_data: Dict[str, Any], category: str) -> Dict[
        str, Any]:
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


# ===================================================================
# SERVICES SPÉCIALISÉS POUR CONSOMMER LES TABLES
# ===================================================================

class UserService:
    """Service pour gérer les utilisateurs"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Créer un nouvel utilisateur"""
        if not self.use_mongodb:
            raise Exception("MongoDB requis pour cette opération")

        user_doc = {
            "user_id": user_data["user_id"],
            'password_hash': user_data["password_hash"],
            "profile": user_data.get("profile", {}),
            "farmer_info": user_data.get("farmer_info", {}),
            "subscription": user_data.get("subscription", {
                "plan": "free",
                "start_date": datetime.now(),
                "is_active": True
            }),
            "preferences": user_data.get("preferences", {}),
            "stats": {
                "total_predictions": 0,
                "successful_treatments": 0,
                "farms_managed": 0,
                "last_activity": datetime.now()
            },
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_active": True
        }

        result = self.db.users.insert_one(user_doc)
        return str(result.inserted_id)

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer un utilisateur par ID"""
        if not self.use_mongodb:
            return None

        return self.db.users.find_one({"user_id": user_id, "is_active": True})

    def update_user_stats(self, user_id: str, stats_update: Dict[str, Any]) -> bool:
        """Mettre à jour les statistiques d'un utilisateur"""
        if not self.use_mongodb:
            return False

        result = self.db.users.update_one(
            {"user_id": user_id, "is_active": True},
            {
                "$inc": stats_update,
                "$set": {"updated_at": datetime.now()}
            }
        )
        return result.modified_count > 0

    def get_users_by_region(self, country: str, region: str = None) -> List[Dict[str, Any]]:
        """Récupérer les utilisateurs par région"""
        if not self.use_mongodb:
            return []

        query = {"profile.country": country, "is_active": True}
        if region:
            query["profile.region"] = region

        return list(self.db.users.find(query))


class CropService:
    """Service pour gérer les cultures"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def get_all_crops(self) -> List[Dict[str, Any]]:
        """Récupérer toutes les cultures"""
        if not self.use_mongodb:
            return []

        return list(self.db.crops.find({"is_active": True}))

    def get_crop_by_id(self, crop_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer une culture par ID"""
        if not self.use_mongodb:
            return None

        return self.db.crops.find_one({"crop_id": crop_id, "is_active": True})

    def get_crops_by_disease(self, disease_id: str) -> List[Dict[str, Any]]:
        """Récupérer les cultures affectées par une maladie"""
        if not self.use_mongodb:
            return []

        return list(self.db.crops.find({
            "supported_diseases": disease_id,
            "is_active": True
        }))

    def get_seasonal_crops(self, season: str) -> List[Dict[str, Any]]:
        """Récupérer les cultures par saison"""
        if not self.use_mongodb:
            return []

        return list(self.db.crops.find({
            "growing_seasons": season,
            "is_active": True
        }))


class PredictionService:
    """Service pour gérer les prédictions"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def create_prediction(self, prediction_data: Dict[str, Any]) -> str:
        """Créer une nouvelle prédiction"""
        if not self.use_mongodb:
            raise Exception("MongoDB requis pour cette opération")

        prediction_doc = {
            "prediction_id": prediction_data["prediction_id"],
            "user_id": prediction_data["user_id"],
            "farm_id": prediction_data.get("farm_id"),
            "image_info": prediction_data["image_info"],
            "classification": prediction_data["classification"],
            "disease_info": prediction_data["disease_info"],
            "location": prediction_data.get("location", {}),
            "environmental_context": prediction_data.get("environmental_context", {}),
            "user_feedback": {},
            "processing_time": prediction_data.get("processing_time", 0.0),
            "status": "completed",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        result = self.db.predictions.insert_one(prediction_doc)
        return str(result.inserted_id)

    def get_user_predictions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupérer les prédictions d'un utilisateur"""
        if not self.use_mongodb:
            return []

        return list(self.db.predictions.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit))

    def get_prediction_by_id(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer une prédiction par ID"""
        if not self.use_mongodb:
            return None

        return self.db.predictions.find_one({"prediction_id": prediction_id})

    def update_prediction_feedback(self, prediction_id: str, feedback: Dict[str, Any]) -> bool:
        """Mettre à jour le feedback d'une prédiction"""
        if not self.use_mongodb:
            return False

        result = self.db.predictions.update_one(
            {"prediction_id": prediction_id},
            {
                "$set": {
                    "user_feedback": feedback,
                    "updated_at": datetime.now()
                }
            }
        )
        return result.modified_count > 0

    def get_predictions_by_disease(self, disease_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les prédictions par maladie"""
        if not self.use_mongodb:
            return []

        return list(self.db.predictions.find(
            {"disease_info.disease_id": disease_id}
        ).sort("created_at", -1).limit(limit))

    def get_predictions_by_location(self, coordinates: Dict[str, float], radius_km: float = 10) -> List[Dict[str, Any]]:
        """Récupérer les prédictions par localisation"""
        if not self.use_mongodb:
            return []

        # Recherche géospatiale
        return list(self.db.predictions.find({
            "location.coordinates": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [coordinates["longitude"], coordinates["latitude"]]
                    },
                    "$maxDistance": radius_km * 1000  # Convertir en mètres
                }
            }
        }))


class TreatmentService:
    """Service pour gérer les traitements"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def create_treatment(self, treatment_data: Dict[str, Any]) -> str:
        """Créer un nouveau traitement"""
        if not self.use_mongodb:
            raise Exception("MongoDB requis pour cette opération")

        treatment_doc = {
            "treatment_id": treatment_data["treatment_id"],
            "user_id": treatment_data["user_id"],
            "prediction_id": treatment_data["prediction_id"],
            "disease_id": treatment_data["disease_id"],
            "farm_id": treatment_data.get("farm_id"),
            "recommended_treatments": treatment_data["recommended_treatments"],
            "treatment_plan": treatment_data.get("treatment_plan", {}),
            "implementation": {
                "status": "planned",
                "applications_done": 0,
                "results": None,
                "effectiveness_rating": None,
                "side_effects": None,
                "cost_actual": None
            },
            "follow_up": treatment_data.get("follow_up", {}),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_active": True
        }

        result = self.db.treatments.insert_one(treatment_doc)
        return str(result.inserted_id)

    def get_user_treatments(self, user_id: str, status: str = None) -> List[Dict[str, Any]]:
        """Récupérer les traitements d'un utilisateur"""
        if not self.use_mongodb:
            return []

        query = {"user_id": user_id, "is_active": True}
        if status:
            query["implementation.status"] = status

        return list(self.db.treatments.find(query).sort("created_at", -1))

    def update_treatment_progress(self, treatment_id: str, progress_data: Dict[str, Any]) -> bool:
        """Mettre à jour le progrès d'un traitement"""
        if not self.use_mongodb:
            return False

        result = self.db.treatments.update_one(
            {"treatment_id": treatment_id, "is_active": True},
            {
                "$set": {
                    "implementation": progress_data,
                    "updated_at": datetime.now()
                }
            }
        )
        return result.modified_count > 0

    def get_treatment_effectiveness_stats(self, disease_id: str) -> Dict[str, Any]:
        """Récupérer les statistiques d'efficacité des traitements"""
        if not self.use_mongodb:
            return {}

        pipeline = [
            {"$match": {"disease_id": disease_id, "is_active": True}},
            {"$group": {
                "_id": "$implementation.status",
                "count": {"$sum": 1},
                "avg_effectiveness": {"$avg": "$implementation.effectiveness_rating"}
            }}
        ]

        results = list(self.db.treatments.aggregate(pipeline))
        return {result["_id"]: result for result in results}


class FarmService:
    """Service pour gérer les exploitations agricoles"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def create_farm(self, farm_data: Dict[str, Any]) -> str:
        """Créer une nouvelle exploitation"""
        if not self.use_mongodb:
            raise Exception("MongoDB requis pour cette opération")

        farm_doc = {
            "farm_id": farm_data["farm_id"],
            "user_id": farm_data["user_id"],
            "farm_info": farm_data["farm_info"],
            "crops_grown": farm_data.get("crops_grown", []),
            "management_practices": farm_data.get("management_practices", {}),
            "history": {
                "diseases_encountered": [],
                "treatments_applied": [],
                "yield_records": []
            },
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_active": True
        }

        result = self.db.user_farms.insert_one(farm_doc)
        return str(result.inserted_id)

    def get_user_farms(self, user_id: str) -> List[Dict[str, Any]]:
        """Récupérer les exploitations d'un utilisateur"""
        if not self.use_mongodb:
            return []

        return list(self.db.user_farms.find({"user_id": user_id, "is_active": True}))

    def get_farm_by_id(self, farm_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer une exploitation par ID"""
        if not self.use_mongodb:
            return None

        return self.db.user_farms.find_one({"farm_id": farm_id, "is_active": True})

    def add_disease_to_farm_history(self, farm_id: str, disease_id: str) -> bool:
        """Ajouter une maladie à l'historique de l'exploitation"""
        if not self.use_mongodb:
            return False

        result = self.db.user_farms.update_one(
            {"farm_id": farm_id, "is_active": True},
            {
                "$addToSet": {"history.diseases_encountered": disease_id},
                "$set": {"updated_at": datetime.now()}
            }
        )
        return result.modified_count > 0

    def get_farms_by_location(self, coordinates: Dict[str, float], radius_km: float = 50) -> List[Dict[str, Any]]:
        """Récupérer les exploitations par localisation"""
        if not self.use_mongodb:
            return []

        return list(self.db.user_farms.find({
            "farm_info.location.coordinates": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [coordinates["longitude"], coordinates["latitude"]]
                    },
                    "$maxDistance": radius_km * 1000
                }
            },
            "is_active": True
        }))


class FeedbackService:
    """Service pour gérer les retours utilisateurs"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def create_feedback(self, feedback_data: Dict[str, Any]) -> str:
        """Créer un nouveau feedback"""
        if not self.use_mongodb:
            raise Exception("MongoDB requis pour cette opération")

        feedback_doc = {
            "feedback_id": feedback_data["feedback_id"],
            "user_id": feedback_data["user_id"],
            "prediction_id": feedback_data.get("prediction_id"),
            "treatment_id": feedback_data.get("treatment_id"),
            "feedback_type": feedback_data["feedback_type"],
            "rating": feedback_data["rating"],
            "feedback_data": feedback_data.get("feedback_data", {}),
            "comments": feedback_data.get("comments", {}),
            "user_corrections": feedback_data.get("user_corrections", {}),
            "metadata": feedback_data.get("metadata", {}),
            "status": "pending",
            "admin_response": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        result = self.db.feedback.insert_one(feedback_doc)
        return str(result.inserted_id)

    def get_user_feedback(self, user_id: str) -> List[Dict[str, Any]]:
        """Récupérer les feedbacks d'un utilisateur"""
        if not self.use_mongodb:
            return []

        return list(self.db.feedback.find({"user_id": user_id}).sort("created_at", -1))

    def get_feedback_statistics(self) -> Dict[str, Any]:
        """Récupérer les statistiques de feedback"""
        if not self.use_mongodb:
            return {}

        pipeline = [
            {"$group": {
                "_id": "$feedback_type",
                "count": {"$sum": 1},
                "avg_rating": {"$avg": "$rating"}
            }}
        ]

        results = list(self.db.feedback.aggregate(pipeline))
        return {result["_id"]: result for result in results}

class ImageService:
    """Service pour gérer les images"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def create_image(self, image_data: Dict[str, Any]) -> str:
        """Créer un nouvel enregistrement d'image"""
        if not self.use_mongodb:
            raise Exception("MongoDB requis pour cette opération")

        image_doc = {
            "image_id": image_data["image_id"],
            "user_id": image_data["user_id"],
            "original_filename": image_data["original_filename"],
            "file_info": {
                "file_path": image_data["file_path"],
                "file_size": image_data["file_size"],
                "mime_type": image_data["mime_type"],
                "dimensions": image_data.get("dimensions", {}),
                "quality": image_data.get("quality"),
                "camera_info": image_data.get("camera_info")
            },
            "metadata": {
                "capture_date": image_data.get("capture_date"),
                "location": image_data.get("location"),
                "device_info": image_data.get("device_info"),
                "exif_data": image_data.get("exif_data")
            },
            "processing_info": {
                "is_processed": False,
                "preprocessing_applied": [],
                "thumbnail_path": None,
                "compressed_path": None
            },
            "usage": {
                "prediction_count": 0,
                "last_used": None,
                "associated_predictions": []
            },
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_active": True
        }

        result = self.db.images.insert_one(image_doc)
        return str(result.inserted_id)

    def get_image_by_id(self, image_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer une image par ID"""
        if not self.use_mongodb:
            return None

        return self.db.images.find_one({"image_id": image_id, "is_active": True})

    def get_user_images(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupérer les images d'un utilisateur"""
        if not self.use_mongodb:
            return []

        return list(self.db.images.find(
            {"user_id": user_id, "is_active": True}
        ).sort("created_at", -1).limit(limit))

    def update_image_processing(self, image_id: str, processing_info: Dict[str, Any]) -> bool:
        """Mettre à jour les informations de traitement d'une image"""
        if not self.use_mongodb:
            return False

        result = self.db.images.update_one(
            {"image_id": image_id, "is_active": True},
            {
                "$set": {
                    "processing_info": processing_info,
                    "updated_at": datetime.now()
                }
            }
        )
        return result.modified_count > 0

    def increment_usage_stats(self, image_id: str, prediction_id: str) -> bool:
        """Incrémenter les statistiques d'utilisation d'une image"""
        if not self.use_mongodb:
            return False

        result = self.db.images.update_one(
            {"image_id": image_id, "is_active": True},
            {
                "$inc": {"usage.prediction_count": 1},
                "$set": {"usage.last_used": datetime.now()},
                "$addToSet": {"usage.associated_predictions": prediction_id}
            }
        )
        return result.modified_count > 0

    def get_unprocessed_images(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les images non traitées"""
        if not self.use_mongodb:
            return []

        return list(self.db.images.find(
            {"processing_info.is_processed": False, "is_active": True}
        ).limit(limit))

    def delete_image(self, image_id: str) -> bool:
        """Supprimer une image (soft delete)"""
        if not self.use_mongodb:
            return False

        result = self.db.images.update_one(
            {"image_id": image_id},
            {
                "$set": {
                    "is_active": False,
                    "updated_at": datetime.now()
                }
            }
        )
        return result.modified_count > 0


class PredictionHistoryService:
    """Service pour gérer l'historique des prédictions"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def create_prediction_history(self, history_data: Dict[str, Any]) -> str:
        """Créer un nouvel historique de prédictions"""
        if not self.use_mongodb:
            raise Exception("MongoDB requis pour cette opération")

        history_doc = {
            "user_id": history_data["user_id"],
            "farm_id": history_data.get("farm_id"),
            "summary": {
                "total_predictions": history_data["total_predictions"],
                "period": history_data["period"],
                "start_date": history_data["start_date"],
                "end_date": history_data["end_date"]
            },
            "diseases_detected": history_data.get("diseases_detected", []),
            "accuracy_metrics": {
                "user_confirmed_correct": history_data.get("user_confirmed_correct", 0),
                "user_confirmed_incorrect": history_data.get("user_confirmed_incorrect", 0),
                "accuracy_percentage": history_data.get("accuracy_percentage", 0.0),
                "confidence_average": history_data.get("confidence_average", 0.0)
            },
            "seasonal_patterns": history_data.get("seasonal_patterns", []),
            "treatment_effectiveness": history_data.get("treatment_effectiveness", []),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        result = self.db.prediction_history.insert_one(history_doc)
        return str(result.inserted_id)

    def get_user_history(self, user_id: str, period: str = None) -> List[Dict[str, Any]]:
        """Récupérer l'historique d'un utilisateur"""
        if not self.use_mongodb:
            return []

        query = {"user_id": user_id}
        if period:
            query["summary.period"] = period

        return list(self.db.prediction_history.find(query).sort("created_at", -1))

    def get_farm_history(self, farm_id: str) -> List[Dict[str, Any]]:
        """Récupérer l'historique d'une exploitation"""
        if not self.use_mongodb:
            return []

        return list(self.db.prediction_history.find(
            {"farm_id": farm_id}
        ).sort("created_at", -1))

    def update_accuracy_metrics(self, user_id: str, period: str, metrics: Dict[str, Any]) -> bool:
        """Mettre à jour les métriques de précision"""
        if not self.use_mongodb:
            return False

        result = self.db.prediction_history.update_one(
            {"user_id": user_id, "summary.period": period},
            {
                "$set": {
                    "accuracy_metrics": metrics,
                    "updated_at": datetime.now()
                }
            }
        )
        return result.modified_count > 0

    def get_seasonal_analysis(self, user_id: str, year: int = None) -> Dict[str, Any]:
        """Obtenir l'analyse saisonnière"""
        if not self.use_mongodb:
            return {}

        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$unwind": "$seasonal_patterns"},
            {"$group": {
                "_id": "$seasonal_patterns.season",
                "total_predictions": {"$sum": "$seasonal_patterns.prediction_count"},
                "common_diseases": {"$push": "$seasonal_patterns.diseases"}
            }}
        ]

        if year:
            pipeline.insert(1, {"$match": {"summary.start_date": {"$gte": datetime(year, 1, 1)}}})

        results = list(self.db.prediction_history.aggregate(pipeline))
        return {result["_id"]: result for result in results}

    def get_treatment_effectiveness_trends(self, user_id: str) -> List[Dict[str, Any]]:
        """Obtenir les tendances d'efficacité des traitements"""
        if not self.use_mongodb:
            return []

        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$unwind": "$treatment_effectiveness"},
            {"$sort": {"created_at": -1}},
            {"$limit": 10}
        ]

        return list(self.db.prediction_history.aggregate(pipeline))


class SystemLogsService:
    """Service pour gérer les logs système"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def create_log(self, log_data: Dict[str, Any]) -> str:
        """Créer un nouveau log"""
        if not self.use_mongodb:
            raise Exception("MongoDB requis pour cette opération")

        log_doc = {
            "log_id": log_data["log_id"],
            "timestamp": datetime.now(),
            "level": log_data["level"],
            "source": log_data["source"],
            "event_type": log_data["event_type"],
            "message": log_data["message"],
            "details": log_data.get("details", {}),
            "performance_metrics": log_data.get("performance_metrics", {}),
            "context": log_data.get("context", {}),
            "created_at": datetime.now()
        }

        result = self.db.system_logs.insert_one(log_doc)
        return str(result.inserted_id)

    def get_logs_by_level(self, level: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les logs par niveau"""
        if not self.use_mongodb:
            return []

        return list(self.db.system_logs.find(
            {"level": level}
        ).sort("timestamp", -1).limit(limit))

    def get_logs_by_source(self, source: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les logs par source"""
        if not self.use_mongodb:
            return []

        return list(self.db.system_logs.find(
            {"source": source}
        ).sort("timestamp", -1).limit(limit))

    def get_logs_by_event_type(self, event_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les logs par type d'événement"""
        if not self.use_mongodb:
            return []

        return list(self.db.system_logs.find(
            {"event_type": event_type}
        ).sort("timestamp", -1).limit(limit))

    def get_logs_by_user(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupérer les logs d'un utilisateur"""
        if not self.use_mongodb:
            return []

        return list(self.db.system_logs.find(
            {"details.user_id": user_id}
        ).sort("timestamp", -1).limit(limit))

    def get_error_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les logs d'erreur"""
        if not self.use_mongodb:
            return []

        return list(self.db.system_logs.find(
            {"level": {"$in": ["ERROR", "CRITICAL"]}}
        ).sort("timestamp", -1).limit(limit))

    def get_performance_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Obtenir les métriques de performance"""
        if not self.use_mongodb:
            return {}

        pipeline = [
            {"$match": {
                "timestamp": {"$gte": start_date, "$lte": end_date},
                "performance_metrics.execution_time": {"$exists": True}
            }},
            {"$group": {
                "_id": "$source",
                "avg_execution_time": {"$avg": "$performance_metrics.execution_time"},
                "max_execution_time": {"$max": "$performance_metrics.execution_time"},
                "min_execution_time": {"$min": "$performance_metrics.execution_time"},
                "avg_memory_usage": {"$avg": "$performance_metrics.memory_usage"},
                "avg_cpu_usage": {"$avg": "$performance_metrics.cpu_usage"},
                "total_requests": {"$sum": 1}
            }}
        ]

        results = list(self.db.system_logs.aggregate(pipeline))
        return {result["_id"]: result for result in results}

    def cleanup_old_logs(self, days_to_keep: int = 30) -> int:
        """Nettoyer les anciens logs"""
        if not self.use_mongodb:
            return 0

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        result = self.db.system_logs.delete_many({"timestamp": {"$lt": cutoff_date}})
        return result.deleted_count

    def get_system_health_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé de la santé du système"""
        if not self.use_mongodb:
            return {}

        pipeline = [
            {"$match": {"timestamp": {"$gte": datetime.now() - timedelta(hours=24)}}},
            {"$group": {
                "_id": "$level",
                "count": {"$sum": 1},
                "sources": {"$addToSet": "$source"}
            }}
        ]

        results = list(self.db.system_logs.aggregate(pipeline))
        return {
            "last_24h_summary": {result["_id"]: result for result in results},
            "total_logs": sum(result["count"] for result in results),
            "active_sources": len(set().union(*[result["sources"] for result in results]))
        }


class AnalyticsService:
    """Service pour les analyses et statistiques avancées"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db = db_manager.db if db_manager.use_mongodb else None
        self.use_mongodb = db_manager.use_mongodb

    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Obtenir les analytics d'un utilisateur"""
        if not self.use_mongodb:
            return {}

        # Récupérer les données de base
        user = self.db.users.find_one({"user_id": user_id})
        if not user:
            return {}

        # Statistiques des prédictions
        predictions_count = self.db.predictions.count_documents({"user_id": user_id})

        # Précision des prédictions
        correct_predictions = self.db.predictions.count_documents({
            "user_id": user_id,
            "user_feedback.is_correct": True
        })

        accuracy = (correct_predictions / predictions_count * 100) if predictions_count > 0 else 0

        # Maladies les plus détectées
        disease_pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$disease_info.disease_id",
                "count": {"$sum": 1},
                "avg_confidence": {"$avg": "$classification.confidence"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]

        top_diseases = list(self.db.predictions.aggregate(disease_pipeline))

        # Évolution temporelle
        temporal_pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"}
                },
                "count": {"$sum": 1},
                "avg_confidence": {"$avg": "$classification.confidence"}
            }},
            {"$sort": {"_id.year": 1, "_id.month": 1}}
        ]

        temporal_data = list(self.db.predictions.aggregate(temporal_pipeline))

        return {
            "user_profile": {
                "user_id": user_id,
                "total_predictions": predictions_count,
                "accuracy_percentage": round(accuracy, 2),
                "experience_level": user.get("farmer_info", {}).get("experience_years", 0)
            },
            "top_diseases": top_diseases,
            "temporal_evolution": temporal_data,
            "recent_activity": self._get_recent_activity(user_id)
        }

    def get_disease_analytics(self, disease_id: str) -> Dict[str, Any]:
        """Obtenir les analytics d'une maladie"""
        if not self.use_mongodb:
            return {}

        # Fréquence de détection
        detection_count = self.db.predictions.count_documents({"disease_info.disease_id": disease_id})

        # Confiance moyenne
        confidence_pipeline = [
            {"$match": {"disease_info.disease_id": disease_id}},
            {"$group": {
                "_id": None,
                "avg_confidence": {"$avg": "$classification.confidence"},
                "min_confidence": {"$min": "$classification.confidence"},
                "max_confidence": {"$max": "$classification.confidence"}
            }}
        ]

        confidence_stats = list(self.db.predictions.aggregate(confidence_pipeline))

        # Distribution géographique
        geo_pipeline = [
            {"$match": {"disease_info.disease_id": disease_id}},
            {"$group": {
                "_id": "$location.address",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]

        geo_distribution = list(self.db.predictions.aggregate(geo_pipeline))

        # Efficacité des traitements
        treatment_pipeline = [
            {"$match": {"disease_id": disease_id}},
            {"$group": {
                "_id": "$implementation.status",
                "count": {"$sum": 1},
                "avg_effectiveness": {"$avg": "$implementation.effectiveness_rating"}
            }}
        ]

        treatment_stats = list(self.db.treatments.aggregate(treatment_pipeline))

        return {
            "disease_id": disease_id,
            "detection_frequency": detection_count,
            "confidence_statistics": confidence_stats[0] if confidence_stats else {},
            "geographic_distribution": geo_distribution,
            "treatment_effectiveness": treatment_stats,
            "seasonal_patterns": self._get_disease_seasonal_patterns(disease_id)
        }

    def get_system_analytics(self) -> Dict[str, Any]:
        """Obtenir les analytics du système"""
        if not self.use_mongodb:
            return {}

        # Utilisateurs actifs
        active_users = self.db.users.count_documents({"is_active": True})

        # Prédictions par jour (derniers 30 jours)
        daily_predictions = self._get_daily_predictions_stats()

        # Top des maladies détectées
        top_diseases_pipeline = [
            {"$group": {
                "_id": "$disease_info.disease_id",
                "count": {"$sum": 1},
                "avg_confidence": {"$avg": "$classification.confidence"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]

        top_diseases = list(self.db.predictions.aggregate(top_diseases_pipeline))

        # Métriques de performance
        performance_logs = self.db.system_logs.find(
            {"performance_metrics.execution_time": {"$exists": True}},
            {"performance_metrics": 1}
        ).sort("timestamp", -1).limit(1000)

        avg_response_time = sum(log["performance_metrics"]["execution_time"] for log in performance_logs) / len(
            list(performance_logs))

        return {
            "overview": {
                "total_users": active_users,
                "total_predictions": self.db.predictions.count_documents({}),
                "total_treatments": self.db.treatments.count_documents({}),
                "avg_response_time": round(avg_response_time, 3)
            },
            "daily_predictions": daily_predictions,
            "top_diseases": top_diseases,
            "user_distribution": self._get_user_distribution(),
            "system_health": self._get_system_health_metrics()
        }

    def _get_recent_activity(self, user_id: str) -> List[Dict[str, Any]]:
        """Récupérer l'activité récente d'un utilisateur"""
        return list(self.db.predictions.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(10))

    def _get_disease_seasonal_patterns(self, disease_id: str) -> List[Dict[str, Any]]:
        """Obtenir les patterns saisonniers d'une maladie"""
        pipeline = [
            {"$match": {"disease_info.disease_id": disease_id}},
            {"$group": {
                "_id": {"$month": "$created_at"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]

        return list(self.db.predictions.aggregate(pipeline))

    def _get_daily_predictions_stats(self) -> List[Dict[str, Any]]:
        """Obtenir les statistiques quotidiennes des prédictions"""
        from datetime import timedelta

        start_date = datetime.now() - timedelta(days=30)

        pipeline = [
            {"$match": {"created_at": {"$gte": start_date}}},
            {"$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"}
                },
                "count": {"$sum": 1},
                "avg_confidence": {"$avg": "$classification.confidence"}
            }},
            {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}}
        ]

        return list(self.db.predictions.aggregate(pipeline))

    def _get_user_distribution(self) -> Dict[str, Any]:
        """Obtenir la distribution des utilisateurs"""
        pipeline = [
            {"$group": {
                "_id": "$profile.country",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]

        return list(self.db.users.aggregate(pipeline))

    def _get_system_health_metrics(self) -> Dict[str, Any]:
        """Obtenir les métriques de santé du système"""
        error_count = self.db.system_logs.count_documents({
            "level": {"$in": ["ERROR", "CRITICAL"]},
            "timestamp": {"$gte": datetime.now() - timedelta(hours=24)}
        })

        total_logs = self.db.system_logs.count_documents({
            "timestamp": {"$gte": datetime.now() - timedelta(hours=24)}
        })

        return {
            "error_rate": (error_count / total_logs * 100) if total_logs > 0 else 0,
            "total_errors_24h": error_count,
            "total_logs_24h": total_logs
        }


# Classe principale pour combiner tous les services
class ServiceManager:
    """Gestionnaire principal pour tous les services"""

    def __init__(self, db_manager):
        self.db_manager = db_manager

        # Services existants
        self.user_service = UserService(db_manager)
        self.crop_service = CropService(db_manager)
        self.prediction_service = PredictionService(db_manager)
        self.treatment_service = TreatmentService(db_manager)
        self.farm_service = FarmService(db_manager)
        self.feedback_service = FeedbackService(db_manager)

        # Nouveaux services
        self.image_service = ImageService(db_manager)
        self.prediction_history_service = PredictionHistoryService(db_manager)
        self.system_logs_service = SystemLogsService(db_manager)
        self.analytics_service = AnalyticsService(db_manager)

    def get_complete_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Obtenir le profil complet d'un utilisateur"""
        user = self.user_service.get_user(user_id)
        if not user:
            return {}

        farms = self.farm_service.get_user_farms(user_id)
        predictions = self.prediction_service.get_user_predictions(user_id, limit=10)
        treatments = self.treatment_service.get_user_treatments(user_id)
        images = self.image_service.get_user_images(user_id, limit=10)
        analytics = self.analytics_service.get_user_analytics(user_id)

        return {
            "user_profile": user,
            "farms": farms,
            "recent_predictions": predictions,
            "treatments": treatments,
            "images": images,
            "analytics": analytics
        }

    def get_system_dashboard(self) -> Dict[str, Any]:
        """Obtenir le tableau de bord du système"""
        system_analytics = self.analytics_service.get_system_analytics()
        health_summary = self.system_logs_service.get_system_health_summary()

        return {
            "system_analytics": system_analytics,
            "health_summary": health_summary,
            "model_info": self.db_manager.get_model_info()
        }

    def close(self):
        """Fermer toutes les connexions"""
        self.db_manager.close()