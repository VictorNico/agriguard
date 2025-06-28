<template>
  <div>
    <!-- Zone de dépôt -->
    <div
        v-if="!selectedImage"
        class="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-green-500 transition-colors cursor-pointer"
        @click="$emit('triggerUpload')"
    >
      <div class="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
        <CameraIcon />
      </div>
      <p class="text-lg font-medium text-gray-900 mb-2">{{ $t('home.uploadArea.title') }}</p>
      <p class="text-sm text-gray-500">{{ $t('home.uploadArea.subtitle') }}</p>
    </div>

    <!-- Prévisualisation image -->
    <div v-if="selectedImage" class="relative">
      <img :src="selectedImage" :alt="$t('image.selected')" class="w-full rounded-xl shadow-lg">
      <button
          @click="$emit('clearImage')"
          :title="$t('image.clear')"
          class="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600"
      >
        ×
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  selectedImage: String
})

defineEmits(['triggerUpload', 'clearImage'])

const { t } = useI18n()
</script>