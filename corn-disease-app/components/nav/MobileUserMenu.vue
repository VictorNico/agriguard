<template>
  <div class="mt-3 space-y-1 px-2">
    <span
        v-for="item in menuItems"
        :key="item.href"
        class="block px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors cursor-pointer"
        @click="item.command"
    >
      <i :class="item.icon" class="mr-2"></i>
      {{ item.label }}
    </span>
  </div>
</template>

<script setup>
import {useAuthStore} from "~/stores/auth/index.js";

const { t } = useI18n()

const authStore = useAuthStore()
const menuItems = [
  { command: ()=>{navigateTo('/profile')}, label: t('user.profile'), icon: 'fas fa-user' },
  { command: ()=>{navigateTo('/settings')}, label: t('user.settings'), icon: 'fas fa-cog' },
  { command: ()=>{authStore.logout()}, label: t('user.logout'), icon: 'fas fa-sign-out-alt' }
]
</script>