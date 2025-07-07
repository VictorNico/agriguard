# app.py (Version mise à jour)
# app.py (Version avec sauvegarde permanente)
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from models.yolo_model_cls_db import MaizeDiseaseClassifier
from utils.image_processing import process_image
import uuid
import logging
from datetime import datetime, timedelta
import shutil
from models.database_manager import UserService
import jwt
import bcrypt
import secrets
import re
from functools import wraps

app = Flask(__name__)
CORS(app)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
PERMANENT_STORAGE = 'storage/images'
PREDICTIONS_LOG = 'storage/predictions'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_STORAGE'] = PERMANENT_STORAGE
app.config['PREDICTIONS_LOG'] = PREDICTIONS_LOG

# Configuration pour servir le frontend Nuxt
FRONTEND_DIST_DIR = '../corn-disease-app/.output/public'
app.config['FRONTEND_DIST_DIR'] = FRONTEND_DIST_DIR

# Configuration MongoDB (optionnelle)
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'agriguard_db')


# Configuration JWT (à ajouter dans votre configuration)
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# Créer les dossiers nécessaires
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PERMANENT_STORAGE, exist_ok=True)
os.makedirs(PREDICTIONS_LOG, exist_ok=True)
os.makedirs(f"{PREDICTIONS_LOG}/daily", exist_ok=True)

# Initialiser le classificateur
classifier = MaizeDiseaseClassifier(
    model_path='weights/best.pt',
    json_fallback_path='data/diseases_database.json',
    mongodb_url=MONGODB_URL,
    database_name=DATABASE_NAME
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def calculate_relevance_score(query, disease_info):
    """Calculer un score de pertinence pour la recherche"""
    score = 0
    query_lower = query.lower()

    # Score basé sur le nom
    name = disease_info.get('name', '').lower()
    if query_lower in name:
        score += 10

    # Score basé sur la description
    description = disease_info.get('description', '').lower()
    if query_lower in description:
        score += 5

    # Score basé sur les symptômes
    symptoms = str(disease_info.get('symptoms', [])).lower()
    if query_lower in symptoms:
        score += 3

    return score
def generate_timestamped_filename(original_filename):
    """Générer un nom de fichier avec timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # microseconds to milliseconds
    name, ext = os.path.splitext(original_filename)
    safe_name = secure_filename(name)
    return f"{timestamp}_{safe_name}{ext}"
def get_severity_level(confidence):
    """Déterminer le niveau de sévérité basé sur la confiance"""
    if confidence >= 0.9:
        return "very_high"
    elif confidence >= 0.8:
        return "high"
    elif confidence >= 0.6:
        return "medium"
    elif confidence >= 0.4:
        return "low"
    else:
        return "very_low"
def save_image_permanently(temp_filepath, original_filename):
    """Sauvegarder une image de manière permanente"""
    try:
        # Générer le nom de fichier avec timestamp
        permanent_filename = generate_timestamped_filename(original_filename)

        # Créer le dossier par date
        date_folder = datetime.now().strftime("%Y-%m-%d")
        daily_folder = os.path.join(PERMANENT_STORAGE, date_folder)
        os.makedirs(daily_folder, exist_ok=True)

        # Chemin complet du fichier permanent
        permanent_filepath = os.path.join(daily_folder, permanent_filename)

        # Copier le fichier
        shutil.copy2(temp_filepath, permanent_filepath)

        # Retourner le chemin relatif pour la base de données
        relative_path = os.path.join(date_folder, permanent_filename)

        return {
            "success": True,
            "permanent_filename": permanent_filename,
            "relative_path": relative_path,
            "absolute_path": permanent_filepath,
            "date_folder": date_folder
        }

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde permanente: {e}")
        return {
            "success": False,
            "error": str(e)
        }
def save_prediction_record(prediction_data):
    """Sauvegarder un enregistrement de prédiction"""
    try:
        # Fichier de log quotidien
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(PREDICTIONS_LOG, "daily", f"predictions_{date_str}.json")

        # Charger les prédictions existantes
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                predictions = json.load(f)
        else:
            predictions = {"date": date_str, "predictions": []}

        # Ajouter la nouvelle prédiction
        predictions["predictions"].append(prediction_data)

        # Sauvegarder
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(predictions, f, indent=2, ensure_ascii=False)

        # Aussi sauvegarder dans un fichier global
        global_log = os.path.join(PREDICTIONS_LOG, "all_predictions.json")

        if os.path.exists(global_log):
            with open(global_log, 'r', encoding='utf-8') as f:
                all_predictions = json.load(f)
        else:
            all_predictions = {"total_predictions": 0, "predictions": []}

        all_predictions["predictions"].append(prediction_data)
        all_predictions["total_predictions"] = len(all_predictions["predictions"])

        # Limiter à 1000 prédictions dans le fichier global
        if len(all_predictions["predictions"]) > 1000:
            all_predictions["predictions"] = all_predictions["predictions"][-1000:]

        with open(global_log, 'w', encoding='utf-8') as f:
            json.dump(all_predictions, f, indent=2, ensure_ascii=False)

        return {"success": True, "log_file": log_file}

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde de prédiction: {e}")
        return {"success": False, "error": str(e)}
def save_to_database_if_available(prediction_record):
    """Sauvegarder dans MongoDB si disponible"""
    try:
        if classifier.db_manager.use_mongodb:
            # Sauvegarder dans la collection predictions
            collection = classifier.db_manager.db.predictions
            result = collection.insert_one(prediction_record)
            return {"success": True, "inserted_id": str(result.inserted_id)}
        else:
            return {"success": False, "reason": "MongoDB not available"}
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde MongoDB: {e}")
        return {"success": False, "error": str(e)}



# Utilitaires d'authentification
def hash_password(password: str) -> str:
    """Hasher un mot de passe"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Vérifier un mot de passe"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def generate_tokens(user_id: str) -> dict:
    """Générer les tokens JWT"""
    access_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + JWT_ACCESS_TOKEN_EXPIRES,
        'iat': datetime.utcnow(),
        'type': 'access'
    }

    refresh_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + JWT_REFRESH_TOKEN_EXPIRES,
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }

    access_token = jwt.encode(access_payload, JWT_SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, JWT_SECRET_KEY, algorithm='HS256')

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': int(JWT_ACCESS_TOKEN_EXPIRES.total_seconds())
    }


