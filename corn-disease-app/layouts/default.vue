<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
    <OfflineIndicator />
    <NavigationBar
        :user="user"
        :is-logged-in="isLoggedIn"
    />
    <main >
      <slot />
    </main>
    <FooterSection />
    <PwaInstallPrompt />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {useAuthStore} from "~/stores/auth/index.js";
import {Capacitor} from "@capacitor/core";


const authStore = useAuthStore()
// Simulation de l'état utilisateur (à remplacer par votre logique d'authentification)
const user = ref({
  name: `${authStore.userName}`,
  email: `${authStore.userEmail}`,
  avatar: authStore.user?.profile?.avatar_url || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
})

const isLoggedIn = ref(authStore.isLoggedIn)
watch(isLoggedIn, (newValue) => {
    user.value = {
      name: `${authStore.userName}`,
      email: `${authStore.userEmail}`,
      avatar: authStore.user?.profile?.avatar_url || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
    }

})
</script>