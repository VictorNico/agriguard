<template>
  <div>
    <h5 class="font-semibold text-gray-900 mb-3">{{ $t('results.treatment.recommended') }}:</h5>
    <div class="space-y-3">
      <TreatmentCard
          v-for="(treatment, index) in treatments"
          :key="index"
          :treatment="treatment"
      />
    </div>
  </div>
</template>

<script setup>
defineProps({
  treatments: Array
})

const { t } = useI18n()
</script>