<template>
  <div class="-mr-2 flex items-center md:hidden">
    <button
        type="button"
        class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary transition-colors"
        aria-controls="mobile-menu"
        :aria-expanded="false"
        @click="$emit('toggle')"
    >
      <span class="sr-only">{{ $t('nav.openMainMenu') }}</span>
      <i class="fas fa-bars h-6 w-6"></i>
    </button>
  </div>
</template>

<script setup>
defineEmits(['toggle'])
const { t } = useI18n()
</script>