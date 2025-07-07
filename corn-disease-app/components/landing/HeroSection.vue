<template>
  <div class="relative bg-white overflow-hidden">
    <div class="max-w-7xl mx-auto">
      <div class="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
        <div class="pt-10 sm:pt-16 lg:pt-8 lg:pb-14 lg:overflow-hidden">
          <div class="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div class="sm:text-center lg:text-left">
              <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                <span class="block">{{ $t('hero.title_part1') }}</span>
                <span class="block text-purple-700">{{ $t('hero.title_part2') }}</span>
              </h1>
              <p class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                {{ $t('hero.description') }}
              </p>
              <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div class="rounded-md shadow">
                  <NuxtLink
                      href="/analyze"
                      class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-green-700 hover:bg-green-800 md:py-4 md:text-lg md:px-10"
                  >
                    <Icon name="heroicons:play-circle" class="mr-2 font-medium md:text-lg" />
                    {{ $t('hero.demo_button') }}
                  </NuxtLink>
                </div>
                <div class="mt-3 sm:mt-0 sm:ml-3">
                  <NuxtLink
                      href="#"
                      class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-green-700 bg-green-300/10 hover:bg-opacity-90 md:py-4 md:text-lg md:px-10"
                  >
                    <Icon name="heroicons:device-phone-mobile" class="mr-2 text-green-250" />
                    {{ $t('hero.download_button') }}
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
      <img
          class="h-56 w-full object-center sm:h-72 md:h-96 lg:w-full lg:h-full"
          src="/img2.png"
          :alt="t('hero.image_alt')"
          loading="lazy"
      />
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()
</script>