<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Section de statut du modèle -->
    <div class="mb-6 p-4 rounded-lg" :class="modelStatusClass">
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full" :class="modelStatusIndicator"></div>
        <span class="font-medium">{{ modelStatusText }}</span>
      </div>
      <p class="text-sm mt-1 opacity-80">{{ modelStatusDescription }}</p>
    </div>

    <!-- Bouton de chargement du modèle -->
    <div v-if="!modelLoaded && !isLoadingModel" class="mb-6">
      <button
          @click="initializeModel"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
      >
        Charger le modèle IA
      </button>
    </div>

    <!-- Section d'upload d'image -->
    <ImageUploadSection
        :selected-image="selectedImage"
        :selected-images="selectedImages"
        :is-analyzing="isAnalyzing"
        :batch-mode="batchMode"
        :disabled="!modelLoaded"
        @file-selected="handleFileSelect"
        @files-selected="handleFilesSelect"
        @clear-image="clearImage"
        @clear-images="clearImages"
        @analyze="analyzeImage"
        @analyze-batch="analyzeBatch"
        @toggle-batch-mode="toggleBatchMode"
        @error="handleError"
    />

    <!-- Résultats de classification -->
    <ClassificationResults :results="classificationResults" />

    <!-- Messages d'erreur -->
    <ErrorMessage
        :message="errorMessage"
        @retry="retryAnalysis"
    />

    <!-- Informations sur le modèle (debug) -->
    <div v-if="modelLoaded && isDevelopment" class="mt-8 p-4 bg-gray-100 rounded-lg">
      <h3 class="font-medium mb-2">Informations du modèle</h3>
      <pre class="text-sm">{{ JSON.stringify(modelInfo, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const { t } = useI18n()

// Meta tags dynamiques
useSeoMeta({
  title: t('app.name'),
  description: t('app.description'),
  ogTitle: t('app.name'),
  ogDescription: t('app.description'),
  twitterTitle: t('app.name'),
  twitterDescription: t('app.description')
})

// Utiliser le composable de classification
const {
  modelLoaded,
  isLoading: isLoadingModel,
  error: modelError,
  loadModel,
  classify,
  classifyBatch,
  getModelInfo
} = useMaizeClassifier()

// État de l'interface
const selectedImage = ref(null)
const selectedImages = ref([])
const batchMode = ref(false)
const isAnalyzing = ref(false)
const classificationResults = ref(null)
const errorMessage = ref(null)
const modelInfo = ref(null)

// Variables d'environnement
const isDevelopment = process.env.NODE_ENV === 'development'

// Statut du modèle
const modelStatusClass = computed(() => {
  if (isLoadingModel.value) return 'bg-yellow-50 border border-yellow-200'
  if (modelError.value) return 'bg-red-50 border border-red-200'
  if (modelLoaded.value) return 'bg-green-50 border border-green-200'
  return 'bg-gray-50 border border-gray-200'
})

const modelStatusIndicator = computed(() => {
  if (isLoadingModel.value) return 'bg-yellow-500 animate-pulse'
  if (modelError.value) return 'bg-red-500'
  if (modelLoaded.value) return 'bg-green-500'
  return 'bg-gray-400'
})

const modelStatusText = computed(() => {
  if (isLoadingModel.value) return 'Chargement du modèle...'
  if (modelError.value) return 'Erreur du modèle'
  if (modelLoaded.value) return 'Modèle prêt'
  return 'Modèle non chargé'
})

const modelStatusDescription = computed(() => {
  if (isLoadingModel.value) return 'Téléchargement et initialisation en cours'
  if (modelError.value) return modelError.value
  if (modelLoaded.value) return 'Classification disponible en mode hors ligne'
  return 'Cliquez pour charger le modèle de classification'
})

// Initialiser le modèle
const initializeModel = async () => {
  try {
    await loadModel('/models/model.json') // Chemin vers votre modèle
    if (modelLoaded.value) {
      modelInfo.value = getModelInfo()
    }
  } catch (error) {
    console.error('Erreur initialisation modèle:', error)
    errorMessage.value = 'Impossible de charger le modèle IA'
  }
}

// Gestionnaires d'événements
const handleFileSelect = (imageData) => {
  selectedImage.value = imageData
  errorMessage.value = null
  classificationResults.value = null
}

const handleFilesSelect = (imagesData) => {
  selectedImages.value = imagesData
  errorMessage.value = null
  classificationResults.value = null
}

const clearImage = () => {
  selectedImage.value = null
  classificationResults.value = null
  errorMessage.value = null
}

const clearImages = () => {
  selectedImages.value = []
  classificationResults.value = null
  errorMessage.value = null
}

const toggleBatchMode = () => {
  batchMode.value = !batchMode.value
  clearImage()
  clearImages()
}

const handleError = (error) => {
  errorMessage.value = error
}

// Analyser une image
const analyzeImage = async () => {
  if (!selectedImage.value || !modelLoaded.value) return

  isAnalyzing.value = true
  errorMessage.value = null

  try {
    // Convertir l'image en File ou utiliser directement l'URL
    let imageToAnalyze
    if (selectedImage.value.startsWith('data:')) {
      // Si c'est une data URL, créer un blob
      const response = await fetch(selectedImage.value)
      imageToAnalyze = await response.blob()
    } else {
      imageToAnalyze = selectedImage.value
    }

    const result = await classify(imageToAnalyze)

    if (result.success) {
      classificationResults.value = result
    } else {
      throw new Error(result.error || 'Erreur de classification')
    }

  } catch (error) {
    console.error('Erreur analyse:', error)
    errorMessage.value = error.message || 'Erreur lors de l\'analyse de l\'image'
  } finally {
    isAnalyzing.value = false
  }
}

// Analyser plusieurs images
const analyzeBatch = async () => {
  if (!selectedImages.value.length || !modelLoaded.value) return

  isAnalyzing.value = true
  errorMessage.value = null

  try {
    // Convertir les images en format utilisable
    const imagesToAnalyze = []
    for (const imageUrl of selectedImages.value) {
      if (imageUrl.startsWith('data:')) {
        const response = await fetch(imageUrl)
        const blob = await response.blob()
        imagesToAnalyze.push(blob)
      } else {
        imagesToAnalyze.push(imageUrl)
      }
    }

    const results = await classifyBatch(imagesToAnalyze)

    // Formater les résultats pour correspondre à l'API
    const batchResult = {
      success: true,
      results: results,
      timestamp: new Date().toISOString()
    }

    classificationResults.value = batchResult

  } catch (error) {
    console.error('Erreur analyse batch:', error)
    errorMessage.value = error.message || 'Erreur lors de l\'analyse des images'
  } finally {
    isAnalyzing.value = false
  }
}

// Réessayer l'analyse
const retryAnalysis = () => {
  if (batchMode.value && selectedImages.value.length > 0) {
    analyzeBatch()
  } else if (selectedImage.value) {
    analyzeImage()
  }
}

// Initialiser automatiquement le modèle au montage du composant
onMounted(() => {
  // Charger automatiquement le modèle si disponible
  if (process.client) {
    initializeModel()
  }
})
</script>