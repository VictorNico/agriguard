<template>
  <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
    <div class="text-center mb-6">
      <h2 class="text-3xl font-bold text-gray-900 mb-2">
        {{ $t('home.title') }}
      </h2>
      <p class="text-gray-600">
        {{ $t('home.subtitle') }}
      </p>
    </div>

    <div class="max-w-md mx-auto">
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

      <input
          ref="fileInput"
          type="file"
          accept="image/*"
          capture="environment"
          @change="handleFileChange"
          class="hidden"
      >
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  selectedImage: String,
  isAnalyzing: Boolean
})

const emit = defineEmits(['fileSelected', 'clearImage', 'analyze'])

const { t } = useI18n()
const fileInput = ref(null)

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
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

const handleFileSelect = (image) => {
  emit('fileSelected', image)
}

const clearImage = () => {
  emit('clearImage')
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>