<template>
  <span :class="statusClass" class="px-2 py-1 rounded-full text-xs font-medium">
    {{ success ? t('results.status.success') : t('results.status.error') }}
  </span>
</template>

<script setup>
const props = defineProps({
  success: Boolean
})

const statusClass = computed(() => {
  return props.success
      ? 'bg-green-100 text-green-800'
      : 'bg-red-100 text-red-800'
})

const { t } = useI18n()
</script>
