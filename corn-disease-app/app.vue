<!-- app.vue -->
<template>
  <div id="app">
    <!-- Splash screen pour PWA -->
    <div v-if="showWebSplash" id="web-splash-screen" class="splash-screen">
      <div class="splash-content">
        <div class="splash-logo">
          <div class="corn-icon h-full flex items-center">
            <img
                src="/logo.png"
                alt="Logo"
                class="h-full w-auto max-h-full object-contain"
            />
          </div>
          <h1>Corn Disease Detection</h1>
          <p>Détection IA des maladies du maïs</p>
        </div>

        <div class="splash-progress-container">
          <div class="splash-progress-bar">
            <div
                class="splash-progress"
                :style="{ width: progress + '%' }"
            ></div>
          </div>
          <p class="splash-message">{{ message }}</p>
        </div>
      </div>
    </div>

    <!-- Contenu principal -->
    <div v-else>
        <CookieConsent v-if="!isConsentGiven" />
        <Toast/>
        <NuxtLayout>
          <NuxtPage />
        </NuxtLayout>
      </div>
  </div>
</template>

<script setup>
import { Capacitor } from '@capacitor/core'

const { isShowing, progress, message, loadingSequence } = useSplashScreen()

// État pour le splash screen web
const showWebSplash = ref(!Capacitor.isNativePlatform())

// Lancer la séquence de chargement
onMounted(async () => {
  if (!Capacitor.isNativePlatform()) {
    // Pour PWA, gérer le splash screen web
    await loadingSequence()
    showWebSplash.value = false
  }
})

// Surveiller les changements d'état
watch(isShowing, (newValue) => {
  if (!Capacitor.isNativePlatform()) {
    showWebSplash.value = newValue
  }
})

import {useToast} from "primevue/usetoast";

useHead({
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { key: 'theme-color', name: 'theme-color', content: 'light' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: 'fr'
  }
})

// manipulation de configuration d'execution - environement ...
const config = useRuntimeConfig()
import { useLocaleStore } from '~/stores/locale';

// Initialiser les stores et vue-i18n
const localeStore = useLocaleStore();
const { locale } = useI18n();

// Initialiser la langue d'i18n avec celle du store
locale.value = localeStore.language;

// Observer les changements de langue dans Pinia et synchroniser avec vue-i18n
watch(
    () => localeStore.language,
    (newLang) => {
      locale.value = newLang; // Synchronise la langue avec vue-i18n
    }
);

// Observer les changements de vue-i18n pour mettre à jour Pinia si nécessaire
watch(
    () => locale.value,
    (newLang) => {
      if (localeStore.language !== newLang) {
        localeStore.setLanguage(newLang); // Synchronise Pinia si i18n change
      }
    }
);

// useSeoMeta({
//   title,
//   description,
//   ogTitle: title,
//   ogDescription: description,
//   ogImage: `${config.public.serverUrl}/logo.png`,
//   twitterImage: `${config.public.serverUrl}/logo.png`,
//   twitterCard: 'summary_large_image'
// })

import { useAuthStore } from '~/stores/auth';

const auth = useAuthStore()
const toast = useToast();
const { t } = useI18n()
// console.log(auth.user,auth.token,auth.isAuthenticated);
const dd = auth.ValidateToken()
// console.log('token',dd);
if(dd === 0){
  toast.add({ severity: 'info', summary: t('expiredSession'), life: 7000 });
}

import { useCookie } from '#app';

const cookieConsent = useCookie('cookie_consent');
console.log(cookieConsent.value);
const isConsentGiven = computed(()=> cookieConsent.value);

console.log(isConsentGiven.value);
</script>

<style scoped>
.splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ffffff 0%, #2E7D32 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  transition: opacity 0.5s ease-out;
}

.splash-content {
  text-align: center;
  color: white;
  max-width: 300px;
}

.splash-logo {
  margin-bottom: 3rem;
}

.corn-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: bounce 2s infinite;
}

.splash-logo h1 {
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
  font-weight: bold;
}

.splash-logo p {
  font-size: 1rem;
  margin: 0;
  opacity: 0.9;
}

.splash-progress-container {
  margin-top: 2rem;
}

.splash-progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.splash-progress {
  height: 100%;
  background: white;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.splash-message {
  font-size: 0.9rem;
  margin: 0;
  opacity: 0.8;
  min-height: 1.2rem;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .splash-content {
    max-width: 250px;
  }

  .corn-icon {
    font-size: 3rem;
  }

  .splash-logo h1 {
    font-size: 1.5rem;
  }
}
/* width */
::-webkit-scrollbar {
  width: 8px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #d5e4d281;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #a6c0a6;
  border-radius: 5px;
}
::-webkit-scrollbar:horizontal {
  height: 8px; /* Modifier la hauteur selon tes besoins */
}
/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>