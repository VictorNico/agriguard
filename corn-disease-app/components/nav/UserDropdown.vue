<template>
  <div class="ml-3 relative">
    <div>
      <button
          type="button"
          class="bg-gray-800 flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white transition-colors"
          @click="toggleDropdown"
          :aria-expanded="isDropdownOpen"
          aria-haspopup="true"
      >
        <span class="sr-only">{{ $t('user.openMenu') }}</span>
        <img
            class="h-8 w-8 rounded-full"
            :src="user.avatar"
            :alt="user.name"
        >
      </button>
    </div>

    <!-- Menu déroulant -->
    <Transition
        enter-active-class="transition ease-out duration-100"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
    >
      <div
          v-if="isDropdownOpen"
          class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50"
      >
        <NuxtLink
            v-for="item in menuItems"
            :key="item.href"
            :to="item.href"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
            @click="closeDropdown"
        >
          <i :class="item.icon" class="mr-2"></i>
          {{ item.label }}
        </NuxtLink>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  user: Object
})

const { t } = useI18n()
const isDropdownOpen = ref(false)

const menuItems = [
  { href: '/profile', label: t('user.profile'), icon: 'fas fa-user' },
  { href: '/settings', label: t('user.settings'), icon: 'fas fa-cog' },
  { href: '/logout', label: t('user.logout'), icon: 'fas fa-sign-out-alt' }
]

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const closeDropdown = () => {
  isDropdownOpen.value = false
}

// Fermer le dropdown en cliquant à l'extérieur
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>