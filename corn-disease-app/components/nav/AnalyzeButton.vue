<template>
  <NuxtLink
      to="/analyze"
      class="ml-4 h-10 flex items-center px-3 sm:px-4 py-0.5 text-sm font-medium rounded-md shadow-sm text-white bg-green-700 hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 transform hover:scale-105 overflow-hidden whitespace-nowrap flex-nowrap min-w-0"
  >
    <i class="fas fa-camera mr-2 shrink-0"></i>
    <span class="truncate">{{ t('nav.analyzePlant') }}</span>
  </NuxtLink>
</template>

<script setup>
const { t } = useI18n()
</script>
