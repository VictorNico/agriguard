<template>
  <div
      class="fixed bottom-0 left-0 right-0 bg-green-900 text-white p-4 flex flex-col items-center justify-between z-50 ff-a lg:flex-row kin"
  >
    <p class="text-sm text-center mb-2">
      {{ t('rgpd.consent.text1')}} <a href="/privacy-policy" class="text-green-400 underline">{{ t('rgpd.consent.text2')}}</a>.
    </p>
    <div class="downt">
      <button @click="acceptCookies" class="bg-green-500 text-white px-4 py-2 rounded mr-2">
        {{ t('rgpd.consent.btn1')}}
      </button>
      <button @click="declineCookies" class="bg-gray-500 text-white px-4 py-2 rounded">
        {{ t('rgpd.consent.btn2')}}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useCookie } from '#app';
// import Cookies from 'js-cookie';
const { t } = useI18n()
const cookieConsent = useCookie('cookie_consent');


const acceptCookies = () => {
  cookieConsent.value = 'true';
};

const declineCookies = () => {
  cookieConsent.value = 'false';
  // Supprime les cookies non essentiels
  // Cookies.remove('_ga'); // Exemple pour Google Analytics
  // Cookies.remove('_gid');
};
</script>


<style scoped>
.flex {
  display: flex;
}

.active {
  position: relative;
}

.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #22c55e;
}
.ff-a{
  font-family: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}
input,
select,
.p-component.p-inputwrapper,
button {
  height: 32px;
  font-size: 12px;
  max-width: 140px;
}

svg.p-icon.p-multiselect-dropdown-icon {
  width: 11px !important;
}

.p-datatable.p-component {
  font-size: .8em;
}

.router-link-active[data-v-433a9abd] {
  background-color: rgb(107 255 126 / 14%);
}

.p-datatable-scrollable-header,
.p-datatable-scrollable-body {
  overflow-x: auto !important;
  /* Défilement horizontal */
}

.p-datatable-scrollable-body {
  max-width: 100%;
}

.datatable-container {
  width: calc(100vw - 255px) !important;
}
.kin{
  background: rgba(15, 71, 9, 0.863);
    --globalnav-backdrop-filter: saturate(180%) blur(20px);
    backdrop-filter: saturate(180%) blur(20px);
    --globalnav-background: rgba(187, 236, 187, 0.22);
}

</style>
