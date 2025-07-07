<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <ImageUploadSection
        :selected-image="selectedImage"
        :selected-images="selectedImages"
        :is-analyzing="isAnalyzing"
        :batch-mode="batchMode"
        @file-selected="handleFileSelect"
        @files-selected="handleFilesSelect"
        @clear-image="clearImage"
        @clear-images="clearImages"
        @analyze="analyzeImage"
        @analyze-batch="analyzeBatch"
        @toggle-batch-mode="toggleBatchMode"
        @error="handleError"
    />

    <classificationResults :results="classification_Results"/>

    <ErrorMessage
        :message="errorMessage"
        @retry="retryAnalysis"
    />
  </div>
</template>

<script setup>
import {ref} from 'vue'

const {t} = useI18n()
import {useAuthStore} from "~/stores/auth/index.js";
const authStore = useAuthStore()
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
const selectedImages = ref([])
const batchMode = ref(false)
const isAnalyzing = ref(false)
const classification_Results = ref(null)
const errorMessage = ref(null)

const handleFileSelect = (imageData) => {
  selectedImage.value = imageData
  errorMessage.value = null
}

const handleFilesSelect = (imagesData) => {
  selectedImages.value = imagesData
  errorMessage.value = null
}

const clearImage = () => {
  selectedImage.value = null
  classification_Results.value = null
  errorMessage.value = null
}

const clearImages = () => {
  selectedImages.value = []
  classification_Results.value = null
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

const analyzeImage = async () => {
  if (!selectedImage.value) return

  isAnalyzing.value = true
  errorMessage.value = null

  try {
    const response = await fetch(selectedImage.value)
    const blob = await response.blob()
    const formData = new FormData()
    formData.append('image', blob, 'image.jpg')
    formData.append('user_id',authStore?.user?.user_id || 'unknown' )
    const apiResponse = await fetch(`${config.public.apiBase}/api/classify`, {
      method: 'POST',
      body: formData
    })

    if (!apiResponse.ok) {
      throw new Error(`HTTP ${apiResponse.status}`)
    }

    const result = await apiResponse.json()

    if (result.success) {
      classification_Results.value = result
    } else {
      throw new Error(result.error || t('errors.analysis'))
    }

  } catch (error) {
    console.error('Erreur analyse:', error)
    handleApiError(error)
  } finally {
    isAnalyzing.value = false
  }
}

const analyzeBatch = async () => {
  if (!selectedImages.value.length) return

  isAnalyzing.value = true
  errorMessage.value = null

  try {
    const formData = new FormData()

    // Convertir chaque image en blob et l'ajouter au FormData
    for (let i = 0; i < selectedImages.value.length; i++) {
      const response = await fetch(selectedImages.value[i])
      const blob = await response.blob()
      formData.append('images', blob, `image_${i}.jpg`)
    }
    formData.append('user_id',authStore?.user?.user_id || 'unknown' )
    const apiResponse = await fetch(`${config.public.apiBase}/api/classify/batch`, {
      method: 'POST',
      body: formData
    })

    if (!apiResponse.ok) {
      throw new Error(`HTTP ${apiResponse.status}`)
    }

    const result = await apiResponse.json()

    if (result.success) {
      classification_Results.value = result
    } else {
      throw new Error(result.error || t('errors.analysis'))
    }

  } catch (error) {
    console.error('Erreur analyse batch:', error)
    handleApiError(error)
  } finally {
    isAnalyzing.value = false
  }
}

const handleApiError = (error) => {
  if (error.message.includes('HTTP')) {
    errorMessage.value = t('errors.server')
  } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
    errorMessage.value = t('errors.network')
  } else {
    errorMessage.value = t('errors.analysis')
  }
}

const retryAnalysis = () => {
  if (batchMode.value && selectedImages.value.length > 0) {
    analyzeBatch()
  } else if (selectedImage.value) {
    analyzeImage()
  }
}
</script>