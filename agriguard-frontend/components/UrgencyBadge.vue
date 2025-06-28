<template>
  <span
      :class="getUrgencyClass(urgency)"
      class="px-2 py-1 rounded-full text-xs font-medium"
  >
    {{ $t(`results.urgency.${urgency}`) }}
  </span>
</template>

<script setup>
defineProps({
  urgency: String
})

const { t } = useI18n()

const getUrgencyClass = (urgency) => {
  const classes = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  }
  return classes[urgency] || classes.medium
}
</script>