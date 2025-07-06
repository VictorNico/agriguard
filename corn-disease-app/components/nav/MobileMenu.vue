<template>
  <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
  >
    <div v-if="isOpen" ref="menuRef" class="lg:hidden" id="mobile-menu">
      <!-- Navigation Links -->
      <div class="pt-2 pb-3 space-y-1">
        <NuxtLink
            v-for="item in menu"
            :key="item.href"
            :to="item.href"
            @click="handleLinkClick"
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
      <div class="flex justify-between px-5 py-3">
        <InternationalisationButtons />
        <AnalyzeButton />
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'
import { onClickOutside } from '@vueuse/core'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  isOpen: Boolean,
  isLoggedIn: Boolean,
  user: Object,
  currentRoute: String
})

const emit = defineEmits(['close']) // 🔴 pour fermer le menu depuis le parent

const { t } = useI18n()

const menu = computed(() => props.isLoggedIn ? authMenuItems : visitorMenuItems)

const visitorMenuItems = [
  { href: '/', label: t('nav.home') },
  { href: '#features', label: t('nav.features') },
  { href: '#marketPlace', label: t('nav.marketPlace') },
  { href: '#blog', label: t('nav.blog') },
  { href: '#faq', label: t('nav.faq') },
  { href: '#about', label: t('nav.aboutUs') },
]

const authMenuItems = [
  { href: '/', label: t('nav.home') },
  { href: '#dashboard', label: t('nav.dashboard') },
  { href: '#marketplace', label: t('nav.marketPlace') },
  { href: '#community', label: t('nav.community') },
  { href: '/forum', label: t('nav.forum') },
  { href: '/blog', label: t('nav.blog') },
  { href: '/faq', label: t('nav.faq') },
]


const getMobileLinkClasses = (href) => {
  const isActive = props.currentRoute === href
  return isActive
      ? 'bg-green-700 text-white'
      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
}

const menuRef = ref(null)

// ⬇️ Fermer si clic à l'extérieur
onClickOutside(menuRef, () => {
  if (props.isOpen) emit('close')
})

// ⬇️ Fermer quand on clique sur un lien
const handleLinkClick = () => {
  emit('close')
}
</script>
