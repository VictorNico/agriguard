<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
      <ImageUploadSection
          :selected-image="selectedImage"
          :is-analyzing="isAnalyzing"
          @file-selected="handleFileSelect"
          @clear-image="clearImage"
          @analyze="analyzeImage"
          @error="handleError"
      />

      <DetectionResults :results="detectionResults" />

      <ErrorMessage
          :message="errorMessage"
          @retry="retryAnalysis"
      />
  </div>
</template>

<script setup>
import { ref } from 'vue'

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
const selectedImage = ref(null)
const isAnalyzing = ref(false)
const detectionResults = ref(null)
const errorMessage = ref(null)

const handleFileSelect = (imageData) => {
  selectedImage.value = imageData
  errorMessage.value = null
}

const clearImage = () => {
  selectedImage.value = null
  detectionResults.value = null
  errorMessage.value = null
}

const handleError = (error) => {
  errorMessage.value = error
}

const analyzeImage = async () => {
  if (!selectedImage.value) return

  isAnalyzing.value = true
  errorMessage.value = null

  try {
    const response = await fetch(selectedImage.value)
    const blob = await response.blob()
    const formData = new FormData()
    formData.append('image', blob, 'image.jpg')

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

    if (error.message.includes('HTTP')) {
      errorMessage.value = t('errors.server')
    } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
      errorMessage.value = t('errors.network')
    } else {
      errorMessage.value = t('errors.analysis')
    }

    // Simulation pour MVP
    // detectionResults.value = {
    //   success: true,
    //   detections: [
    //     {
    //       pest_name: t('pests.legionnaire_automne'),
    //       confidence: 0.87,
    //       description: "Chenille destructrice qui attaque le maïs et autres graminées",
    //       severity: "high",
    //       urgency: "high",
    //       treatment: [
    //         {
    //           type: "chimique",
    //           product: t('treatments.cypermethrine'),
    //           dosage: "50ml pour 15L d'eau",
    //           timing: t('time.morning') + " ou " + t('time.evening')
    //         }
    //       ]
    //     }
    //   ],
    //   total_pests: 1
    // }
    // errorMessage.value = null
  } finally {
    isAnalyzing.value = false
  }
}

const retryAnalysis = () => {
  if (selectedImage.value) {
    analyzeImage()
  }
}
</script>