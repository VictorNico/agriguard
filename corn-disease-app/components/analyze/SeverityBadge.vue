<template>
  <span :class="severityClass" class="px-2 py-1 rounded-full text-xs font-medium">
    {{ t(`results.severity.${severity}`) }}
  </span>
</template>

<script setup>
const props = defineProps({
  severity: String
})

const severityClass = computed(() => {
  switch (props.severity) {
    case 'very_high': return 'bg-red-100 text-red-800'
    case 'high': return 'bg-orange-100 text-orange-800'
    case 'medium': return 'bg-yellow-100 text-yellow-800'
    case 'low': return 'bg-blue-100 text-blue-800'
    case 'very_low': return 'bg-gray-100 text-gray-800'
    default: return 'bg-gray-100 text-gray-800'
  }
})

const { t } = useI18n()
</script>