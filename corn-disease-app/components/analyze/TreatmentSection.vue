<template>
  <div class="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
    <h5 class="font-medium text-green-900 mb-3">{{ t('results.treatments') }}</h5>

    <div class="space-y-3">
      <div
          v-for="treatment in treatments"
          :key="treatment.product || treatment.method"
          class="bg-white rounded-lg p-3 border border-green-200"
      >
        <div class="flex items-center justify-between mb-2">
          <span class="font-medium text-green-900">
            {{ treatment.product || treatment.method }}
          </span>
          <span class="text-xs bg-green-200 text-green-800 px-2 py-1 rounded">
            {{ t(`results.treatment.type.${treatment.type}`) }}
          </span>
        </div>

        <div class="text-sm text-green-700 space-y-1">
          <p v-if="treatment.dosage">
            <strong>{{ t('results.treatment.dosage') }}:</strong> {{ treatment.dosage }}
          </p>
          <p v-if="treatment.application_method">
            <strong>{{ t('results.treatment.application') }}:</strong> {{ treatment.application_method }}
          </p>
          <p v-if="treatment.timing">
            <strong>{{ t('results.treatment.timing') }}:</strong> {{ treatment.timing }}
          </p>
          <p v-if="treatment.frequency">
            <strong>{{ t('results.treatment.frequency') }}:</strong> {{ treatment.frequency }}
          </p>
        </div>

        <div v-if="treatment.precautions" class="mt-2 text-xs text-orange-700 bg-orange-50 p-2 rounded">
          <strong>{{ t('results.treatment.precautions') }}:</strong> {{ treatment.precautions }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  treatments: Array
})

const { t } = useI18n()
</script>