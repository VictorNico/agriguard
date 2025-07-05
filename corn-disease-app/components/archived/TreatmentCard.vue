<template>
  <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
    <div class="flex items-center justify-between mb-2">
      <span class="font-medium text-blue-900">{{ treatment.product }}</span>
      <span class="text-xs bg-blue-200 text-blue-800 px-2 py-1 rounded">
        {{ $t(`results.treatment.type.${treatment.type}`) }}
      </span>
    </div>
    <p class="text-sm text-blue-700 mb-1">
      <strong>{{ $t('results.treatmentDetails.dosage') }}:</strong> {{ treatment.dosage }}
    </p>
    <p class="text-sm text-blue-700">
      <strong>{{ $t('results.treatmentDetails.application') }}:</strong> {{ treatment.timing }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  treatment: Object
})

const { t } = useI18n()
</script>