def validate_email(email: str) -> bool:
    """Valider le format d'email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> dict:
    """Valider la force du mot de passe"""
    errors = []
    if len(password) < 8:
        errors.append("Le mot de passe doit contenir au moins 8 caractères")
    if not re.search(r'[A-Z]', password):
        errors.append("Le mot de passe doit contenir au moins une majuscule")
    if not re.search(r'[a-z]', password):
        errors.append("Le mot de passe doit contenir au moins une minuscule")
    if not re.search(r'[0-9]', password):
        errors.append("Le mot de passe doit contenir au moins un chiffre")

    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }


def token_required(f):
    """Décorateur pour vérifier l'authentification"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Récupérer le token du header Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
            except IndexError:
                return jsonify({'error': 'Format de token invalide'}), 401

        if not token:
            return jsonify({'error': 'Token manquant'}), 401

        try:
            # Décoder le token
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])

            # Vérifier que c'est un access token
            if payload.get('type') != 'access':
                return jsonify({'error': 'Type de token invalide'}), 401

            # Récupérer l'utilisateur
            user_id = payload['user_id']
            user_service = UserService(classifier.db_manager)
            current_user = user_service.get_user(user_id)

            if not current_user:
                return jsonify({'error': 'Utilisateur non trouvé'}), 401

            # Ajouter l'utilisateur à la requête
            request.current_user = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expiré'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token invalide'}), 401

        return f(*args, **kwargs)

    return decorated


# ========================================
# ENDPOINTS D'AUTHENTIFICATION
# ========================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    try:
        data = request.get_json()

        # Validation des données requises
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ {field} est requis'}), 400

        # Validation de l'email
        if not validate_email(data['email']):
            return jsonify({'error': 'Format d\'email invalide'}), 400

        # Validation du mot de passe
        password_validation = validate_password(data['password'])
        if not password_validation['is_valid']:
            return jsonify({
                'error': 'Mot de passe invalide',
                'details': password_validation['errors']
            }), 400

        # Vérifier si l'utilisateur existe déjà
        user_service = UserService(classifier.db_manager)
        existing_user = None

        if classifier.db_manager.use_mongodb:
            existing_user = classifier.db_manager.db.users.find_one({
                'profile.email': data['email'],
                'is_active': True
            })

        if existing_user:
            return jsonify({'error': 'Un utilisateur avec cet email existe déjà'}), 409

        # Créer l'utilisateur
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(data['password'])

        user_data = {
            'user_id': user_id,
            'profile': {
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'phone': data.get('phone', ''),
                'avatar_url': data.get('avatar_url'),
                'language': data.get('language', 'fr'),
                'country': data.get('country', 'CM'),
                'region': data.get('region', ''),
                'city': data.get('city', '')
            },
            'farmer_info': {
                'experience_years': data.get('experience_years', 0),
                'farm_size_hectares': data.get('farm_size_hectares', 0.0),
                'primary_crops': data.get('primary_crops', []),
                'farming_type': data.get('farming_type', 'traditional'),
                'certifications': data.get('certifications', [])
            },
            'subscription': {
                'plan': 'free',
                'start_date': datetime.now(),
                'is_active': True
            },
            'preferences': {
                'notification_settings': {
                    'email': True,
                    'sms': False,
                    'push': True
                },
                'language': data.get('language', 'fr'),
                'timezone': data.get('timezone', 'Africa/Douala')
            },
            'password_hash': hashed_password
        }

        # Sauvegarder l'utilisateur
        if classifier.db_manager.use_mongodb:
            user_service.create_user(user_data)
        else:
            return jsonify({'error': 'MongoDB requis pour l\'inscription'}), 503

        # Générer les tokens
        tokens = generate_tokens(user_id)

        # Récupérer l'utilisateur créé pour la réponse
        created_user = user_service.get_user(user_id)

        return jsonify({
            'success': True,
            'message': 'Utilisateur créé avec succès',
            'user': {
                'user_id': created_user['user_id'],
                'profile': created_user['profile'],
                'farmer_info': created_user['farmer_info'],
                'subscription': created_user['subscription']
            },
            'tokens': tokens
        }), 201

    except Exception as e:
        logger.error(f"Erreur lors de l'inscription: {e}")
        return jsonify({'error': 'Erreur lors de l\'inscription'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Connexion d'un utilisateur"""
    try:
        data = request.get_json()

        # Validation des données requises
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email et mot de passe requis'}), 400

        # Rechercher l'utilisateur
        if not classifier.db_manager.use_mongodb:
            return jsonify({'error': 'MongoDB requis pour la connexion'}), 503

        user = classifier.db_manager.db.users.find_one({
            'profile.email': data['email'],
            'is_active': True
        })

        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        # Vérifier le mot de passe
        if not verify_password(data['password'], user['password_hash']):
            return jsonify({'error': 'Mot de passe incorrect'}), 401

        # Mettre à jour la dernière activité
        classifier.db_manager.db.users.update_one(
            {'user_id': user['user_id']},
            {'$set': {'stats.last_activity': datetime.now()}}
        )

        # Générer les tokens
        tokens = generate_tokens(user['user_id'])

        return jsonify({
            'success': True,
            'message': 'Connexion réussie',
            'user': {
                'user_id': user['user_id'],
                'profile': user['profile'],
                'farmer_info': user['farmer_info'],
                'subscription': user['subscription'],
                'stats': user['stats']
            },
            'tokens': tokens
        })

    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {e}")
        return jsonify({'error': 'Erreur lors de la connexion'}), 500


@app.route('/api/auth/refresh', methods=['POST'])
def refresh_token():
    """Rafraîchir le token d'accès"""
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            return jsonify({'error': 'Refresh token requis'}), 400

        try:
            # Décoder le refresh token
            payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=['HS256'])

            # Vérifier que c'est un refresh token
            if payload.get('type') != 'refresh':
                return jsonify({'error': 'Type de token invalide'}), 401

            user_id = payload['user_id']

            # Vérifier que l'utilisateur existe
            user_service = UserService(classifier.db_manager)
            user = user_service.get_user(user_id)

            if not user:
                return jsonify({'error': 'Utilisateur non trouvé'}), 401

            # Générer de nouveaux tokens
            tokens = generate_tokens(user_id)

            return jsonify({
                'success': True,
                'tokens': tokens
            })

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Refresh token expiré'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Refresh token invalide'}), 401

    except Exception as e:
        logger.error(f"Erreur lors du rafraîchissement: {e}")
        return jsonify({'error': 'Erreur lors du rafraîchissement'}), 500


