<template>
  <div class="mt-6 space-y-3">
    <button
        v-if="selectedImages.length && !isAnalyzing"
        @click="$emit('analyze')"
        class="w-full bg-green-600 text-white py-3 px-6 rounded-xl font-medium hover:bg-green-700 transition-colors"
    >
      {{ t('image.analyze_batch', { count: selectedImages.length }) }}
    </button>

    <LoadingButton v-if="isAnalyzing" />

    <button
        @click="$emit('triggerUpload')"
        class="w-full bg-gray-100 text-gray-700 py-3 px-6 rounded-xl font-medium hover:bg-gray-200 transition-colors"
    >
      {{ selectedImages.length ? t('image.add_more') : t('image.choose_images') }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  selectedImages: Array,
  isAnalyzing: Boolean
})

defineEmits(['analyze', 'triggerUpload'])

const { t } = useI18n()
</script>