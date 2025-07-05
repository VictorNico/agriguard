<template>
  <div class="mb-4">
    <div class="flex items-center justify-between">
      <h4 class="text-xl font-semibold text-gray-900">
        {{ classification.predicted_class }}
      </h4>
      <div class="text-sm text-gray-500">
        {{ formatTimestamp(timestamp) }}
      </div>
    </div>

    <div class="flex items-center space-x-4 mt-2">
      <ConfidenceBadge
          :confidence="classification.confidence"
          :percentage="classification.confidence_percentage"
      />
      <SeverityBadge :severity="classification.severity" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  classification: Object,
  timestamp: String
})

const formatTimestamp = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleString()
}
</script>
