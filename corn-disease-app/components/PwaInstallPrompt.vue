<!--<template>-->
<!--  <div-->
<!--      v-if="showInstallPrompt"-->
<!--      class="fixed bottom-4 left-4 right-4 bg-white rounded-lg shadow-lg border p-4 z-50 animate-slide-up"-->
<!--  >-->
<!--    <div class="flex items-start space-x-3">-->
<!--      <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">-->
<!--        <Icon name="heroicons:arrow-down-tray" class="w-6 h-6 text-green-600" />-->
<!--      </div>-->
<!--      <div class="flex-1">-->
<!--        <h4 class="font-semibold text-gray-900">{{ $t('install.title') }}</h4>-->
<!--        <p class="text-sm text-gray-600 mt-1">{{ $t('install.description') }}</p>-->
<!--        <div class="flex space-x-3 mt-3">-->
<!--          <button-->
<!--              @click="installPWA"-->
<!--              class="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700"-->
<!--          >-->
<!--            {{ $t('install.install') }}-->
<!--          </button>-->
<!--          <button-->
<!--              @click="dismissPrompt"-->
<!--              class="text-gray-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-100"-->
<!--          >-->
<!--            {{ $t('install.later') }}-->
<!--          </button>-->
<!--        </div>-->
<!--      </div>-->
<!--      <button-->
<!--          @click="dismissPrompt"-->
<!--          class="text-gray-400 hover:text-gray-600"-->
<!--      >-->
<!--        <Icon name="heroicons:x-mark" class="w-5 h-5" />-->
<!--      </button>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted } from 'vue'-->

<!--const showInstallPrompt = ref(false)-->
<!--let deferredPrompt = null-->

<!--const installPWA = async () => {-->
<!--  if (deferredPrompt) {-->
<!--    deferredPrompt.prompt()-->
<!--    const { outcome } = await deferredPrompt.userChoice-->
<!--    console.log(`User response to the install prompt: ${outcome}`)-->
<!--    deferredPrompt = null-->
<!--    showInstallPrompt.value = false-->
<!--  }-->
<!--}-->

<!--const dismissPrompt = () => {-->
<!--  showInstallPrompt.value = false-->
<!--  // Sauvegarder le choix dans localStorage-->
<!--  localStorage.setItem('pwa-dismissed', 'true')-->
<!--}-->

<!--onMounted(() => {-->
<!--  // Vérifier si déjà installé-->
<!--  if (window.matchMedia('(display-mode: standalone)').matches) {-->
<!--    return-->
<!--  }-->

<!--  // Vérifier si déjà refusé-->
<!--  if (localStorage.getItem('pwa-dismissed') === 'true') {-->
<!--    return-->
<!--  }-->

<!--  // Écouter l'événement beforeinstallprompt-->
<!--  window.addEventListener('beforeinstallprompt', (e) => {-->
<!--    e.preventDefault()-->
<!--    deferredPrompt = e-->
<!--    showInstallPrompt.value = true-->
<!--  })-->

<!--  // En localhost, simuler l'événement pour tester-->
<!--  if (process.dev && window.location.port === '8080') {-->
<!--    setTimeout(() => {-->
<!--      if (!deferredPrompt) {-->
<!--        showInstallPrompt.value = true-->
<!--      }-->
<!--    }, 2000)-->
<!--  }-->
<!--})-->
<!--</script>-->

<!--<style scoped>-->
<!--@keyframes slide-up {-->
<!--  from {-->
<!--    transform: translateY(100%);-->
<!--    opacity: 0;-->
<!--  }-->
<!--  to {-->
<!--    transform: translateY(0);-->
<!--    opacity: 1;-->
<!--  }-->
<!--}-->

<!--.animate-slide-up {-->
<!--  animation: slide-up 0.3s ease-out;-->
<!--}-->
<!--</style>-->

<template>
  <div
      v-if="showInstallPrompt"
      class="fixed bottom-4 left-4 right-4 bg-white rounded-lg shadow-lg border p-4 z-50 animate-slide-up"
  >
    <div class="flex items-start space-x-3">
      <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
        <Icon name="heroicons:arrow-down-tray" class="w-6 h-6 text-green-600" />
      </div>
      <div class="flex-1">
        <h4 class="font-semibold text-gray-900">{{ $t('install.title') }}</h4>
        <p class="text-sm text-gray-600 mt-1">{{ $t('install.description') }}</p>
        <div class="flex space-x-3 mt-3">
          <button
              @click="install"
              class="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700"
          >
            {{ $t('install.install') }}
          </button>
          <button
              @click="dismiss"
              class="text-gray-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-100"
          >
            {{ $t('install.later') }}
          </button>
        </div>
      </div>
      <button
          @click="dismiss"
          class="text-gray-400 hover:text-gray-600"
      >
        <Icon name="heroicons:x-mark" class="w-5 h-5" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const showInstallPrompt = ref(false)
let deferredPrompt = null

onMounted(() => {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    deferredPrompt = e

    // Vérifier si déjà installé ou prompt déjà rejeté
    const dismissed = localStorage.getItem('pwa-install-dismissed')
    const isInstalled = window.matchMedia('(display-mode: standalone)').matches

    if (!dismissed && !isInstalled) {
      setTimeout(() => {
        showInstallPrompt.value = true
      }, 5000) // Attendre 5 secondes
    }
  })

  window.addEventListener('appinstalled', () => {
    showInstallPrompt.value = false
    deferredPrompt = null
  })
})

const install = async () => {
  if (deferredPrompt) {
    deferredPrompt.prompt()
    const { outcome } = await deferredPrompt.userChoice

    if (outcome === 'accepted') {
      console.log('PWA installée')
    }

    deferredPrompt = null
  }
  showInstallPrompt.value = false
}

const dismiss = () => {
  showInstallPrompt.value = false
  localStorage.setItem('pwa-install-dismissed', 'true')
}
</script>

<style scoped>
@keyframes slide-up {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}
</style>