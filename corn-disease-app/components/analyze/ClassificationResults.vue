<template>
  <div v-if="results" class="bg-white rounded-2xl shadow-lg p-8">
    <h3 class="text-2xl font-bold text-gray-900 mb-6">{{ t('results.title') }}</h3>

    <!-- Résultats pour une seule image -->
    <div v-if="results.classification" class="space-y-6">
      <SingleClassificationCard :result="results" />
    </div>

    <!-- Résultats pour plusieurs images (batch) -->
    <div v-else-if="results.results" class="space-y-6">
      <div class="mb-4 p-4 bg-blue-50 rounded-lg">
        <p class="text-sm text-blue-700">
          {{ t('results.batch.summary', {
          total: results.total_images,
          successful: results.successful_classifications
        }) }}
        </p>
      </div>

      <BatchClassificationCard
          v-for="(result, index) in results.results"
          :key="index"
          :result="result"
          :image-data="getImageData(index)"
      />
    </div>

    <!-- Aucun résultat -->
    <NoDetectionMessage v-else />
  </div>
</template>

<script setup>
const props = defineProps({
  results: Object
})

const { t } = useI18n()

// Pour récupérer les données d'image si nécessaire
const getImageData = (index) => {
  // Cette fonction peut être étendue selon vos besoins
  return null
}
</script>
