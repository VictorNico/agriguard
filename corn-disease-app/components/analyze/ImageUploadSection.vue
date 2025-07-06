<template>
  <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
    <div class="text-center mb-6">
      <h2 class="text-3xl font-bold text-gray-900 mb-2">
        {{ t('home.title') }}
      </h2>
      <p class="text-gray-600">
        {{ t('home.subtitle') }}
      </p>
    </div>

    <!-- Toggle pour mode batch -->
    <div class="flex justify-center mb-6">
      <button
          @click="$emit('toggleBatchMode')"
          class="flex items-center space-x-2 px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
      >
        <span class="text-sm font-medium">
          {{ batchMode ? t('home.single_mode') : t('home.batch_mode') }}
        </span>
      </button>
    </div>

    <div class="max-w-md mx-auto">
      <!-- Mode simple -->
      <div v-if="!batchMode">
        <ImageUploadArea
            :selected-image="selectedImage"
            @file-selected="handleFileSelect"
            @clear-image="clearImage"
            @trigger-upload="triggerFileInput"
        />

        <ImageUploadActions
            :selected-image="selectedImage"
            :is-analyzing="isAnalyzing"
            @analyze="$emit('analyze')"
            @trigger-upload="triggerFileInput"
        />
      </div>

      <!-- Mode batch -->
      <div v-else>
        <BatchImageUploadArea
            :selected-images="selectedImages"
            @files-selected="handleFilesSelect"
            @clear-images="clearImages"
            @trigger-upload="triggerFileInput"
        />

        <BatchImageUploadActions
            :selected-images="selectedImages"
            :is-analyzing="isAnalyzing"
            @analyze="$emit('analyzeBatch')"
            @trigger-upload="triggerFileInput"
        />
      </div>

      <input
          ref="fileInput"
          type="file"
          :accept="'image/*'"
          :multiple="batchMode"
          :capture="!batchMode ? 'environment' : undefined"
          @change="handleFileChange"
          class="hidden"
      >
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  selectedImage: String,
  selectedImages: Array,
  isAnalyzing: Boolean,
  batchMode: Boolean
})

const emit = defineEmits(['fileSelected', 'filesSelected', 'clearImage', 'clearImages', 'analyze', 'analyzeBatch', 'toggleBatchMode'])

const { t } = useI18n()
const fileInput = ref(null)

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const files = Array.from(event.target.files)

  if (props.batchMode) {
    // Mode batch
    if (files.length > 10) {
      emit('error', t('errors.too_many_files'))
      return
    }

    const validFiles = files.filter(file => file.type.startsWith('image/'))
    if (validFiles.length !== files.length) {
      emit('error', t('errors.invalid_files'))
      return
    }

    const imagePromises = validFiles.map(file => {
      return new Promise((resolve) => {
        const reader = new FileReader()
        reader.onload = (e) => resolve(e.target.result)
        reader.readAsDataURL(file)
      })
    })

    Promise.all(imagePromises).then(images => {
      emit('filesSelected', images)
    })
  } else {
    // Mode simple
    const file = files[0]
    if (file) {
      if (!file.type.startsWith('image/')) {
        emit('error', t('errors.file'))
        return
      }

      const reader = new FileReader()
      reader.onload = (e) => {
        emit('fileSelected', e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }
}

const handleFileSelect = (image) => {
  emit('fileSelected', image)
}

const handleFilesSelect = (images) => {
  emit('filesSelected', images)
}

const clearImage = () => {
  emit('clearImage')
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const clearImages = () => {
  emit('clearImages')
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>