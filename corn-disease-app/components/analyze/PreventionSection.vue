<template>
  <div class="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
    <h5 class="font-medium text-blue-900 mb-3">{{ t('results.prevention') }}</h5>

    <ul class="text-sm text-blue-800 space-y-2">
      <li v-for="measure in preventionMeasures" :key="measure" class="flex items-start">
        <span class="mr-2 text-blue-600">•</span>
        <span>{{ measure }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  preventionMeasures: Array
})

const { t } = useI18n()
</script>