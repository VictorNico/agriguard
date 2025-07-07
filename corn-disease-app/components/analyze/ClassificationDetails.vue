<template>
  <div class="space-y-4">
    <!-- Description de la maladie/état -->
    <div v-if="diseaseInfo?.description" class="bg-gray-50 rounded-lg p-4">
      <h5 class="font-medium text-gray-900 mb-2">{{ t('results.description') }}</h5>
      <p class="text-gray-700 text-sm">{{ diseaseInfo.description }}</p>
    </div>

    <!-- Informations scientifiques -->
    <div v-if="diseaseInfo?.scientific_name" class="text-sm text-gray-600">
      <strong>{{ t('results.scientific_name') }}:</strong> {{ diseaseInfo.scientific_name }}
    </div>

    <!-- Urgence et impact -->
    <div v-if="diseaseInfo?.urgency || diseaseInfo?.impact" class="flex space-x-4 text-sm">
      <div v-if="diseaseInfo.urgency">
        <UrgencyBadge :urgency="diseaseInfo.urgency" />
      </div>
      <div v-if="diseaseInfo.impact" class="text-gray-600">
        <strong>{{ t('results.impact') }}:</strong> {{ diseaseInfo.impact }}
      </div>
    </div>

    <!-- Symptômes -->
    <div v-if="diseaseInfo?.symptoms?.length" class="bg-yellow-50 rounded-lg p-4">
      <h5 class="font-medium text-yellow-900 mb-2">{{ t('results.symptoms') }}</h5>
      <ul class="text-sm text-yellow-800 space-y-1">
        <li v-for="symptom in diseaseInfo.symptoms" :key="symptom" class="flex items-start">
          <span class="mr-2">•</span>
          <span>{{ symptom }}</span>
        </li>
      </ul>
    </div>

    <!-- Cultures affectées -->
    <div v-if="diseaseInfo?.crops_affected?.length" class="text-sm text-gray-600">
      <strong>{{ t('results.crops_affected') }}:</strong>
      {{ diseaseInfo.crops_affected.join(', ') }}
    </div>

    <!-- Top 5 prédictions -->
    <div v-if="classification.top5_predictions?.length" class="bg-blue-50 rounded-lg p-4">
      <h5 class="font-medium text-blue-900 mb-2">{{ t('results.top_predictions') }}</h5>
      <div class="space-y-2">
        <div
            v-for="prediction in classification.top5_predictions"
            :key="prediction.class_id"
            class="flex justify-between items-center text-sm"
        >
          <span class="text-blue-800">{{ prediction.class }}</span>
          <span class="text-blue-600 font-medium">{{ prediction.confidence }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  classification: Object,
  diseaseInfo: Object
})

const { t } = useI18n()
</script>