<template>
  <div class="border border-gray-200 rounded-xl p-6">
    <div class="flex items-start space-x-4">
      <!-- Miniature de l'image si disponible -->
      <div v-if="imageData" class="flex-shrink-0">
        <img :src="imageData" :alt="result.filename" class="w-16 h-16 object-cover rounded-lg">
      </div>

      <!-- Informations de classification -->
      <div class="flex-1">
        <div class="flex items-center justify-between mb-2">
          <h4 class="font-medium text-gray-900">{{ result.filename }}</h4>
          <ClassificationStatus :success="result.success" />
        </div>

        <div v-if="result.success && result.classification">
          <SingleClassificationCard :result="result" />
        </div>

        <div v-else-if="!result.success" class="text-red-600 text-sm">
          {{ result.error || t('errors.classification') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()
defineProps({
  result: Object,
  imageData: String
})
</script>