@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout():
    """Déconnexion (invalide les tokens côté client)"""
    try:
        # Dans une implémentation complète, vous pourriez ajouter
        # les tokens à une blacklist stockée en base

        return jsonify({
            'success': True,
            'message': 'Déconnexion réussie'
        })

    except Exception as e:
        logger.error(f"Erreur lors de la déconnexion: {e}")
        return jsonify({'error': 'Erreur lors de la déconnexion'}), 500


@app.route('/api/auth/profile', methods=['GET'])
@token_required
def get_profile():
    """Récupérer le profil de l'utilisateur connecté"""
    try:
        user = request.current_user

        return jsonify({
            'success': True,
            'user': {
                'user_id': user['user_id'],
                'profile': user['profile'],
                'farmer_info': user['farmer_info'],
                'subscription': user['subscription'],
                'preferences': user['preferences'],
                'stats': user['stats']
            }
        })

    except Exception as e:
        logger.error(f"Erreur lors de la récupération du profil: {e}")
        return jsonify({'error': 'Erreur lors de la récupération du profil'}), 500


@app.route('/api/auth/profile', methods=['PUT'])
@token_required
def update_profile():
    """Mettre à jour le profil de l'utilisateur"""
    try:
        user = request.current_user
        data = request.get_json()

        # Préparer les données de mise à jour
        update_data = {}

        # Mettre à jour le profil
        if 'profile' in data:
            for key, value in data['profile'].items():
                if key in ['first_name', 'last_name', 'phone', 'avatar_url', 'language', 'country', 'region', 'city']:
                    update_data[f'profile.{key}'] = value

        # Mettre à jour les informations d'agriculteur
        if 'farmer_info' in data:
            for key, value in data['farmer_info'].items():
                if key in ['experience_years', 'farm_size_hectares', 'primary_crops', 'farming_type', 'certifications']:
                    update_data[f'farmer_info.{key}'] = value

        # Mettre à jour les préférences
        if 'preferences' in data:
            for key, value in data['preferences'].items():
                if key in ['notification_settings', 'language', 'timezone']:
                    update_data[f'preferences.{key}'] = value

        # Ajouter la date de mise à jour
        update_data['updated_at'] = datetime.now()

        # Effectuer la mise à jour
        if classifier.db_manager.use_mongodb:
            result = classifier.db_manager.db.users.update_one(
                {'user_id': user['user_id']},
                {'$set': update_data}
            )

            if result.modified_count > 0:
                # Récupérer l'utilisateur mis à jour
                updated_user = classifier.db_manager.db.users.find_one({'user_id': user['user_id']})

                return jsonify({
                    'success': True,
                    'message': 'Profil mis à jour avec succès',
                    'user': {
                        'user_id': updated_user['user_id'],
                        'profile': updated_user['profile'],
                        'farmer_info': updated_user['farmer_info'],
                        'subscription': updated_user['subscription'],
                        'preferences': updated_user['preferences'],
                        'stats': updated_user['stats']
                    }
                })
            else:
                return jsonify({'error': 'Aucune modification effectuée'}), 400
        else:
            return jsonify({'error': 'MongoDB requis pour cette opération'}), 503

    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour du profil: {e}")
        return jsonify({'error': 'Erreur lors de la mise à jour du profil'}), 500


