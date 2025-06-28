<template>
  <NuxtLink
      to="/analyze"
      class="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-700 hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 transform hover:scale-105"
  >
    <i class="fas fa-camera mr-2"></i>
    {{ $t('nav.analyzePlant') }}
  </NuxtLink>
</template>

<script setup>
const { t } = useI18n()
</script>