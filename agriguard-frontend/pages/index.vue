<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
    <!-- Offline Indicator -->
    <OfflineIndicator />
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-xl">🌾</span>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">{{ $t('app.name') }}</h1>
              <p class="text-sm text-gray-600">{{ $t('app.tagline') }}</p>
            </div>
          </div>
          <InternationalisationButtons />

        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-4 py-8">
      <!-- Upload Section -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <div class="text-center mb-6">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">
            {{ $t('home.title') }}
          </h2>
          <p class="text-gray-600">
            {{ $t('home.subtitle') }}
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
            <p class="text-lg font-medium text-gray-900 mb-2">{{ $t('home.uploadArea.title') }}</p>
            <p class="text-sm text-gray-500">{{ $t('home.uploadArea.subtitle') }}</p>
          </div>

          <!-- Image Preview -->
          <div v-if="selectedImage" class="relative">
            <img :src="selectedImage" :alt="$t('image.selected')" class="w-full rounded-xl shadow-lg">
            <button
                @click="clearImage"
                :title="$t('image.clear')"
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
              {{ $t('image.analyzeButton') }}
            </button>

            <button
                v-if="isAnalyzing"
                disabled
                class="w-full bg-gray-400 text-white py-3 px-6 rounded-xl font-medium cursor-not-allowed"
            >
              <span class="inline-block animate-spin mr-2">⏳</span>
              {{ $t('status.processing') }}
            </button>

            <button
                @click="triggerFileInput"
                class="w-full bg-gray-100 text-gray-700 py-3 px-6 rounded-xl font-medium hover:bg-gray-200 transition-colors"
            >
              {{ $t('image.chooseAnother') }}
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
        <h3 class="text-2xl font-bold text-gray-900 mb-6">{{ $t('results.title') }}</h3>

        <div v-if="detectionResults.detections.length === 0" class="text-center py-8">
          <div class="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
            <span class="text-2xl">{{ $t('results.noPests.icon') }}</span>
          </div>
          <h4 class="text-xl font-semibold text-green-700 mb-2">{{ $t('results.noPests.title') }}</h4>
          <p class="text-gray-600">{{ $t('results.noPests.description') }}</p>
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
                    {{ $t('results.confidence') }}: {{ Math.round(detection.confidence * 100) }}{{ $t('units.percentage') }}
                  </span>
                  <span
                      :class="getUrgencyClass(detection.urgency)"
                      class="px-2 py-1 rounded-full text-xs font-medium"
                  >
                    {{ $t(`results.urgency.${detection.urgency}`) }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Description -->
            <p class="text-gray-700 mb-4">{{ detection.description }}</p>

            <!-- Treatments -->
            <div v-if="detection.treatment && detection.treatment.length > 0">
              <h5 class="font-semibold text-gray-900 mb-3">{{ $t('results.treatment.recommended') }}:</h5>
              <div class="space-y-3">
                <div
                    v-for="(treatment, treatIndex) in detection.treatment"
                    :key="treatIndex"
                    class="bg-blue-50 border border-blue-200 rounded-lg p-4"
                >
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium text-blue-900">{{ treatment.product }}</span>
                    <span class="text-xs bg-blue-200 text-blue-800 px-2 py-1 rounded">
                      {{ $t(`results.treatment.type.${treatment.type}`) }}
                    </span>
                  </div>
                  <p class="text-sm text-blue-700 mb-1">
                    <strong>{{ $t('results.treatmentDetails.dosage') }}:</strong> {{ treatment.dosage }}
                  </p>
                  <p class="text-sm text-blue-700">
                    <strong>{{ $t('results.treatmentDetails.application') }}:</strong> {{ treatment.timing }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-xl p-6 mb-8">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <span class="text-red-500 text-xl">⚠️</span>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">{{ $t('status.error') }}</h3>
            <p class="mt-1 text-sm text-red-700">{{ errorMessage }}</p>
            <button
                @click="retryAnalysis"
                class="mt-2 text-sm text-red-600 hover:text-red-800 underline"
            >
              {{ $t('buttons.retry') }}
            </button>
          </div>
        </div>
      </div>
    </main>
    <!-- PWA Install Prompt -->
    <PwaInstallPrompt />
  </div>
</template>

<script setup>
import { ref } from 'vue'
// Utiliser les traductions
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

const config = useRuntimeConfig()
const fileInput = ref(null)
const selectedImage = ref(null)
const isAnalyzing = ref(false)
const detectionResults = ref(null)
const errorMessage = ref(null)

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Vérifier le type de fichier
    if (!file.type.startsWith('image/')) {
      errorMessage.value = t('errors.file')
      return
    }

    errorMessage.value = null
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
  errorMessage.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const analyzeImage = async () => {
  if (!selectedImage.value) return

  isAnalyzing.value = true
  errorMessage.value = null

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

    if (!apiResponse.ok) {
      throw new Error(`HTTP ${apiResponse.status}`)
    }

    const result = await apiResponse.json()

    if (result.success) {
      detectionResults.value = result
    } else {
      throw new Error(result.error || t('errors.analysis'))
    }

  } catch (error) {
    console.error('Erreur analyse:', error)

    // Définir le message d'erreur approprié
    if (error.message.includes('HTTP')) {
      errorMessage.value = t('errors.server')
    } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
      errorMessage.value = t('errors.network')
    } else {
      errorMessage.value = t('errors.analysis')
    }

    // Simulation pour MVP - vous pouvez commenter cette partie en production
    detectionResults.value = {
      success: true,
      detections: [
        {
          pest_name: t('pests.legionnaire_automne'),
          confidence: 0.87,
          description: "Chenille destructrice qui attaque le maïs et autres graminées",
          severity: "high",
          urgency: "high",
          treatment: [
            {
              type: "chimique",
              product: t('treatments.cypermethrine'),
              dosage: "50ml pour 15L d'eau",
              timing: t('time.morning') + " ou " + t('time.evening')
            }
          ]
        }
      ],
      total_pests: 1
    }
    errorMessage.value = null // Reset error for simulation
  } finally {
    isAnalyzing.value = false
  }
}

const retryAnalysis = () => {
  if (selectedImage.value) {
    analyzeImage()
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
</script>