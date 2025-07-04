<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-8xl mx-auto px-4 sm:px-2 lg:px-4">
      <div class="flex justify-between h-16">
        <!-- Logo et menu desktop -->
        <div class="flex items-center">
          <AppLogo />
          <DesktopNavMenu :current-route="currentRoute" />
        </div>

        <!-- Actions desktop -->
        <div class="hidden lg:ml-2 lg:flex lg:items-center">
          <AuthButtons v-if="!isLoggedIn" />
          <UserActions v-else :user="user" />
          <AnalyzeButton />
          <InternationalisationButtons />
        </div>

        <!-- Bouton menu mobile -->
        <MobileMenuButton @toggle="toggleMobileMenu" />
      </div>
    </div>

    <!-- Menu mobile -->
    <MobileMenu
        :is-open="isMobileMenuOpen"
        :is-logged-in="isLoggedIn"
        :user="user"
        :current-route="currentRoute"
    />
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'

// Props
const props = defineProps({
  user: {
    type: Object,
    default: () => ({
      name: 'Victor DJIEMBOU',
      email: 'victor@example.com',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
    })
  },
  isLoggedIn: {
    type: Boolean,
    default: true
  }
})

// État local
const isMobileMenuOpen = ref(false)

// Route actuelle
const route = useRoute()
const currentRoute = computed(() => route.path)

// Méthodes
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
</script>

<!--<style scoped>-->
<!--//* {-->
<!--//  outline: 1px solid red;-->
<!--//}-->

<!--</style>-->