<template>
  <div class="flex items-center justify-between mb-4">
    <div>
      <h4 class="text-xl font-semibold text-gray-900">
        {{ detection.pest_name }}
      </h4>
      <div class="flex items-center space-x-4 mt-1">
        <span class="text-sm text-gray-500">
          {{ $t('results.confidence') }}: {{ Math.round(detection.confidence * 100) }}{{ $t('units.percentage') }}
        </span>
        <UrgencyBadge :urgency="detection.urgency" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  detection: Object
})

const { t } = useI18n()
</script>