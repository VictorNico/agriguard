<template>
  <div class="flex items-center space-x-3 h-16 overflow-hidden">
    <!-- Logo -->
    <div class="h-full flex items-center">
      <a href="/" class="h-full flex items-center">
        <img
            src="/logo.png"
            alt="Logo"
            class="h-full w-auto max-h-full object-contain"
        />
      </a>
    </div>

    <!-- Texte -->
    <div class="leading-tight truncate">
      <h1 class="text-base lg:text-xl font-bold text-green-700">
        {{ t('app.main_name') }}
        <span class="text-purple-950">{{ t('app.prefix_name') }}</span>
      </h1>
      <p class="text-xs lg:text-sm text-gray-600 truncate">
        {{ t('app.tagline') }}
      </p>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()
</script>
