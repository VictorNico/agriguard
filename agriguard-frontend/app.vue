<template>
  <div>
    <CookieConsent v-if="!isConsentGiven" />
    <Toast/>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
<script setup lang="ts">
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

<style>
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