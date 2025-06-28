from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from models.yolo_model import PestDetector
from utils.image_processing import process_image
import uuid

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialiser le modèle
detector = PestDetector()

# Charger la base de données des ravageurs
with open('data/pest_database.json', 'r', encoding='utf-8') as f:
    pest_db = json.load(f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": detector.model_loaded})

@app.route('/api/detect', methods=['POST'])
def detect_pest():
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

            # Traiter l'image
            processed_img = process_image(filepath)

            # Détecter les ravageurs
            detections = detector.detect(processed_img)

            # Enrichir avec info database
            results = []
            for detection in detections:
                pest_info = pest_db.get(detection['class'], {})
                result = {
                    "pest_name": detection['class'],
                    "confidence": detection['confidence'],
                    "bbox": detection['bbox'],
                    "severity": get_severity(detection['confidence']),
                    "description": pest_info.get('description', ''),
                    "treatment": pest_info.get('treatment', []),
                    "urgency": pest_info.get('urgency', 'medium')
                }
                results.append(result)

            # Nettoyer le fichier uploadé
            os.remove(filepath)

            return jsonify({
                "success": True,
                "detections": results,
                "total_pests": len(results)
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_severity(confidence):
    if confidence > 0.8:
        return "high"
    elif confidence > 0.6:
        return "medium"
    else:
        return "low"

@app.route('/api/pests', methods=['GET'])
def get_pest_database():
    return jsonify(pest_db)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=3000)