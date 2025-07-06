from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from typing import Optional, List, Dict, Any, TypedDict
from enum import Enum
import json
import os

# Configuration MongoDB
MONGODB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "agriguard_db"

class UrgencyLevel(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DiseaseType(Enum):
    VIRAL = "maladie_virale"
    FUNGAL = "maladie_fongique"
    BACTERIAL = "maladie_bacterienne"
    PEST = "ravageur_insecte"
    HEALTHY = "etat_sain"

class TreatmentType(Enum):
    PREVENTIVE = "preventif"
    CHEMICAL = "chimique"
    BIOLOGICAL = "biologique"
    CULTURAL = "cultural"
    STORAGE = "stockage"

# Define TypedDict classes for complex nested structures
class PathogenDict(TypedDict):
    virus: Optional[str]
    full_name: str
    french_name: str
    role: str
    pathogen_type: Optional[str]

class VectorDict(TypedDict):
    name: str
    scientific_name: str
    virus_transmitted: Optional[str]
    transmission_mode: Optional[str]
    percentage_in_study: Optional[str]
    description: str

class TreatmentOptionDict(TypedDict):
    treatment_id: str
    type: str
    category: str
    product: str
    dosage: str
    timing: str
    priority: str
    description: str
    cost_estimate: Optional[float]
    availability: Optional[str]
    effectiveness: Optional[str]

class ImageDict(TypedDict):
    url: str
    description: str
    type: str

class MetadataDict(TypedDict):
    is_default: bool
    data_source: str
    version: str
    confidence_level: float

# 1. USERS COLLECTION (unchanged)
users_schema = {
    "_id": ObjectId,
    "user_id": str,
    "password_hash": str,
    "profile": {
        "first_name": str,
        "last_name": str,
        "email": str,
        "phone": str,
        "avatar_url": Optional[str],
        "language": str,
        "country": str,
        "region": str,
        "city": str
    },
    "farmer_info": {
        "experience_years": int,
        "farm_size_hectares": float,
        "primary_crops": List[str],
        "farming_type": str,
        "certifications": List[str]
    },
    "subscription": {
        "plan": str,
        "start_date": datetime,
        "end_date": Optional[datetime],
        "is_active": bool
    },
    "preferences": {
        "notification_settings": {
            "email": bool,
            "sms": bool,
            "push": bool
        },
        "language": str,
        "timezone": str
    },
    "stats": {
        "total_predictions": int,
        "successful_treatments": int,
        "farms_managed": int,
        "last_activity": datetime
    },
    "created_at": datetime,
    "updated_at": datetime,
    "is_active": bool
}

# 2. CROPS COLLECTION (improved)
crops_schema = {
    "_id": ObjectId,
    "crop_id": str,
    "name": {
        "fr": str,
        "en": str,
        "scientific": str
    },
    "category": str,
    "supported_diseases": List[str],
    "growing_seasons": List[str],
    "description": {
        "fr": str,
        "en": str
    },
    "image_url": Optional[str],
    "common_varieties": List[str],
    "optimal_conditions": {
        "temperature_range": {"min": float, "max": float},
        "humidity_range": {"min": float, "max": float},
        "soil_type": List[str],
        "ph_range": {"min": float, "max": float}
    },
    "is_active": bool,
    "created_at": datetime,
    "updated_at": datetime
}

# 3. DISEASES COLLECTION (improved to support default data)
diseases_schema = {
    "_id": ObjectId,
    "disease_id": str,
    "name": {
        "fr": str,
        "en": str,
        "scientific": Optional[str]
    },
    "type": str,
    "description": {
        "fr": str,
        "en": str
    },
    "crops_affected": List[str],
    "urgency": str,
    "symptoms": {
        "fr": List[str],
        "en": List[str]
    },
    "pathogens": List[PathogenDict],
    "vectors": List[VectorDict],
    "treatment_options": List[TreatmentOptionDict],
    "prevention_measures": List[str],
    "impact": {
        "description": str,
        "yield_loss_percentage": Optional[str],
        "economic_impact": Optional[str]
    },
    "geographic_distribution": str,
    "images": List[ImageDict],
    "references": List[str],
    "metadata": MetadataDict,
    "created_at": datetime,
    "updated_at": datetime,
    "is_active": bool
}

# 4. PREDICTIONS COLLECTION (unchanged)
predictions_schema = {
    "_id": ObjectId,
    "prediction_id": str,
    "user_id": str,
    "farm_id": Optional[str],
    "image_info": {
        "image_id": str,
        "original_filename": str,
        "file_path": str,
        "file_size": int,
        "mime_type": str,
        "dimensions": {
            "width": int,
            "height": int
        }
    },
    "classification": {
        "predicted_class": str,
        "class_id": int,
        "confidence": float,
        "confidence_percentage": float,
        "model_version": str,
        "top5_predictions": List[Dict[str, Any]]
    },
    "disease_info": {
        "disease_id": str,
        "category": str,
        "urgency": str,
        "risk_level": str
    },
    "location": {
        "coordinates": {
            "latitude": float,
            "longitude": float
        },
        "address": Optional[str],
        "farm_zone": Optional[str]
    },
    "environmental_context": {
        "weather_conditions": Optional[str],
        "temperature": Optional[float],
        "humidity": Optional[float],
        "season": Optional[str]
    },
    "user_feedback": {
        "is_correct": Optional[bool],
        "actual_disease": Optional[str],
        "confidence_rating": Optional[int],
        "comments": Optional[str],
        "feedback_date": Optional[datetime]
    },
    "processing_time": float,
    "status": str,
    "created_at": datetime,
    "updated_at": datetime
}

# 5. IMAGES COLLECTION (unchanged)
images_schema = {
    "_id": ObjectId,
    "image_id": str,
    "user_id": str,
    "original_filename": str,
    "file_info": {
        "file_path": str,
        "file_size": int,
        "mime_type": str,
        "dimensions": {
            "width": int,
            "height": int
        },
        "quality": Optional[str],
        "camera_info": Optional[str]
    },
    "metadata": {
        "capture_date": Optional[datetime],
        "location": Optional[Dict[str, float]],
        "device_info": Optional[str],
        "exif_data": Optional[Dict[str, Any]]
    },
    "processing_info": {
        "is_processed": bool,
        "preprocessing_applied": List[str],
        "thumbnail_path": Optional[str],
        "compressed_path": Optional[str]
    },
    "usage": {
        "prediction_count": int,
        "last_used": Optional[datetime],
        "associated_predictions": List[str]
    },
    "created_at": datetime,
    "updated_at": datetime,
    "is_active": bool
}

# 6. TREATMENTS COLLECTION (unchanged)
treatments_schema = {
    "_id": ObjectId,
    "treatment_id": str,
    "user_id": str,
    "prediction_id": str,
    "disease_id": str,
    "farm_id": Optional[str],
    "recommended_treatments": List[Dict[str, Any]],
    "treatment_plan": {
        "start_date": datetime,
        "end_date": Optional[datetime],
        "frequency": str,
        "total_applications": int,
        "notes": Optional[str]
    },
    "implementation": {
        "status": str,
        "applications_done": int,
        "results": Optional[str],
        "effectiveness_rating": Optional[int],
        "side_effects": Optional[str],
        "cost_actual": Optional[float]
    },
    "follow_up": {
        "next_inspection_date": Optional[datetime],
        "monitoring_frequency": str,
        "success_indicators": List[str],
        "failure_indicators": List[str]
    },
    "created_at": datetime,
    "updated_at": datetime,
    "is_active": bool
}

# 7. USER_FARMS COLLECTION (unchanged)
user_farms_schema = {
    "_id": ObjectId,
    "farm_id": str,
    "user_id": str,
    "farm_info": {
        "name": str,
        "description": Optional[str],
        "total_area": float,
        "location": {
            "coordinates": {
                "latitude": float,
                "longitude": float
            },
            "address": str,
            "country": str,
            "region": str,
            "city": str
        },
        "zones": List[Dict[str, Any]]
    },
    "crops_grown": List[Dict[str, Any]],
    "management_practices": {
        "irrigation_type": str,
        "fertilization_schedule": List[Dict[str, Any]],
        "pest_management": str,
        "organic_certified": bool
    },
    "history": {
        "diseases_encountered": List[str],
        "treatments_applied": List[str],
        "yield_records": List[Dict[str, Any]]
    },
    "created_at": datetime,
    "updated_at": datetime,
    "is_active": bool
}

# 8. PREDICTION_HISTORY COLLECTION (unchanged)
prediction_history_schema = {
    "_id": ObjectId,
    "user_id": str,
    "farm_id": Optional[str],
    "summary": {
        "total_predictions": int,
        "period": str,
        "start_date": datetime,
        "end_date": datetime
    },
    "diseases_detected": List[Dict[str, Any]],
    "accuracy_metrics": {
        "user_confirmed_correct": int,
        "user_confirmed_incorrect": int,
        "accuracy_percentage": float,
        "confidence_average": float
    },
    "seasonal_patterns": List[Dict[str, Any]],
    "treatment_effectiveness": List[Dict[str, Any]],
    "created_at": datetime,
    "updated_at": datetime
}

# 9. FEEDBACK COLLECTION (unchanged)
feedback_schema = {
    "_id": ObjectId,
    "feedback_id": str,
    "user_id": str,
    "prediction_id": Optional[str],
    "treatment_id": Optional[str],
    "feedback_type": str,
    "rating": int,
    "feedback_data": {
        "accuracy_rating": Optional[int],
        "ease_of_use": Optional[int],
        "helpfulness": Optional[int],
        "recommendation_likelihood": Optional[int]
    },
    "comments": {
        "what_worked": Optional[str],
        "improvements_needed": Optional[str],
        "general_comments": Optional[str]
    },
    "user_corrections": {
        "correct_disease": Optional[str],
        "actual_treatment_used": Optional[str],
        "results_observed": Optional[str]
    },
    "metadata": {
        "device_type": Optional[str],
        "app_version": Optional[str],
        "submission_method": str
    },
    "status": str,
    "admin_response": Optional[str],
    "created_at": datetime,
    "updated_at": datetime
}

# 10. SYSTEM_LOGS COLLECTION (unchanged)
system_logs_schema = {
    "_id": ObjectId,
    "log_id": str,
    "timestamp": datetime,
    "level": str,
    "source": str,
    "event_type": str,
    "message": str,
    "details": {
        "user_id": Optional[str],
        "prediction_id": Optional[str],
        "error_code": Optional[str],
        "stack_trace": Optional[str],
        "request_data": Optional[Dict[str, Any]],
        "response_data": Optional[Dict[str, Any]]
    },
    "performance_metrics": {
        "execution_time": Optional[float],
        "memory_usage": Optional[float],
        "cpu_usage": Optional[float]
    },
    "context": {
        "ip_address": Optional[str],
        "user_agent": Optional[str],
        "request_id": Optional[str],
        "session_id": Optional[str]
    },
    "created_at": datetime
}

# INDEX CONFIGURATIONS (improved)
indexes_config = {
    "users": [
        {"keys": [("user_id", 1)], "unique": True},
        {"keys": [("profile.email", 1)], "unique": True},
        {"keys": [("created_at", -1)]},
        {"keys": [("profile.country", 1), ("profile.region", 1)]}
    ],
    "crops": [
        {"keys": [("crop_id", 1)], "unique": True},
        {"keys": [("is_active", 1)]},
        {"keys": [("category", 1)]}
    ],
    "diseases": [
        {"keys": [("disease_id", 1)], "unique": True},
        {"keys": [("urgency", 1)]},
        {"keys": [("type", 1)]},
        {"keys": [("crops_affected", 1)]},
        {"keys": [("metadata.is_default", 1)]},
        {"keys": [("is_active", 1)]}
    ],
    "predictions": [
        {"keys": [("prediction_id", 1)], "unique": True},
        {"keys": [("user_id", 1), ("created_at", -1)]},
        {"keys": [("classification.predicted_class", 1)]},
        {"keys": [("disease_info.urgency", 1)]},
        {"keys": [("location.coordinates", "2dsphere")]}
    ],
    "images": [
        {"keys": [("image_id", 1)], "unique": True},
        {"keys": [("user_id", 1), ("created_at", -1)]},
        {"keys": [("processing_info.is_processed", 1)]}
    ],
    "treatments": [
        {"keys": [("treatment_id", 1)], "unique": True},
        {"keys": [("user_id", 1), ("created_at", -1)]},
        {"keys": [("prediction_id", 1)]},
        {"keys": [("implementation.status", 1)]}
    ],
    "user_farms": [
        {"keys": [("farm_id", 1)], "unique": True},
        {"keys": [("user_id", 1)]},
        {"keys": [("farm_info.location.coordinates", "2dsphere")]}
    ],
    "prediction_history": [
        {"keys": [("user_id", 1), ("summary.period", 1)]},
        {"keys": [("summary.start_date", 1), ("summary.end_date", 1)]}
    ],
    "feedback": [
        {"keys": [("feedback_id", 1)], "unique": True},
        {"keys": [("user_id", 1), ("created_at", -1)]},
        {"keys": [("feedback_type", 1)]},
        {"keys": [("rating", 1)]}
    ],
    "system_logs": [
        {"keys": [("log_id", 1)], "unique": True},
        {"keys": [("timestamp", -1)]},
        {"keys": [("level", 1)]},
        {"keys": [("source", 1)]},
        {"keys": [("event_type", 1)]}
    ]
}



def load_default_data(json_file_path: str = "default_data.json") -> Dict[str, List[Dict[str, Any]]]:
    """
    Charge les données par défaut des maladies et cultures depuis un fichier JSON externe

    Args:
        json_file_path: Chemin vers le fichier JSON contenant les données par défaut

    Returns:
        Dict contenant les données formatées pour MongoDB: {"crops": [...], "diseases": [...]}

    Raises:
        FileNotFoundError: Si le fichier JSON n'existe pas
        json.JSONDecodeError: Si le fichier JSON est malformé
        KeyError: Si la structure JSON ne correspond pas à ce qui est attendu
    """

    # Vérifier que le fichier existe
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"Le fichier de données par défaut '{json_file_path}' n'existe pas")

    try:
        # Charger le fichier JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extraire les données
        diseases_data = data.get("diseases", {})
        classes_data = data.get("classes", {})
        legacy_pests_data = data.get("legacy_pests", {})
        metadata = data.get("metadata", {})

        # Préparer les collections
        crops = []
        diseases = []

        # =====================================================
        # TRAITEMENT DES CULTURES (CROPS)
        # =====================================================

        # Créer les données par défaut des cultures basées sur le contenu JSON
        default_crops = [
            {
                "crop_id": "mais",
                "name": {
                    "fr": "Maïs",
                    "en": "Maize",
                    "scientific": "Zea mays"
                },
                "category": "cereal",
                "supported_diseases": ["MLN", "MSV", "saine"],
                "growing_seasons": ["saison_seche", "saison_pluvieuse"],
                "description": {
                    "fr": "Céréale de base largement cultivée",
                    "en": "Widely cultivated staple cereal"
                },
                "common_varieties": ["Variété locale", "Hybride amélioré"],
                "optimal_conditions": {
                    "temperature_range": {"min": 15.0, "max": 35.0},
                    "humidity_range": {"min": 40.0, "max": 80.0},
                    "soil_type": ["limoneux", "sableux"],
                    "ph_range": {"min": 6.0, "max": 7.5}
                },
                "is_active": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "crop_id": "sorgho",
                "name": {
                    "fr": "Sorgho",
                    "en": "Sorghum",
                    "scientific": "Sorghum bicolor"
                },
                "category": "cereal",
                "supported_diseases": ["legionnaire_automne"],
                "growing_seasons": ["saison_seche"],
                "description": {
                    "fr": "Céréale résistante à la sécheresse",
                    "en": "Drought-resistant cereal"
                },
                "common_varieties": ["Sorgho rouge", "Sorgho blanc"],
                "optimal_conditions": {
                    "temperature_range": {"min": 20.0, "max": 40.0},
                    "humidity_range": {"min": 30.0, "max": 70.0},
                    "soil_type": ["argileux", "sableux"],
                    "ph_range": {"min": 6.0, "max": 8.0}
                },
                "is_active": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]

        crops.extend(default_crops)

        # =====================================================
        # TRAITEMENT DES MALADIES (DISEASES)
        # =====================================================

        # Traiter les maladies principales
        for disease_id, disease_data in diseases_data.items():
            disease_doc = _transform_disease_to_mongo(disease_id, disease_data, metadata)
            diseases.append(disease_doc)

        # Traiter les classes (comme "saine")
        for class_id, class_data in classes_data.items():
            class_doc = _transform_class_to_mongo(class_id, class_data, metadata)
            diseases.append(class_doc)

        # Traiter les ravageurs legacy
        for pest_id, pest_data in legacy_pests_data.items():
            pest_doc = _transform_pest_to_mongo(pest_id, pest_data, metadata)
            diseases.append(pest_doc)

        return {
            "crops": crops,
            "diseases": diseases,
            "metadata": metadata
        }

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Erreur de format JSON dans le fichier '{json_file_path}': {e}")
    except KeyError as e:
        raise KeyError(f"Clé manquante dans la structure JSON: {e}")
    except Exception as e:
        raise Exception(f"Erreur lors du chargement des données par défaut: {e}")
def _transform_disease_to_mongo(disease_id: str, disease_data: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforme une maladie du format JSON vers le format MongoDB
    """
    return {
        "disease_id": disease_id,
        "name": {
            "fr": disease_data.get("name", ""),
            "en": disease_data.get("scientific_name", ""),
            "scientific": disease_data.get("scientific_name", "")
        },
        "type": disease_data.get("type", ""),
        "description": {
            "fr": disease_data.get("description", ""),
            "en": disease_data.get("description", "")
        },
        "crops_affected": disease_data.get("crops", []),
        "urgency": disease_data.get("urgency", "medium"),
        "symptoms": {
            "fr": disease_data.get("symptoms", []),
            "en": disease_data.get("symptoms", [])
        },
        "pathogens": disease_data.get("pathogens", []),
        "vectors": disease_data.get("vectors", []),
        "treatment_options": _transform_treatments(disease_data.get("treatment", [])),
        "prevention_measures": disease_data.get("prevention", []),
        "impact": {
            "description": disease_data.get("impact", ""),
            "yield_loss_percentage": _extract_yield_loss(disease_data.get("impact", "")),
            "economic_impact": _determine_economic_impact(disease_data.get("urgency", "medium"))
        },
        "geographic_distribution": disease_data.get("geographic_distribution", ""),
        "images": [],
        "references": metadata.get("reference_sources", []),
        "metadata": {
            "is_default": True,
            "data_source": "JSON Import",
            "version": metadata.get("version", "2.0"),
            "confidence_level": 0.95
        },
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True
    }
def _transform_class_to_mongo(class_id: str, class_data: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforme une classe (comme "saine") du format JSON vers le format MongoDB
    """
    return {
        "disease_id": class_id,
        "name": {
            "fr": class_data.get("name", ""),
            "en": class_data.get("name", ""),
            "scientific": None
        },
        "type": class_data.get("type", "etat_sain"),
        "description": {
            "fr": class_data.get("description", ""),
            "en": class_data.get("description", "")
        },
        "crops_affected": class_data.get("crops", []),
        "urgency": class_data.get("urgency", "none"),
        "symptoms": {
            "fr": class_data.get("symptoms", []),
            "en": class_data.get("symptoms", [])
        },
        "pathogens": [],
        "vectors": [],
        "treatment_options": _transform_treatments(class_data.get("recommendations", [])),
        "prevention_measures": class_data.get("recommendations", []),
        "impact": {
            "description": "Aucun impact négatif - État sain",
            "yield_loss_percentage": "0%",
            "economic_impact": "Aucun"
        },
        "geographic_distribution": "Universel",
        "images": [],
        "references": [],
        "metadata": {
            "is_default": True,
            "data_source": "JSON Import",
            "version": metadata.get("version", "2.0"),
            "confidence_level": 1.0
        },
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True
    }
def _transform_pest_to_mongo(pest_id: str, pest_data: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforme un ravageur legacy du format JSON vers le format MongoDB
    """
    return {
        "disease_id": pest_id,
        "name": {
            "fr": pest_data.get("name", ""),
            "en": pest_data.get("name", ""),
            "scientific": pest_data.get("scientific_name", "")
        },
        "type": pest_data.get("type", "ravageur_insecte"),
        "description": {
            "fr": pest_data.get("description", ""),
            "en": pest_data.get("description", "")
        },
        "crops_affected": pest_data.get("crops", []),
        "urgency": pest_data.get("urgency", "medium"),
        "symptoms": {
            "fr": pest_data.get("symptoms", []),
            "en": pest_data.get("symptoms", [])
        },
        "pathogens": [{
            "virus": None,
            "full_name": pest_data.get("scientific_name", ""),
            "french_name": pest_data.get("name", ""),
            "role": "Ravageur principal",
            "pathogen_type": "insecte"
        }],
        "vectors": [],
        "treatment_options": _transform_treatments(pest_data.get("treatment", [])),
        "prevention_measures": pest_data.get("prevention", []),
        "impact": {
            "description": pest_data.get("description", ""),
            "yield_loss_percentage": "Variable",
            "economic_impact": _determine_economic_impact(pest_data.get("urgency", "medium"))
        },
        "geographic_distribution": "Selon distribution naturelle",
        "images": [],
        "references": [],
        "metadata": {
            "is_default": True,
            "data_source": "JSON Import - Legacy",
            "version": metadata.get("version", "2.0"),
            "confidence_level": 0.85
        },
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True
    }
def _transform_treatments(treatments: List[Any]) -> List[Dict[str, Any]]:
    """
    Transforme les traitements du format JSON vers le format MongoDB
    """
    transformed_treatments = []

    for i, treatment in enumerate(treatments):
        if isinstance(treatment, dict):
            # Format standard de traitement
            transformed_treatment = {
                "treatment_id": f"TREAT_{i+1:03d}",
                "type": treatment.get("type", "unknown"),
                "category": treatment.get("category", "general"),
                "product": treatment.get("product", ""),
                "dosage": treatment.get("dosage", ""),
                "timing": treatment.get("timing", ""),
                "priority": treatment.get("priority", "medium"),
                "description": treatment.get("description", ""),
                "cost_estimate": None,
                "availability": None,
                "effectiveness": treatment.get("effectiveness", "medium")
            }
        elif isinstance(treatment, str):
            # Format simple (recommandations)
            transformed_treatment = {
                "treatment_id": f"REC_{i+1:03d}",
                "type": "preventif",
                "category": "recommendation",
                "product": "N/A",
                "dosage": "N/A",
                "timing": "Selon besoins",
                "priority": "medium",
                "description": treatment,
                "cost_estimate": None,
                "availability": None,
                "effectiveness": "medium"
            }
        else:
            continue

        transformed_treatments.append(transformed_treatment)

    return transformed_treatments
def _extract_yield_loss(impact_text: str) -> str:
    """
    Extrait le pourcentage de perte de rendement du texte d'impact
    """
    import re

    # Rechercher des patterns comme "20-90%", "10-50%", etc.
    pattern = r'(\d+(?:-\d+)?%)'
    match = re.search(pattern, impact_text)

    if match:
        return match.group(1)
    else:
        return "Variable"
def _determine_economic_impact(urgency: str) -> str:
    """
    Détermine l'impact économique basé sur l'urgence
    """
    impact_mapping = {
        "none": "Aucun",
        "low": "Faible",
        "medium": "Modéré",
        "high": "Élevé",
        "critical": "Très élevé"
    }

    return impact_mapping.get(urgency, "Modéré")
def save_data_to_mongodb(data: Dict[str, List[Dict[str, Any]]],
                        mongodb_url: str = "mongodb://localhost:27017/",
                        database_name: str = "agriguard_db") -> Dict[str, int]:
    """
    Sauvegarde les données dans MongoDB

    Args:
        data: Données à sauvegarder (résultat de load_default_data)
        mongodb_url: URL de connexion MongoDB
        database_name: Nom de la base de données

    Returns:
        Dict avec le nombre d'enregistrements insérés par collection
    """
    from pymongo import MongoClient

    try:
        # Connexion à MongoDB
        client = MongoClient(mongodb_url)
        db = client[database_name]

        results = {}

        # Insérer les cultures
        if data["crops"]:
            crops_collection = db["crops"]
            # Supprimer les données existantes marquées comme par défaut
            crops_collection.delete_many({"metadata.is_default": True})
            # Insérer les nouvelles données
            result = crops_collection.insert_many(data["crops"])
            results["crops"] = len(result.inserted_ids)

        # Insérer les maladies
        if data["diseases"]:
            diseases_collection = db["diseases"]
            # Supprimer les données existantes marquées comme par défaut
            diseases_collection.delete_many({"metadata.is_default": True})
            # Insérer les nouvelles données
            result = diseases_collection.insert_many(data["diseases"])
            results["diseases"] = len(result.inserted_ids)

        client.close()
        return results

    except Exception as e:
        raise Exception(f"Erreur lors de la sauvegarde en MongoDB: {e}")

# FONCTION D'INITIALISATION DE LA BASE DE DONNÉES
def init_database():
    """
    Initialise la base de données avec les collections et index
    """
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    collections = [
        "users", "crops", "diseases", "predictions", "images",
        "treatments", "user_farms", "prediction_history", "feedback", "system_logs"
    ]

    # Créer les collections
    for collection_name in collections:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' créée")

    # Créer les index
    for collection_name, indexes in indexes_config.items():
        collection = db[collection_name]
        for index_config in indexes:
            collection.create_index(**index_config)
            print(f"Index créé pour {collection_name}: {index_config['keys']}")

    print("Base de données initialisée avec succès!")
    return db

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        db = init_database()
        # Charger les données depuis le fichier JSON
        print("Chargement des données par défaut...")
        data = load_default_data("data/diseases_database.json")

        print(f"Données chargées:")
        print(f"- {len(data['crops'])} cultures")
        print(f"- {len(data['diseases'])} maladies/classes")

        # Sauvegarder en MongoDB
        print("\nSauvegarde en MongoDB...")
        results = save_data_to_mongodb(data)

        print(f"Sauvegarde terminée:")
        for collection, count in results.items():
            print(f"- {collection}: {count} enregistrements")

    except Exception as e:
        print(f"Erreur: {e}")