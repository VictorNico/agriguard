<template>
  <div>
    <!-- Zone de dépôt pour plusieurs images -->
    <div
        v-if="!selectedImages.length"
        class="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-green-500 transition-colors cursor-pointer"
        @click="$emit('triggerUpload')"
    >
      <div class="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
        <CameraIcon />
      </div>
      <p class="text-lg font-medium text-gray-900 mb-2">{{ t('home.uploadArea.batch_title') }}</p>
      <p class="text-sm text-gray-500">{{ t('home.uploadArea.batch_subtitle') }}</p>
    </div>

    <!-- Prévisualisation des images -->
    <div v-if="selectedImages.length" class="space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-sm font-medium text-gray-700">
          {{ t('home.images_selected', { count: selectedImages.length }) }}
        </span>
        <button
            @click="$emit('clearImages')"
            class="text-sm text-red-600 hover:text-red-700"
        >
          {{ t('image.clear_all') }}
        </button>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div v-for="(image, index) in selectedImages" :key="index" class="relative">
          <img :src="image" :alt="`Image ${index + 1}`" class="w-full h-24 object-cover rounded-lg shadow-sm">
          <button
              @click="removeImage(index)"
              class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-red-600"
          >
            ×
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  selectedImages: Array
})

const emit = defineEmits(['triggerUpload', 'clearImages', 'removeImage'])

const { t } = useI18n()

const removeImage = (index) => {
  const newImages = [...props.selectedImages]
  newImages.splice(index, 1)
  emit('filesSelected', newImages)
}
</script>
