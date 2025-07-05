<template>
  <span :class="confidenceClass" class="px-2 py-1 rounded-full text-xs font-medium">
    {{ t('results.confidence') }}: {{ percentage }}{{ t('units.percentage') }}
  </span>
</template>

<script setup>
const props = defineProps({
  confidence: Number,
  percentage: Number
})

const confidenceClass = computed(() => {
  const conf = props.confidence
  if (conf >= 0.9) return 'bg-green-100 text-green-800'
  if (conf >= 0.7) return 'bg-yellow-100 text-yellow-800'
  if (conf >= 0.5) return 'bg-orange-100 text-orange-800'
  return 'bg-red-100 text-red-800'
})

const { t } = useI18n()
</script>