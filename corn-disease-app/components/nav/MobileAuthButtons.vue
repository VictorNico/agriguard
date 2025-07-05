<template>
  <div class="grid grid-cols-2 gap-4">
    <NuxtLink
        to="/login"
        class="auth-btn px-4 py-2 border border-transparent text-sm font-medium rounded-md text-green-700 bg-white hover:bg-gray-50 text-center transition-colors"
    >
      <i class="fas fa-sign-in-alt mr-2"></i>
      {{ $t('auth.login')}}
    </NuxtLink>
    <NuxtLink
        to="/register"
        class="auth-btn px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-700 hover:bg-secondary text-center transition-colors"
    >
      <i class="fas fa-user-plus mr-2"></i>
      {{ $t('auth.register')}}
    </NuxtLink>
  </div>
</template>

<script setup>
const { t } = useI18n()
</script>