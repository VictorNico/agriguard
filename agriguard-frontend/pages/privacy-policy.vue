<script setup>
const config = useRuntimeConfig()
const { t } = useI18n()
const router = useRouter();
const mobileMenuOpen = ref(false)
definePageMeta({
  layout: 'landing',
});
const goBack = () => {
  router.back();
};
</script>

<template>
  <div class="article-content policy-p relative isolate bg-white h-screen ">
    <button class=" px-4 py-2 rounded hover:bg-gray-600/10 flex items-center hui ml-4" @click="goBack"><svg
        xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
        <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
          d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
      </svg></button>
    <div class="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80" aria-hidden="true">
      <div
        class="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff3d3d] to-[#35f72e] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
        style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" />
    </div>
    <InternationalisationButtons />
    <h1 class="text-2xl font-bold mb-4 text-green-900 text-center">{{ t('rgpd.privacy.title') }}</h1>
    <p class="text-center pt font-semibold text-green-900/90">
      {{ t('rgpd.privacy.brand') }}
    </p>
    <h2 class="text-xl mt-4 text-gray-800">{{ t('rgpd.privacy.rule1.title') }}</h2>
    <p class="text-gray-800/90 pty font-semibold">{{ t('rgpd.privacy.rule1.text') }}</p>
    <h2 class="text-xl mt-4 text-gray-800">{{ t('rgpd.privacy.rule2.title') }}</h2>
    <p class="text-gray-800/90 pty font-semibold">{{ t('rgpd.privacy.rule2.text') }}</p>
    <h2 class="text-xl mt-4 text-gray-800">{{ t('rgpd.privacy.rule3.title') }}</h2>
    <p class="text-gray-800/90 pty font-semibold">{{ t('rgpd.privacy.rule3.text') }} <a
        :href="'mailto:' + config.public.supportEmail" class="text-blue-400 underline">{{ config.public.supportEmail
        }}</a>.
    </p>
  </div>
</template>


<style scoped>
.article-content p,
.article-content h2 {
  margin: 0 15vw;
}

.article-content {
  padding-top: 100px;
  font-family: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";

}

.article-content.policy-p h1 {
  font-size: 50px;
  line-height: 4rem;
}

.article-content.policy-p h1,
.article-content.policy-p .pt {
  margin: 25px 20vw;
}

.article-content.policy-p .pt {
  margin-bottom: 50px;
}

.article-content.policy-p h2 {
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 20px;
}

.article-content.policy-p .pty {
  margin-bottom: 50px;
}.article-content .hui {
    border-radius: 50%;
    height: 45px;
    position: fixed;
    top: 130px;
    left: 30px;
}

.article-content .hui svg {
    width: 20px;
}
</style>