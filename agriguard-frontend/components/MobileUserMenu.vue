<template>
  <div class="mt-3 space-y-1 px-2">
    <NuxtLink
        v-for="item in menuItems"
        :key="item.href"
        :to="item.href"
        class="block px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors"
    >
      <i :class="item.icon" class="mr-2"></i>
      {{ item.label }}
    </NuxtLink>
  </div>
</template>

<script setup>
const { t } = useI18n()

const menuItems = [
  { href: '/profile', label: t('user.profile') || 'Votre profil', icon: 'fas fa-user' },
  { href: '/settings', label: t('user.settings') || 'Paramètres', icon: 'fas fa-cog' },
  { href: '/logout', label: t('user.logout') || 'Déconnexion', icon: 'fas fa-sign-out-alt' }
]
</script>