@app.route('/api/auth/change-password', methods=['POST'])
@token_required
def change_password():
    """Changer le mot de passe de l'utilisateur"""
    try:
        user = request.current_user
        data = request.get_json()

        # Validation des données requises
        required_fields = ['current_password', 'new_password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ {field} est requis'}), 400

        # Vérifier le mot de passe actuel
        if not verify_password(data['current_password'], user['password_hash']):
            return jsonify({'error': 'Mot de passe actuel incorrect'}), 401

        # Valider le nouveau mot de passe
        password_validation = validate_password(data['new_password'])
        if not password_validation['is_valid']:
            return jsonify({
                'error': 'Nouveau mot de passe invalide',
                'details': password_validation['errors']
            }), 400

        # Hasher le nouveau mot de passe
        new_password_hash = hash_password(data['new_password'])

        # Mettre à jour le mot de passe
        if classifier.db_manager.use_mongodb:
            result = classifier.db_manager.db.users.update_one(
                {'user_id': user['user_id']},
                {'$set': {
                    'password_hash': new_password_hash,
                    'updated_at': datetime.now()
                }}
            )

            if result.modified_count > 0:
                return jsonify({
                    'success': True,
                    'message': 'Mot de passe modifié avec succès'
                })
            else:
                return jsonify({'error': 'Échec de la modification du mot de passe'}), 500
        else:
            return jsonify({'error': 'MongoDB requis pour cette opération'}), 503

    except Exception as e:
        logger.error(f"Erreur lors du changement de mot de passe: {e}")
        return jsonify({'error': 'Erreur lors du changement de mot de passe'}), 500


@app.route('/api/auth/delete-account', methods=['DELETE'])
@token_required
def delete_account():
    """Supprimer le compte utilisateur"""
    try:
        user = request.current_user
        data = request.get_json()

        # Vérifier le mot de passe pour confirmation
        if not data.get('password'):
            return jsonify({'error': 'Mot de passe requis pour la suppression'}), 400

        if not verify_password(data['password'], user['password_hash']):
            return jsonify({'error': 'Mot de passe incorrect'}), 401

        # Marquer l'utilisateur comme inactif au lieu de le supprimer
        if classifier.db_manager.use_mongodb:
            result = classifier.db_manager.db.users.update_one(
                {'user_id': user['user_id']},
                {'$set': {
                    'is_active': False,
                    'deleted_at': datetime.now(),
                    'updated_at': datetime.now()
                }}
            )

            if result.modified_count > 0:
                return jsonify({
                    'success': True,
                    'message': 'Compte supprimé avec succès'
                })
            else:
                return jsonify({'error': 'Échec de la suppression du compte'}), 500
        else:
            return jsonify({'error': 'MongoDB requis pour cette opération'}), 503

    except Exception as e:
        logger.error(f"Erreur lors de la suppression du compte: {e}")
        return jsonify({'error': 'Erreur lors de la suppression du compte'}), 500

# ========================================
# MIDDLEWARE ET HANDLERS D'ERREUR
# ========================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erreur interne: {error}")
    return jsonify({"error": "Internal server error"}), 500

# ========================================
# API ROUTES (préfixées par /api)
# ========================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérifier l'état de l'API et du modèle"""
    model_info = classifier.get_model_info()

    return jsonify({
        "status": "healthy",
        "model_loaded": model_info['model_loaded'],
        "classes_supported": model_info['classes_supported'],
        "diseases_in_db": model_info['diseases_in_db'],
        "database_source": model_info['database_source'],
        "mongodb_available": model_info['database_source'] == 'mongodb'
    })





