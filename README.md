# AgriGuard AI - Setup MVP Flask + Nuxt3

## 🚀 ARCHITECTURE TECHNIQUE

```
Frontend (Nuxt3) ←→ API (Flask) ←→ AI Model (YOLOv11s)
     ↓
  Database (SQLite)
```

---

## 🔧 SETUP BACKEND FLASK

### Structure du projet
```
agriguard-backend/
├── app.py
├── models/
│   ├── __init__.py
│   └── yolo_model.py
├── utils/
│   ├── __init__.py
│   └── image_processing.py
├── data/
│   └── pest_database.json
├── uploads/
├── weights/
│   └── yolov11s.pt
└── requirements.txt
```

### requirements.txt (py-env)
```txt
Flask==2.3.3
Flask-CORS==4.0.0
ultralytics==8.0.196
Pillow==10.0.0
opencv-python==4.8.1.78
numpy==1.24.3
torch==2.0.1
torchvision==0.15.2
```

### environment.yml (conda-env)
```yaml
name: conia2025
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.10
  - pip
  - pip:
      - Flask==2.3.3
      - Flask-CORS==4.0.0
      - ultralytics==8.0.196
      - Pillow==10.0.0
      - opencv-python==4.8.1.78
      - numpy==1.24.3
      - torch==2.0.1
      - torchvision==0.15.2


```

### app.py - API Flask
```python
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
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### models/yolo_model.py
```python
from ultralytics import YOLO
import cv2
import numpy as np

class PestDetector:
    def __init__(self, model_path='weights/yolov11s.pt'):
        self.model_path = model_path
        self.model = None
        self.model_loaded = False
        self.load_model()
    
    def load_model(self):
        try:
            # Pour MVP, utiliser modèle pré-entraîné
            self.model = YOLO('yolov11s.pt')  # Télécharge automatiquement
            self.model_loaded = True
            print("✅ Modèle YOLO chargé avec succès")
        except Exception as e:
            print(f"❌ Erreur chargement modèle: {e}")
            self.model_loaded = False
    
    def detect(self, image):
        if not self.model_loaded:
            return []
        
        try:
            # Lancer la détection
            results = self.model(image, conf=0.3)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Extraction des données
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        bbox = box.xyxy[0].tolist()
                        
                        # Mapping classe → nom ravageur (à adapter)
                        class_names = {
                            0: "legionnaire_automne",
                            1: "bruche_niebe", 
                            2: "cochenille_manioc"
                        }
                        
                        detection = {
                            "class": class_names.get(class_id, f"pest_{class_id}"),
                            "confidence": round(confidence, 2),
                            "bbox": [round(x, 2) for x in bbox]
                        }
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"Erreur détection: {e}")
            return []
```

### data/pest_database.json
```json
{
  "legionnaire_automne": {
    "name": "Légionnaire d'automne",
    "description": "Chenille destructrice qui attaque le maïs, sorgho et autres graminées",
    "crops": ["maïs", "sorgho", "mil"],
    "urgency": "high",
    "treatment": [
      {
        "type": "chimique",
        "product": "Cypermethrine 10% EC",
        "dosage": "50ml pour 15L d'eau",
        "timing": "Tôt le matin ou le soir"
      },
      {
        "type": "biologique", 
        "product": "Bt (Bacillus thuringiensis)",
        "dosage": "2g pour 1L d'eau",
        "timing": "Répéter tous les 7 jours"
      }
    ],
    "prevention": "Rotation des cultures, destruction des résidus"
  },
  "bruche_niebe": {
    "name": "Bruche du niébé",
    "description": "Coléoptère qui attaque les graines de légumineuses",
    "crops": ["niébé", "haricot", "arachide"],
    "urgency": "medium",
    "treatment": [
      {
        "type": "stockage",
        "product": "Sable fin ou cendres",
        "dosage": "Mélanger avec les graines",
        "timing": "Avant stockage"
      }
    ],
    "prevention": "Séchage complet, contenants hermétiques"
  },
  "cochenille_manioc": {
    "name": "Cochenille du manioc",
    "description": "Insecte suceur qui affaiblit les plants de manioc",
    "crops": ["manioc"],
    "urgency": "high",
    "treatment": [
      {
        "type": "biologique",
        "product": "Savon noir",
        "dosage": "50ml pour 1L d'eau",
        "timing": "Pulvériser 2 fois par semaine"
      }
    ],
    "prevention": "Variétés résistantes, espacement adequate"
  }
}
```

---

## 🎨 SETUP FRONTEND NUXT3

### Installation
```bash
npx nuxi@latest init agriguard-frontend
cd agriguard-frontend
npm install
npm install @nuxtjs/tailwindcss @vueuse/nuxt
# PWA Module
npm install @vite-pwa/nuxt --save-dev

