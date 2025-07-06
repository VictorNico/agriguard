from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from models.yolo_model_cls import MaizeDiseaseClassifier  # Importé du fichier précédent
from utils.image_processing import process_image
import uuid

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuration pour servir le frontend Nuxt
FRONTEND_DIST_DIR = '../corn-disease-app/.output/public'  # Chemin vers build Nuxt
app.config['FRONTEND_DIST_DIR'] = FRONTEND_DIST_DIR

# Initialiser le classificateur de maladies du maïs
classifier = MaizeDiseaseClassifier('weights/best.pt', 'data/diseases_database.json')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        "diseases_in_db": model_info['diseases_in_db']
    })

@app.route('/api/classify', methods=['POST'])
def classify_disease():
    """Endpoint principal pour classifier une image de maladie du maïs"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400

        if file and allowed_file(file.filename):
            # Sauvegarder l'image
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                # Traiter l'image
                processed_img = process_image(filepath)

                # Classifier l'image
                result = classifier.classify(processed_img)

                if not result["success"]:
                    return jsonify({"error": result.get("error", "Classification failed")}), 500

                # Enrichir la réponse avec des informations formatées
                classification = result["classification"]
                disease_info = result.get("disease_info", {})

                # Formater la réponse finale
                response = {
                    "success": True,
                    "timestamp": result["timestamp"],
                    "classification": {
                        "predicted_class": classification["predicted_class"],
                        "class_id": classification["class_id"],
                        "confidence": classification["confidence"],
                        "confidence_percentage": classification["confidence_percentage"],
                        "severity": get_severity_level(classification["confidence"]),
                        "top5_predictions": classification.get("top5_predictions", [])
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
                # Nettoyer le fichier uploadé
                if os.path.exists(filepath):
                    os.remove(filepath)

        else:
            return jsonify({"error": "Invalid file type"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/classify/batch', methods=['POST'])
def classify_batch():
    """Endpoint pour classifier plusieurs images en une fois"""
    try:
        if 'images' not in request.files:
            return jsonify({"error": "No images provided"}), 400

        files = request.files.getlist('images')
        if not files:
            return jsonify({"error": "No images selected"}), 400

        # Limiter le nombre d'images (pour éviter surcharge)
        max_images = 10
        if len(files) > max_images:
            return jsonify({"error": f"Maximum {max_images} images allowed"}), 400

        results = []
        filepaths = []

        try:
            # Sauvegarder toutes les images
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    filepaths.append(filepath)

            # Traiter et classifier toutes les images
            processed_images = [process_image(fp) for fp in filepaths]
            classifications = classifier.classify_batch(processed_images)

            # Enrichir chaque résultat
            for i, classification in enumerate(classifications):
                if classification["success"]:
                    result = {
                        "image_index": i,
                        "filename": files[i].filename if i < len(files) else f"image_{i}",
                        "success": True,
                        "classification": {
                            "predicted_class": classification["classification"]["predicted_class"],
                            "class_id": classification["classification"]["class_id"],
                            "confidence": classification["classification"]["confidence"],
                            "confidence_percentage": classification["classification"]["confidence_percentage"],
                            "severity": get_severity_level(classification["classification"]["confidence"])
                        }
                    }

                    # Ajouter les informations de base sur la maladie
                    if "disease_info" in classification:
                        disease_info = classification["disease_info"]
                        result["disease_info"] = {
                            "name": disease_info["name"],
                            "urgency": disease_info["urgency"],
                            "category": disease_info["category"],
                            "description": disease_info["description"]
                        }
                else:
                    result = {
                        "image_index": i,
                        "filename": files[i].filename if i < len(files) else f"image_{i}",
                        "success": False,
                        "error": classification.get("error", "Classification failed")
                    }

                results.append(result)

        finally:
            # Nettoyer tous les fichiers uploadés
            for filepath in filepaths:
                if os.path.exists(filepath):
                    os.remove(filepath)

        return jsonify({
            "success": True,
            "results": results,
            "total_images": len(files),
            "successful_classifications": len([r for r in results if r.get("success", False)])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/disease/<disease_class>', methods=['GET'])
def get_disease_info(disease_class):
    """Obtenir des informations détaillées sur une maladie spécifique"""
    try:
        disease_info = classifier.get_disease_info(disease_class)

        if not disease_info:
            return jsonify({"error": f"Disease class '{disease_class}' not found"}), 404

        # Ajouter les recommandations de traitement
        if disease_info["category"] == "disease":
            treatments = classifier.get_treatment_recommendations(disease_class)
            disease_info["treatment_recommendations"] = treatments

            # Informations sur les vecteurs
            vectors = classifier.get_vector_info(disease_class)
            disease_info["vectors"] = vectors

        return jsonify({
            "success": True,
            "disease_class": disease_class,
            "info": disease_info
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/treatment/<disease_class>', methods=['GET'])
def get_treatment_recommendations(disease_class):
    """Obtenir les recommandations de traitement pour une maladie"""
    try:
        # Paramètres optionnels
        urgency_filter = request.args.get('urgency')  # critical, high, medium, low
        treatment_type = request.args.get('type')  # preventif, chimique, biologique

        treatments = classifier.get_treatment_recommendations(disease_class, urgency_filter)

        if treatment_type:
            treatments = [t for t in treatments if t.get("type") == treatment_type]

        if not treatments:
            return jsonify({
                "success": True,
                "disease_class": disease_class,
                "treatments": [],
                "message": "No treatments found for the specified criteria"
            })

        return jsonify({
            "success": True,
            "disease_class": disease_class,
            "treatments": treatments,
            "filters_applied": {
                "urgency": urgency_filter,
                "type": treatment_type
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/vectors/<disease_class>', methods=['GET'])
def get_vector_info(disease_class):
    """Obtenir les informations sur les vecteurs d'une maladie"""
    try:
        vectors = classifier.get_vector_info(disease_class)

        if not vectors:
            return jsonify({
                "success": True,
                "disease_class": disease_class,
                "vectors": [],
                "message": "No vector information available"
            })

        return jsonify({
            "success": True,
            "disease_class": disease_class,
            "vectors": vectors
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/diseases', methods=['GET'])
def get_diseases_database():
    """Obtenir la base de données complète des maladies"""
    try:
        model_info = classifier.get_model_info()

        return jsonify({
            "success": True,
            "diseases": model_info["diseases_in_db"],
            "classes_supported": model_info["classes_supported"],
            "metadata": model_info["metadata"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/diseases/list', methods=['GET'])
def get_diseases_list():
    """Obtenir la liste des maladies supportées avec informations de base"""
    try:
        model_info = classifier.get_model_info()
        diseases_list = []

        for disease_class in model_info["classes_supported"]:
            disease_info = classifier.get_disease_info(disease_class)

            if disease_info:
                diseases_list.append({
                    "class": disease_class,
                    "name": disease_info["name"],
                    "scientific_name": disease_info.get("scientific_name", ""),
                    "urgency": disease_info["urgency"],
                    "category": disease_info["category"],
                    "crops": disease_info["crops"],
                    "description": disease_info["description"][:200] + "..." if len(disease_info["description"]) > 200 else disease_info["description"]
                })

        return jsonify({
            "success": True,
            "diseases": diseases_list,
            "total": len(diseases_list)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_classification_stats():
    """Statistiques du modèle et de l'API"""
    try:
        model_info = classifier.get_model_info()

        stats = {
            "model_info": model_info,
            "api_config": {
                "upload_folder": app.config['UPLOAD_FOLDER'],
                "allowed_extensions": list(ALLOWED_EXTENSIONS),
                "max_batch_size": 10
            },
            "database_stats": {
                "total_diseases": len(model_info.get("diseases_in_db", [])),
                "total_classes": len(model_info.get("classes_supported", [])),
                "metadata": model_info.get("metadata", {})
            }
        }

        return jsonify({
            "success": True,
            "stats": stats
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

# ========================================
# COMPATIBILITY ENDPOINTS (pour compatibilité avec l'ancien système)
# ========================================

@app.route('/api/detect', methods=['POST'])
def detect_compatibility():
    """Endpoint de compatibilité (redirige vers classify)"""
    return classify_disease()

@app.route('/api/pest/<pest_name>', methods=['GET'])
def get_pest_info_compatibility(pest_name):
    """Endpoint de compatibilité (redirige vers disease)"""
    return get_disease_info(pest_name)

# ========================================
# FRONTEND STATIC SERVING
# ========================================

@app.route('/')
def serve_index():
    """Servir la page principale du frontend"""
    try:
        return send_file(os.path.join(app.config['FRONTEND_DIST_DIR'], 'index.html'))
    except:
        return "<h1>Frontend non trouvé</h1><p>Veuillez builder le frontend Nuxt avec: <code>npm run build</code></p>", 404

@app.route('/<path:path>')
def serve_static_files(path):
    """Servir tous les fichiers statiques du frontend"""
    try:
        # Vérifier si c'est un fichier statique
        full_path = os.path.join(app.config['FRONTEND_DIST_DIR'], path)

        if os.path.isfile(full_path):
            return send_from_directory(app.config['FRONTEND_DIST_DIR'], path)
        else:
            # Pour les routes SPA, rediriger vers index.html
            return send_file(os.path.join(app.config['FRONTEND_DIST_DIR'], 'index.html'))
    except:
        return jsonify({"error": "File not found"}), 404

# ========================================
# ERROR HANDLERS
# ========================================

@app.errorhandler(404)
def not_found(error):
    """Gérer les 404 - rediriger vers l'app frontend pour les routes SPA"""
    if request.path.startswith('/api/'):
        return jsonify({"error": "API endpoint not found"}), 404
    else:
        # Rediriger vers le frontend pour les routes non-API
        return serve_index()

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({"error": "File too large"}), 413

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

    # Afficher l'état du classificateur
    model_info = classifier.get_model_info()
    print(f"\n📊 État du classificateur:")
    print(f"   Modèle chargé: {model_info['model_loaded']}")
    print(f"   Classes supportées: {model_info['classes_supported']}")
    print(f"   Maladies en base: {model_info['diseases_in_db']}")

    print("\n🚀 API Endpoints disponibles:")
    print("   === Classification ===")
    print("   POST /api/classify - Classifier une image")
    print("   POST /api/classify/batch - Classifier plusieurs images")
    print("   === Informations sur les maladies ===")
    print("   GET  /api/disease/<class> - Info détaillée sur une maladie")
    print("   GET  /api/treatment/<class> - Recommandations de traitement")
    print("   GET  /api/vectors/<class> - Informations sur les vecteurs")
    print("   GET  /api/diseases - Base de données complète")
    print("   GET  /api/diseases/list - Liste des maladies")
    print("   === Système ===")
    print("   GET  /api/stats - Statistiques du modèle")
    print("   GET  /api/health - Santé de l'API")
    print("   === Compatibilité ===")
    print("   POST /api/detect - Alias pour /api/classify")
    print("   GET  /api/pest/<name> - Alias pour /api/disease")

    app.run(debug=True, host='0.0.0.0', port=3000)