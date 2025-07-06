<template>
  <div class="text-center py-8">
    <div class="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
      <span class="text-2xl">{{ $t('results.noPests.icon') }}</span>
    </div>
    <h4 class="text-xl font-semibold text-green-700 mb-2">{{ $t('results.noPests.title') }}</h4>
    <p class="text-gray-600">{{ $t('results.noPests.description') }}</p>
  </div>
</template>

<script setup>
const { t } = useI18n()
</script>