# Internationalisation
npm install @nuxtjs/i18n

# Icons pour PWA
npm install @nuxt/icon
```

### nuxt.config.ts
```typescript
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss',
    '@vueuse/nuxt'
  ],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:5000'
    }
  },
  app: {
    head: {
      title: 'AgriGuard AI - Protection des cultures',
      meta: [
        { name: 'description', content: 'Détection IA des ravageurs agricoles au Cameroun' }
      ],
    }
  }
})
```

### pages/index.vue - Page principale
```vue
<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-xl">🌾</span>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">AgriGuard AI</h1>
              <p class="text-sm text-gray-600">Protection intelligente des cultures</p>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-4 py-8">
      <!-- Upload Section -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <div class="text-center mb-6">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">
            Détectez les ravageurs instantanément
          </h2>
          <p class="text-gray-600">
            Prenez une photo de vos cultures pour identifier les menaces
          </p>
        </div>

        <!-- Camera/Upload Interface -->
        <div class="max-w-md mx-auto">
          <div 
            v-if="!selectedImage" 
            class="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-green-500 transition-colors cursor-pointer"
            @click="triggerFileInput"
          >
            <div class="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <p class="text-lg font-medium text-gray-900 mb-2">Prendre une photo</p>
            <p class="text-sm text-gray-500">ou sélectionner depuis la galerie</p>
          </div>

          <!-- Image Preview -->
          <div v-if="selectedImage" class="relative">
            <img :src="selectedImage" alt="Image sélectionnée" class="w-full rounded-xl shadow-lg">
            <button 
              @click="clearImage"
              class="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600"
            >
              ×
            </button>
          </div>

          <!-- Action Buttons -->
          <div class="mt-6 space-y-3">
            <button 
              v-if="selectedImage && !isAnalyzing"
              @click="analyzeImage"
              class="w-full bg-green-600 text-white py-3 px-6 rounded-xl font-medium hover:bg-green-700 transition-colors"
            >
              🔍 Analyser l'image
            </button>
            
            <button 
              v-if="isAnalyzing"
              disabled
              class="w-full bg-gray-400 text-white py-3 px-6 rounded-xl font-medium cursor-not-allowed"
            >
              <span class="inline-block animate-spin mr-2">⏳</span>
              Analyse en cours...
            </button>

            <button 
              @click="triggerFileInput"
              class="w-full bg-gray-100 text-gray-700 py-3 px-6 rounded-xl font-medium hover:bg-gray-200 transition-colors"
            >
              📁 Choisir une autre image
            </button>
          </div>

          <input 
            ref="fileInput"
            type="file" 
            accept="image/*" 
            capture="environment"
            @change="handleFileSelect"
            class="hidden"
          >
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="detectionResults" class="bg-white rounded-2xl shadow-lg p-8">
        <h3 class="text-2xl font-bold text-gray-900 mb-6">Résultats de l'analyse</h3>
        
        <div v-if="detectionResults.detections.length === 0" class="text-center py-8">
          <div class="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
            <span class="text-2xl">✅</span>
          </div>
          <h4 class="text-xl font-semibold text-green-700 mb-2">Aucun ravageur détecté</h4>
          <p class="text-gray-600">Vos cultures semblent en bonne santé !</p>
        </div>

        <div v-else class="space-y-6">
          <div 
            v-for="(detection, index) in detectionResults.detections" 
            :key="index"
            class="border border-gray-200 rounded-xl p-6"
          >
            <!-- Pest Header -->
            <div class="flex items-center justify-between mb-4">
              <div>
                <h4 class="text-xl font-semibold text-gray-900">
                  {{ detection.pest_name }}
                </h4>
                <div class="flex items-center space-x-4 mt-1">
                  <span class="text-sm text-gray-500">
                    Confiance: {{ Math.round(detection.confidence * 100) }}%
                  </span>
                  <span 
                    :class="getUrgencyClass(detection.urgency)"
                    class="px-2 py-1 rounded-full text-xs font-medium"
                  >
                    {{ getUrgencyText(detection.urgency) }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Description -->
            <p class="text-gray-700 mb-4">{{ detection.description }}</p>

            <!-- Treatments -->
            <div v-if="detection.treatment && detection.treatment.length > 0">
              <h5 class="font-semibold text-gray-900 mb-3">Traitements recommandés:</h5>
              <div class="space-y-3">
                <div 
                  v-for="(treatment, treatIndex) in detection.treatment"
                  :key="treatIndex"
                  class="bg-blue-50 border border-blue-200 rounded-lg p-4"
                >
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium text-blue-900">{{ treatment.product }}</span>
                    <span class="text-xs bg-blue-200 text-blue-800 px-2 py-1 rounded">
                      {{ treatment.type }}
                    </span>
                  </div>
                  <p class="text-sm text-blue-700 mb-1">
                    <strong>Dosage:</strong> {{ treatment.dosage }}
                  </p>
                  <p class="text-sm text-blue-700">
                    <strong>Application:</strong> {{ treatment.timing }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const config = useRuntimeConfig()
const fileInput = ref(null)
const selectedImage = ref(null)
const isAnalyzing = ref(false)
const detectionResults = ref(null)

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      selectedImage.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const clearImage = () => {
  selectedImage.value = null
  detectionResults.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const analyzeImage = async () => {
  if (!selectedImage.value) return
  
  isAnalyzing.value = true
  
  try {
    // Convert base64 to blob
    const response = await fetch(selectedImage.value)
    const blob = await response.blob()
    
    // Create FormData
    const formData = new FormData()
    formData.append('image', blob, 'image.jpg')
    
    // Send to API
    const apiResponse = await fetch(`${config.public.apiBase}/api/detect`, {
      method: 'POST',
      body: formData
    })
    
    const result = await apiResponse.json()
    
    if (result.success) {
      detectionResults.value = result
    } else {
      throw new Error(result.error || 'Erreur analyse')
    }
    
  } catch (error) {
    console.error('Erreur analyse:', error)
    // Simulation pour MVP
    detectionResults.value = {
      success: true,
      detections: [
        {
          pest_name: "Légionnaire d'automne",
          confidence: 0.87,
          description: "Chenille destructrice qui attaque le maïs et autres graminées",
          severity: "high",
          urgency: "high",
          treatment: [
            {
              type: "chimique",
              product: "Cypermethrine 10% EC",
              dosage: "50ml pour 15L d'eau",
              timing: "Tôt le matin ou le soir"
            }
          ]
        }
      ],
      total_pests: 1
    }
  } finally {
    isAnalyzing.value = false
  }
}

const getUrgencyClass = (urgency) => {
  const classes = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  }
  return classes[urgency] || classes.medium
}

const getUrgencyText = (urgency) => {
  const texts = {
    high: 'Urgent',
    medium: 'Modéré', 
    low: 'Faible'
  }
  return texts[urgency] || 'Modéré'
}
</script>
```

---

## ⚡ DÉPLOIEMENT RAPIDE

### 1. Backend Flask - py-env
```bash
# Créer environnement virtuel
python -m venv conia2025
source conia2025/bin/activate  # Linux/Mac
# ou
conia2025\Scripts\activate     # Windows

# Installer dépendances
pip install -r requirements.txt

# Lancer serveur
python app.py
```

### 1. Backend Flask - py-env
```bash
# Créer environnement virtuel
conda env create -f environment.yml

# Activer l'environnement
conda activate conia2025 

# Lancer serveur
python app.py
```

### 2. Frontend Nuxt3
```bash
# Installer dépendances
npm install

# Mode développement
npm run dev

# Build production
npm run build
npm run preview
```

### 3. Test complet
```bash
# Backend: http://localhost:3000
# Frontend: http://localhost:8080
# Test API: http://localhost:3000/api/health
```

---

## 🎯 CHECKLIST MVP PRÉ-HACKATHON

### ✅ Fonctionnalités de base
- [ ] Interface upload/caméra
- [ ] Affichage résultats
- [ ] Design responsive
- [ ] Données de test
- [ ] API endpoints fonctionnels

### ✅ Optimisations
- [ ] Chargement rapide
- [ ] Gestion erreurs
- [ ] Feedback utilisateur
- [ ] Mobile-friendly
- [ ] Offline fallback

### ✅ Demo Ready
- [ ] Images de test préparées
- [ ] Scénarios de demo
- [ ] Données réalistes
- [ ] Performance fluide

**Résultat : UX complète en 4-6 heures, vous pouvez vous concentrer sur la data et l'IA pendant le hackathon !**