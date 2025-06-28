<template>
  <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
  >
    <div v-if="isOpen" class="md:hidden" id="mobile-menu">
      <!-- Navigation Links -->
      <div class="pt-2 pb-3 space-y-1">
        <NuxtLink
            v-for="item in menuItems"
            :key="item.href"
            :to="item.href"
            :class="getMobileLinkClasses(item.href)"
            class="block px-3 py-2 rounded-md text-base font-medium"
        >
          {{ item.label }}
        </NuxtLink>
      </div>

      <!-- User Section -->
      <div v-if="isLoggedIn" class="pt-4 pb-3 border-t border-gray-200">
        <MobileUserInfo :user="user" />
        <MobileUserMenu />
      </div>

      <!-- Auth Buttons for Mobile -->
      <div v-else class="px-5 py-3">
        <MobileAuthButtons />
      </div>
      <lazy-divider/>
      <div class="px-5 py-3">
        <InternationalisationButtons />
      </div>
    </div>
  </Transition>
</template>

<script setup>
const props = defineProps({
  isOpen: Boolean,
  isLoggedIn: Boolean,
  user: Object,
  currentRoute: String
})

const { t } = useI18n()

const menuItems = [
  { href: '/', label: t('nav.home') || 'Accueil' },
  { href: '#features', label: t('nav.features') || 'Fonctionnalités' },
  { href: '#dashboard', label: t('nav.dashboard') || 'Tableau de bord' },
  { href: '#community', label: t('nav.community') || 'Communauté' }
]

const getMobileLinkClasses = (href) => {
  const isActive = props.currentRoute === href
  return isActive
      ? 'bg-primary text-white'
      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
}
</script>