@app.route('/api/classify', methods=['POST'])
def classify_disease():
    """Endpoint principal pour classifier une image avec sauvegarde permanente"""
    try:
        # Récupérer l'utilisateur connecté de manière optionnelle
        user_id = request.form.get('user_id')
        # print(request.body)

        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400

        if file and allowed_file(file.filename):
            # Générer un ID unique pour cette prédiction
            prediction_id = str(uuid.uuid4())

            # Sauvegarder l'image temporairement
            temp_filename = secure_filename(f"temp_{prediction_id}_{file.filename}")
            temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
            file.save(temp_filepath)

            try:
                # Traiter l'image
                processed_img = process_image(temp_filepath)

                # Classifier l'image
                result = classifier.classify(processed_img)

                if not result["success"]:
                    # Supprimer le fichier temporaire en cas d'erreur
                    if os.path.exists(temp_filepath):
                        os.remove(temp_filepath)
                    return jsonify({"error": result.get("error", "Classification failed")}), 500

                # Sauvegarder l'image de manière permanente
                save_result = save_image_permanently(temp_filepath, file.filename)

                if not save_result["success"]:
                    logger.warning(f"Échec de la sauvegarde permanente: {save_result.get('error')}")

                # Préparer les données de la prédiction
                classification = result["classification"]
                disease_info = result.get("disease_info", {})

                # Créer l'enregistrement de prédiction avec user_id
                prediction_record = {
                    "prediction_id": prediction_id,
                    "user_id": user_id,  # Ajout du user_id
                    "timestamp": result["timestamp"],
                    "original_filename": file.filename,
                    "processed_filename": save_result.get("permanent_filename"),
                    "image_path": save_result.get("relative_path"),
                    "file_size": os.path.getsize(temp_filepath),
                    "classification": {
                        "predicted_class": classification["predicted_class"],
                        "class_id": classification["class_id"],
                        "confidence": float(f"{float(str(classification['confidence'])):.2f}"),
                        "confidence_percentage": float(f"{float(str(classification['confidence_percentage'])):.2f}"),
                        "severity": get_severity_level(classification["confidence"]),
                        "top5_predictions": classification.get("top5_predictions", [])
                    },
                    "disease_info": disease_info,
                    "database_source": classifier.db_manager.use_mongodb and "mongodb" or "json",
                    "metadata": {
                        "user_agent": request.headers.get('User-Agent'),
                        "client_ip": request.remote_addr,
                        "image_saved": save_result["success"],
                        "authenticated": user_id not in 'unknow'
                    }
                }

                # Sauvegarder l'enregistrement de prédiction
                json_save_result = save_prediction_record(prediction_record)
                mongodb_save_result = save_to_database_if_available(prediction_record)

                # Formater la réponse finale
                response = {
                    "success": True,
                    "prediction_id": prediction_id,
                    "timestamp": result["timestamp"],
                    "classification": {
                        "predicted_class": classification["predicted_class"],
                        "class_id": classification["class_id"],
                        "confidence": float(f"{float(str(classification['confidence'])):.2f}"),
                        "confidence_percentage": float(f"{float(str(classification['confidence_percentage'])):.2f}"),
                        "severity": get_severity_level(classification["confidence"]),
                        "top5_predictions": classification.get("top5_predictions", [])
                    },
                    "database_source": classifier.db_manager.use_mongodb and "mongodb" or "json",
                    "storage_info": {
                        "image_saved": save_result["success"],
                        "prediction_logged": json_save_result["success"],
                        "mongodb_saved": mongodb_save_result["success"]
                    }
                }

                # Ajouter les informations détaillées sur la maladie/état
                if disease_info:
                    response["disease_info"] = {
                        "category": disease_info["category"],
                        "name": disease_info["name"],
                        "scientific_name": disease_info.get("scientific_name", ""),
                        "description": disease_info["description"],
                        "urgency": disease_info["urgency"],
                        "symptoms": disease_info["symptoms"],
                        "crops_affected": disease_info["crops"],
                        "impact": disease_info.get("impact", ""),
                        "geographic_distribution": disease_info.get("geographic_distribution", "")
                    }

                    # Informations spécifiques aux maladies
                    if disease_info["category"] == "disease":
                        response["disease_info"].update({
                            "pathogens": disease_info.get("pathogens", []),
                            "vectors": disease_info.get("vectors", []),
                            "prevention_measures": disease_info.get("prevention_measures", [])
                        })

                        # Obtenir les traitements recommandés
                        treatments = classifier.get_treatment_recommendations(
                            classification["predicted_class"]
                        )
                        response["disease_info"]["treatment_recommendations"] = treatments

                    # Informations pour état sain
                    elif disease_info["category"] == "healthy_state":
                        response["disease_info"]["recommendations"] = disease_info.get("recommendations", [])

                return jsonify(response)

            finally:
                # Supprimer le fichier temporaire
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)

        else:
            return jsonify({"error": "Invalid file type"}), 400

    except Exception as e:
        logger.error(f"Erreur lors de la classification: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/classify/batch', methods=['POST'])
def classify_batch():
    """Endpoint pour classifier plusieurs images avec sauvegarde permanente"""
    try:
        # Récupérer l'utilisateur connecté de manière optionnelle
        user_id = request.form.get('user_id')
        # print(user_id)

        if 'images' not in request.files:
            return jsonify({"error": "No images provided"}), 400

        files = request.files.getlist('images')
        if not files:
            return jsonify({"error": "No images selected"}), 400

        # Limiter le nombre d'images
        max_images = 10
        if len(files) > max_images:
            return jsonify({"error": f"Maximum {max_images} images allowed"}), 400

        batch_id = str(uuid.uuid4())
        results = []
        temp_filepaths = []

        try:
            # Sauvegarder toutes les images temporairement
            for i, file in enumerate(files):
                if file and allowed_file(file.filename):
                    temp_filename = secure_filename(f"batch_{batch_id}_{i}_{file.filename}")
                    temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
                    file.save(temp_filepath)
                    temp_filepaths.append(temp_filepath)

            # Traiter et classifier toutes les images
            for i, (temp_filepath, file) in enumerate(zip(temp_filepaths, files)):
                prediction_id = f"{batch_id}_{i}"

                try:
                    # Traiter l'image
                    processed_img = process_image(temp_filepath)

                    # Classifier
                    classification = classifier.classify(processed_img)

                    if classification["success"]:
                        # Sauvegarder l'image de manière permanente
                        save_result = save_image_permanently(temp_filepath, file.filename)

                        # Créer l'enregistrement de prédiction avec user_id
                        prediction_record = {
                            "prediction_id": prediction_id,
                            "user_id": user_id,  # Ajout du user_id
                            "batch_id": batch_id,
                            "image_index": i,
                            "timestamp": classification["timestamp"],
                            "original_filename": file.filename,
                            "processed_filename": save_result.get("permanent_filename"),
                            "image_path": save_result.get("relative_path"),
                            "file_size": os.path.getsize(temp_filepath),
                            "classification": classification["classification"],
                            "disease_info": classification.get("disease_info", {}),
                            "database_source": classifier.db_manager.use_mongodb and "mongodb" or "json",
                            "metadata": {
                                "user_agent": request.headers.get('User-Agent'),
                                "client_ip": request.remote_addr,
                                "image_saved": save_result["success"],
                                "batch_processing": True,
                                "authenticated": user_id not in 'unknown'
                            }
                        }

                        # Sauvegarder l'enregistrement
                        json_save_result = save_prediction_record(prediction_record)
                        mongodb_save_result = save_to_database_if_available(prediction_record)

                        result = {
                            "image_index": i,
                            "prediction_id": prediction_id,
                            "filename": file.filename,
                            "success": True,
                            "classification": {
                                "predicted_class": classification["classification"]["predicted_class"],
                                "class_id": classification["classification"]["class_id"],
                                "confidence": float(f"{float(str(classification['classification']['confidence'])):.2f}"),
                                "confidence_percentage": float(f"{float(str(classification['classification']['confidence_percentage'])):.2f}"),
                                "severity": get_severity_level(classification["classification"]["confidence"])
                            },
                            "disease_info": classification.get("disease_info", {}),
                            "storage_info": {
                                "image_saved": save_result["success"],
                                "prediction_logged": json_save_result["success"],
                                "mongodb_saved": mongodb_save_result["success"]
                            }
                        }
                    else:
                        result = {
                            "image_index": i,
                            "prediction_id": prediction_id,
                            "filename": file.filename,
                            "success": False,
                            "error": classification.get("error", "Classification failed")
                        }

                    results.append(result)

                except Exception as e:
                    results.append({
                        "image_index": i,
                        "prediction_id": prediction_id,
                        "filename": file.filename,
                        "success": False,
                        "error": str(e)
                    })

            return jsonify({
                "success": True,
                "batch_id": batch_id,
                "total_images": len(files),
                "processed_images": len(results),
                "successful_predictions": len([r for r in results if r["success"]]),
                "results": results,
                "timestamp": datetime.now().isoformat()
            })

        finally:
            # Nettoyer tous les fichiers temporaires
            for temp_filepath in temp_filepaths:
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)

    except Exception as e:
        logger.error(f"Erreur lors de la classification batch: {e}")
        return jsonify({"error": str(e)}), 500
