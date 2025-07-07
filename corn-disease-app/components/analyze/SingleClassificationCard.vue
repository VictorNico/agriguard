<template>
  <div class="border border-gray-200 rounded-xl p-6">
    <ClassificationHeader
        :classification="result.classification"
        :timestamp="result.timestamp"
    />

    <ClassificationDetails
        :classification="result.classification"
        :disease-info="result.disease_info"
    />

    <TreatmentSection
        v-if="result.disease_info?.treatment_recommendations?.length"
        :treatments="result.disease_info.treatment_recommendations"
    />

    <PreventionSection
        v-if="result.disease_info?.prevention_measures?.length"
        :prevention-measures="result.disease_info.prevention_measures"
    />
  </div>
</template>

<script setup>
defineProps({
  result: Object
})
</script>