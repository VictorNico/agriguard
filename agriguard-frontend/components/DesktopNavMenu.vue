<template>
  <div class="hidden md:ml-8 md:flex md:space-x-8">
    <NuxtLink
        v-for="item in menuItems"
        :key="item.href"
        :to="item.href"
        :class="getLinkClasses(item.href)"
        class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
    >
      {{ item.label }}
    </NuxtLink>
  </div>
</template>

<script setup>
const props = defineProps({
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
</script>