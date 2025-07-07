<template>
  <button
      disabled
      class="w-full bg-gray-400 text-white py-3 px-6 rounded-xl font-medium cursor-not-allowed"
  >
    <span class="inline-block animate-spin mr-2">⏳</span>
    {{ $t('status.processing') }}
  </button>
</template>

<script setup>
const { t } = useI18n()
</script>