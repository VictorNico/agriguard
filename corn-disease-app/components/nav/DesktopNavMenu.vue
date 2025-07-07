<template>
  <div class="hidden lg:ml-8 lg:flex lg:space-x-8">
    <NuxtLink
        v-for="item in menu"
        :key="item.href"
        :to="item.href"
        :class="getLinkClasses(item.href)"
        class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium truncate"
    >
      {{ item.label }}
    </NuxtLink>
  </div>
</template>

<script setup>
const props = defineProps({
  isLoggedIn: Boolean,
  currentRoute: String
})


const { t } = useI18n()

const menuItems = [
  { href: '/', label: t('nav.home') },
  { href: '#features', label: t('nav.features') },
  { href: '#dashboard', label: t('nav.dashboard') },
  { href: '#community', label: t('nav.community') }
]

const getLinkClasses = (href) => {
  const isActive = props.currentRoute === href
  return isActive
      ? 'border-primary text-dark'
      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
}

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
  { href: '/dashboard', label: t('nav.dashboard') },
  { href: '/marketplace', label: t('nav.marketPlace') },
  { href: '/community', label: t('nav.community') },
  { href: '/forum', label: t('nav.forum') },
  { href: '/blog', label: t('nav.blog') },
  { href: '/faq', label: t('nav.faq') },
]
</script>