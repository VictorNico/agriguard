<template>
  <div class="mt-6 space-y-3">
    <button
        v-if="selectedImage && !isAnalyzing"
        @click="$emit('analyze')"
        class="w-full bg-green-600 text-white py-3 px-6 rounded-xl font-medium hover:bg-green-700 transition-colors"
    >
      {{ $t('image.analyzeButton') }}
    </button>

    <LoadingButton v-if="isAnalyzing" />

    <button
        @click="$emit('triggerUpload')"
        class="w-full bg-gray-100 text-gray-700 py-3 px-6 rounded-xl font-medium hover:bg-gray-200 transition-colors"
    >
      {{ $t('image.chooseAnother') }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  selectedImage: String,
  isAnalyzing: Boolean
})

defineEmits(['analyze', 'triggerUpload'])

const { t } = useI18n()
</script>