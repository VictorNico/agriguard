<template>
  <div class="flex items-center space-x-3">
<!--    <div class="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">-->
<!--      <span class="text-white font-bold text-xl">🌾</span>-->
<!--    </div>-->
    <div class="flex lg:flex-1">
      <a href="/" class="-m-1.5 p-2.5">
        <img class="h-15 w-auto" src="/logo.png" alt="" />
      </a>
    </div>
    <div>
      <h1 class="text-2xl font-bold text-green-700">{{ $t('app.main_name') }} <span class="text-purple-950">{{ $t('app.prefix_name') }}</span></h1>
      <p class="text-sm text-gray-600">{{ $t('app.tagline') }}</p>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()
</script>