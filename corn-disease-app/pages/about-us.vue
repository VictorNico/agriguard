<!-- pages/about-us.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-yellow-50">
    <!-- Header -->
    <div class="bg-gradient-to-r from-green-600 to-green-700 text-white py-16">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          {{ t('aboutUs.pageTitle') }}
        </h1>
        <p class="text-xl text-green-100 max-w-3xl mx-auto">
          {{ t('aboutUs.pageSubtitle') }}
        </p>
      </div>
    </div>

    <!-- Contenu principal -->
    <div class="container mx-auto px-4 py-16">
      <!-- Histoire et Mission -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
        <div>
          <h2 class="text-3xl font-bold text-green-800 mb-6">{{ t('aboutUs.ourStory') }}</h2>
          <div class="space-y-4 text-gray-700">
            <p class="text-lg leading-relaxed">
              {{ t('aboutUs.story1') }}
            </p>
            <p class="text-lg leading-relaxed">
              {{ t('aboutUs.story2') }}
            </p>
            <p class="text-lg leading-relaxed">
              {{ t('aboutUs.story3') }}
            </p>
          </div>
        </div>

        <div class="relative">
          <div class="bg-gradient-to-r from-green-400 to-yellow-400 rounded-2xl p-8 h-96 flex items-center justify-center">
            <div class="text-center text-white">
              <svg class="w-32 h-32 mx-auto mb-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
              </svg>
              <h3 class="text-2xl font-bold mb-2">{{ t('aboutUs.innovationTitle') }}</h3>
              <p class="text-green-100">{{ t('aboutUs.innovationDesc') }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Mission, Vision, Valeurs -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
        <div class="bg-white p-8 rounded-xl shadow-lg text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L15.09 8.26L22 9L15.09 9.74L12 16L8.91 9.74L2 9L8.91 8.26L12 2Z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-green-800 mb-4">{{ t('aboutUs.mission') }}</h3>
          <p class="text-gray-700 leading-relaxed">
            {{ t('aboutUs.missionFull') }}
          </p>
        </div>

        <div class="bg-white p-8 rounded-xl shadow-lg text-center">
          <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-8 h-8 text-yellow-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-green-800 mb-4">{{ t('aboutUs.vision') }}</h3>
          <p class="text-gray-700 leading-relaxed">
            {{ t('aboutUs.visionFull') }}
          </p>
        </div>

        <div class="bg-white p-8 rounded-xl shadow-lg text-center">
          <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-green-800 mb-4">{{ t('aboutUs.values') }}</h3>
          <p class="text-gray-700 leading-relaxed">
            {{ t('aboutUs.valuesFull') }}
          </p>
        </div>
      </div>

      <!-- Statistiques détaillées -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-16">
        <h2 class="text-3xl font-bold text-green-800 text-center mb-8">
          {{ t('aboutUs.impact') }}
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="text-4xl font-bold text-green-600 mb-2">50,000+</div>
            <div class="text-gray-600">{{ t('aboutUs.farmers') }}</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold text-yellow-600 mb-2">95%</div>
            <div class="text-gray-600">{{ t('aboutUs.accuracy') }}</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold text-blue-600 mb-2">1M+</div>
            <div class="text-gray-600">{{ t('aboutUs.diagnoses') }}</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold text-purple-600 mb-2">15</div>
            <div class="text-gray-600">{{ t('aboutUs.regions') }}</div>
          </div>
        </div>
      </div>

      <!-- Équipe détaillée -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-green-800 text-center mb-8">
          {{ t('aboutUs.meetTeam') }}
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="member in teamMembers" :key="member.id"
               class="bg-white rounded-xl shadow-lg p-6 text-center hover:shadow-xl transition-shadow">
            <div class="w-24 h-24 bg-gradient-to-r from-green-400 to-yellow-400 rounded-full mx-auto mb-4 flex items-center justify-center">
              <span class="text-white font-bold text-xl">{{ member.initials }}</span>
            </div>
            <h3 class="text-xl font-bold text-green-800 mb-2">{{ member.name }}</h3>
            <p class="text-green-600 font-medium mb-3">{{ member.role }}</p>
            <p class="text-gray-600 text-sm leading-relaxed">{{ member.bio }}</p>
            <div class="flex justify-center space-x-3 mt-4">
              <a href="#" class="text-green-600 hover:text-green-700">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"/>
                </svg>
              </a>
              <a href="#" class="text-green-600 hover:text-green-700">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Partenaires -->
      <div class="bg-white rounded-2xl shadow-lg p-8">
        <h2 class="text-3xl font-bold text-green-800 text-center mb-8">
          {{ t('aboutUs.partners') }}
        </h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 opacity-60">
          <div class="flex items-center justify-center h-20 bg-gray-100 rounded-lg">
            <span class="text-gray-500 font-medium">{{ t('aboutUs.partner1') }}</span>
          </div>
          <div class="flex items-center justify-center h-20 bg-gray-100 rounded-lg">
            <span class="text-gray-500 font-medium">{{ t('aboutUs.partner2') }}</span>
          </div>
          <div class="flex items-center justify-center h-20 bg-gray-100 rounded-lg">
            <span class="text-gray-500 font-medium">{{ t('aboutUs.partner3') }}</span>
          </div>
          <div class="flex items-center justify-center h-20 bg-gray-100 rounded-lg">
            <span class="text-gray-500 font-medium">{{ t('aboutUs.partner4') }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

// SEO Meta
useHead({
  title: computed(() => t('aboutUs.metaTitle')),
  meta: [
    {
      name: 'description',
      content: computed(() => t('aboutUs.metaDescription'))
    }
  ]
})

const teamMembers = ref([
  {
    id: 1,
    name: t('aboutUs.team.member1.name'),
    role: t('aboutUs.team.member1.role'),
    bio: t('aboutUs.team.member1.bio'),
    initials: 'JK'
  },
  {
    id: 2,
    name: t('aboutUs.team.member2.name'),
    role: t('aboutUs.team.member2.role'),
    bio: t('aboutUs.team.member2.bio'),
    initials: 'AM'
  },
  {
    id: 3,
    name: t('aboutUs.team.member3.name'),
    role: t('aboutUs.team.member3.role'),
    bio: t('aboutUs.team.member3.bio'),
    initials: 'FK'
  },
  {
    id: 4,
    name: t('aboutUs.team.member4.name'),
    role: t('aboutUs.team.member4.role'),
    bio: t('aboutUs.team.member4.bio'),
    initials: 'SM'
  },
  {
    id: 5,
    name: t('aboutUs.team.member5.name'),
    role: t('aboutUs.team.member5.role'),
    bio: t('aboutUs.team.member5.bio'),
    initials: 'RN'
  },
  {
    id: 6,
    name: t('aboutUs.team.member6.name'),
    role: t('aboutUs.team.member6.role'),
    bio: t('aboutUs.team.member6.bio'),
    initials: 'LM'
  }
])
</script>