# ========================================
# ENDPOINTS POUR LA BASE DE DONNÉES
# ========================================

@app.route('/api/diseases', methods=['GET'])
def get_all_diseases():
    """Obtenir la liste de toutes les maladies"""
    try:
        diseases = classifier.get_diseases_database()
        return jsonify(diseases)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des maladies: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/diseases/<disease_class>', methods=['GET'])
def get_disease_details(disease_class):
    """Obtenir les détails d'une maladie spécifique"""
    try:
        disease_info = classifier.get_disease_info(disease_class)

        if disease_info:
            return jsonify({
                "success": True,
                "disease_class": disease_class,
                "disease_info": disease_info,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Maladie '{disease_class}' non trouvée"
            }), 404

    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la maladie {disease_class}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/diseases/<disease_class>/treatments', methods=['GET'])
def get_disease_treatments(disease_class):
    """Obtenir les traitements pour une maladie spécifique"""
    try:
        urgency_filter = request.args.get('urgency', None)
        treatments = classifier.get_treatment_recommendations(disease_class, urgency_filter)

        return jsonify({
            "success": True,
            "disease_class": disease_class,
            "urgency_filter": urgency_filter,
            "treatments": treatments,
            "total_treatments": len(treatments),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des traitements pour {disease_class}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/diseases/<disease_class>/vectors', methods=['GET'])
def get_disease_vectors(disease_class):
    """Obtenir les vecteurs pour une maladie spécifique"""
    try:
        vectors = classifier.get_vector_info(disease_class)

        return jsonify({
            "success": True,
            "disease_class": disease_class,
            "vectors": vectors,
            "total_vectors": len(vectors),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des vecteurs pour {disease_class}: {e}")
        return jsonify({"error": str(e)}), 500

# ========================================
# ENDPOINTS POUR LES STATISTIQUES
# ========================================

@app.route('/api/stats/model', methods=['GET'])
def get_model_stats():
    """Obtenir les statistiques du modèle"""
    try:
        model_info = classifier.get_model_info()

        return jsonify({
            "success": True,
            "model_stats": {
                "model_loaded": model_info['model_loaded'],
                "total_classes": len(model_info['classes_supported']),
                "supported_classes": model_info['classes_supported'],
                "diseases_in_database": model_info['diseases_in_db'],
                "database_source": model_info['database_source'],
                "mongodb_available": model_info['database_source'] == 'mongodb'
            },
            "metadata": model_info.get('metadata', {}),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats du modèle: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats/database', methods=['GET'])
def get_database_stats():
    """Obtenir les statistiques de la base de données"""
    try:
        diseases_db = classifier.get_diseases_database()

        # Analyser les données
        stats = {
            "total_entries": diseases_db.get('total', 0),
            "database_source": diseases_db.get('source', 'unknown'),
            "categories": {},
            "urgency_levels": {},
            "crops_affected": {}
        }

        # Analyser les maladies
        diseases_data = diseases_db.get('diseases', {})

        # Pour MongoDB, les données sont déjà formatées
        if diseases_db.get('source') == 'mongodb':
            for disease_class, disease_info in diseases_data.items():
                category = disease_info.get('category', 'unknown')
                urgency = disease_info.get('urgency', 'unknown')
                crops = disease_info.get('crops', [])

                # Compter les catégories
                stats['categories'][category] = stats['categories'].get(category, 0) + 1

                # Compter les niveaux d'urgence
                stats['urgency_levels'][urgency] = stats['urgency_levels'].get(urgency, 0) + 1

                # Compter les cultures affectées
                for crop in crops:
                    stats['crops_affected'][crop] = stats['crops_affected'].get(crop, 0) + 1

        # Pour JSON, analyser la structure
        elif diseases_db.get('source') == 'json':
            raw_data = diseases_data

            # Analyser les différentes sections
            for section_name, section_data in raw_data.items():
                if isinstance(section_data, dict):
                    stats['categories'][section_name] = len(section_data)

        return jsonify({
            "success": True,
            "database_stats": stats,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats de la base: {e}")
        return jsonify({"error": str(e)}), 500

# ========================================
# ENDPOINTS POUR LES UTILITAIRES
# ========================================

@app.route('/api/classes', methods=['GET'])
def get_supported_classes():
    """Obtenir la liste des classes supportées"""
    try:
        classes = classifier.get_model_info()['classes_supported']

        return jsonify({
            "success": True,
            "supported_classes": classes,
            "total_classes": len(classes),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des classes: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_diseases():
    """Rechercher des maladies par nom ou symptômes"""
    try:
        query = request.args.get('q', '').lower()
        category = request.args.get('category', None)

        if not query:
            return jsonify({"error": "Paramètre de recherche 'q' requis"}), 400

        # Obtenir toutes les maladies
        diseases_db = classifier.get_diseases_database()
        diseases_data = diseases_db.get('diseases', {})

        results = []

        # Rechercher dans les données
        for disease_class, disease_info in diseases_data.items():
            if isinstance(disease_info, dict):
                # Rechercher dans le nom
                name = disease_info.get('name', '').lower()
                description = disease_info.get('description', '').lower()
                symptoms = str(disease_info.get('symptoms', [])).lower()

                # Vérifier si la requête correspond
                if (query in name or query in description or query in symptoms):
                    # Filtrer par catégorie si spécifiée
                    if category and disease_info.get('category') != category:
                        continue

                    results.append({
                        "disease_class": disease_class,
                        "name": disease_info.get('name', ''),
                        "category": disease_info.get('category', ''),
                        "description": disease_info.get('description', '')[:200] + "..." if len(disease_info.get('description', '')) > 200 else disease_info.get('description', ''),
                        "urgency": disease_info.get('urgency', ''),
                        "relevance_score": calculate_relevance_score(query, disease_info)
                    })

        # Trier par score de pertinence
        results.sort(key=lambda x: x['relevance_score'], reverse=True)

        return jsonify({
            "success": True,
            "query": query,
            "category_filter": category,
            "total_results": len(results),
            "results": results[:20],  # Limiter à 20 résultats
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/predictions/history', methods=['GET'])
def get_predictions_history():
    """Obtenir l'historique des prédictions"""
    try:
        # Paramètres de requête
        date = request.args.get('date')  # Format: YYYY-MM-DD
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))

        if date:
            # Charger les prédictions d'une date spécifique
            log_file = os.path.join(PREDICTIONS_LOG, "daily", f"predictions_{date}.json")

            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                predictions = data.get("predictions", [])
                total = len(predictions)

                # Appliquer pagination
                paginated_predictions = predictions[offset:offset + limit]

                return jsonify({
                    "success": True,
                    "date": date,
                    "total_predictions": total,
                    "returned_predictions": len(paginated_predictions),
                    "offset": offset,
                    "limit": limit,
                    "predictions": paginated_predictions
                })
            else:
                return jsonify({
                    "success": True,
                    "date": date,
                    "total_predictions": 0,
                    "predictions": []
                })

        else:
            # Charger depuis le fichier global
            global_log = os.path.join(PREDICTIONS_LOG, "all_predictions.json")

            if os.path.exists(global_log):
                with open(global_log, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                predictions = data.get("predictions", [])
                total = len(predictions)

                # Trier par timestamp décroissant
                predictions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

                # Appliquer pagination
                paginated_predictions = predictions[offset:offset + limit]

                return jsonify({
                    "success": True,
                    "total_predictions": total,
                    "returned_predictions": len(paginated_predictions),
                    "offset": offset,
                    "limit": limit,
                    "predictions": paginated_predictions
                })
            else:
                return jsonify({
                    "success": True,
                    "total_predictions": 0,
                    "predictions": []
                })

    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'historique: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/predictions/<prediction_id>', methods=['GET'])
def get_prediction_details(prediction_id):
    """Obtenir les détails d'une prédiction spécifique"""
    try:
        # Chercher dans le fichier global
        global_log = os.path.join(PREDICTIONS_LOG, "all_predictions.json")

        if os.path.exists(global_log):
            with open(global_log, 'r', encoding='utf-8') as f:
                data = json.load(f)

            predictions = data.get("predictions", [])

            # Trouver la prédiction
            prediction = next((p for p in predictions if p.get("prediction_id") == prediction_id), None)

            if prediction:
                return jsonify({
                    "success": True,
                    "prediction": prediction
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Prédiction non trouvée"
                }), 404
        else:
            return jsonify({
                "success": False,
                "error": "Aucun historique disponible"
            }), 404

    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la prédiction {prediction_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/predictions/stats', methods=['GET'])
def get_predictions_stats():
    """Obtenir les statistiques des prédictions"""
    try:
        global_log = os.path.join(PREDICTIONS_LOG, "all_predictions.json")

        if os.path.exists(global_log):
            with open(global_log, 'r', encoding='utf-8') as f:
                data = json.load(f)

            predictions = data.get("predictions", [])

            # Calculer les statistiques
            stats = {
                "total_predictions": len(predictions),
                "predictions_by_class": {},
                "predictions_by_date": {},
                "average_confidence": 0,
                "confidence_distribution": {
                    "très_élevé": 0,
                    "élevé": 0,
                    "modéré": 0,
                    "faible": 0
                }
            }

            if predictions:
                confidences = []

                for prediction in predictions:
                    # Compter par classe
                    predicted_class = prediction.get("classification", {}).get("predicted_class", "unknown")
                    stats["predictions_by_class"][predicted_class] = stats["predictions_by_class"].get(predicted_class,
                                                                                                       0) + 1

                    # Compter par date
                    date = prediction.get("timestamp", "")[:10]  # YYYY-MM-DD
                    stats["predictions_by_date"][date] = stats["predictions_by_date"].get(date, 0) + 1

                    # Confiance
                    confidence = prediction.get("classification", {}).get("confidence", 0)
                    confidences.append(confidence)

                    # Distribution de confiance
                    severity = get_severity_level(confidence)
                    stats["confidence_distribution"][severity] = stats["confidence_distribution"].get(severity, 0) + 1

                # Moyenne de confiance
                stats["average_confidence"] = sum(confidences) / len(confidences) if confidences else 0

            return jsonify({
                "success": True,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": True,
                "stats": {
                    "total_predictions": 0,
                    "predictions_by_class": {},
                    "predictions_by_date": {},
                    "average_confidence": 0,
                    "confidence_distribution": {
                        "très_élevé": 0,
                        "élevé": 0,
                        "modéré": 0,
                        "faible": 0
                    }
                }
            })

    except Exception as e:
        logger.error(f"Erreur lors du calcul des statistiques: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/images/<path:image_path>', methods=['GET'])
def serve_saved_image(image_path):
    """Servir une image sauvegardée"""
    try:
        full_path = os.path.join(PERMANENT_STORAGE, image_path)

        if os.path.exists(full_path):
            return send_file(full_path)
        else:
            return jsonify({"error": "Image non trouvée"}), 404

    except Exception as e:
        logger.error(f"Erreur lors du service d'image: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Créer les dossiers nécessaires
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Vérifier si le modèle et la base de données sont disponibles
    if not os.path.exists('weights/best.pt'):
        print("⚠️  Modèle YOLO non trouvé!")
        print("   Placez le modèle dans: weights/best.pt")

    if not os.path.exists('data/diseases_database.json'):
        print("⚠️  Base de données des maladies non trouvée!")
        print("   Placez la base de données dans: data/diseases_database.json")

    # Vérifier si le frontend existe
    if not os.path.exists(app.config['FRONTEND_DIST_DIR']):
        print("⚠️  Frontend build non trouvé!")
        print(f"   Chemin attendu: {app.config['FRONTEND_DIST_DIR']}")
        print("   Exécutez: cd ../agriguard-frontend && npm run build")
    else:
        print("✅ Frontend build trouvé")

    print("🚀 Démarrage du serveur AgriGuard avec sauvegarde permanente...")
    print(f"📊 Modèle: {classifier.get_model_info()['model_loaded']}")
    print(f"💾 Base de données: {classifier.db_manager.use_mongodb and 'MongoDB' or 'JSON'}")
    print(f"🔢 Classes supportées: {len(classifier.get_model_info()['classes_supported'])}")
    print(f"📁 Stockage permanent: {PERMANENT_STORAGE}")
    print(f"📋 Logs de prédictions: {PREDICTIONS_LOG}")



    app.run(debug=True, host='0.0.0.0', port=3000)