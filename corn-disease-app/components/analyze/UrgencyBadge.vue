<template>
  <span :class="urgencyClass" class="px-2 py-1 rounded-full text-xs font-medium">
    {{ t(`results.urgency.${urgency}`) }}
  </span>
</template>

<script setup>
const props = defineProps({
  urgency: String
})

const urgencyClass = computed(() => {
  switch (props.urgency) {
    case 'critical': return 'bg-red-100 text-red-800'
    case 'high': return 'bg-orange-100 text-orange-800'
    case 'medium': return 'bg-yellow-100 text-yellow-800'
    case 'low': return 'bg-green-100 text-green-800'
    default: return 'bg-gray-100 text-gray-800'
  }
})

const { t } = useI18n()
</script>
