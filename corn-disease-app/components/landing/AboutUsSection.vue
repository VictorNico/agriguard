<!-- components/AboutUsSection.vue -->
<template>
  <section id="about" class="py-16 bg-gradient-to-br from-green-50 to-yellow-50">
    <div class="container mx-auto px-4">
      <!-- En-tête de section -->
      <div class="text-center mb-12">
        <h2 class="text-3xl md:text-4xl font-bold text-green-800 mb-4">
          {{ t('about.title') }}
        </h2>
        <p class="text-xl text-green-600 max-w-3xl mx-auto">
          {{ t('about.subtitle') }}
        </p>
      </div>

      <!-- Contenu principal -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
        <!-- Texte -->
        <div class="space-y-6">
          <div class="prose prose-green max-w-none">
            <p class="text-lg text-gray-700 leading-relaxed">
              {{ t('about.description1') }}
            </p>
            <p class="text-lg text-gray-700 leading-relaxed">
              {{ t('about.description2') }}
            </p>
          </div>

          <!-- Statistiques -->
          <div class="grid grid-cols-2 gap-6 mt-8">
            <div class="text-center p-4 bg-white rounded-lg shadow-md">
              <div class="text-3xl font-bold text-green-600 mb-2">95%</div>
              <div class="text-sm text-gray-600">{{ t('about.accuracy') }}</div>
            </div>
            <div class="text-center p-4 bg-white rounded-lg shadow-md">
              <div class="text-3xl font-bold text-yellow-600 mb-2">50k+</div>
              <div class="text-sm text-gray-600">{{ t('about.farmers') }}</div>
            </div>
          </div>
        </div>

        <!-- Image/Illustration -->
        <div class="relative">
          <div class="bg-gradient-to-r from-green-400 to-yellow-400 rounded-2xl p-8 h-96 flex items-center justify-center">
            <div class="text-center text-white">
              <svg class="w-24 h-24 mx-auto mb-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
              </svg>
              <h3 class="text-2xl font-bold mb-2">{{ t('about.aiPowered') }}</h3>
              <p class="text-green-100">{{ t('about.aiDescription') }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Mission et Vision -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white p-8 rounded-xl shadow-lg">
          <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L15.09 8.26L22 9L15.09 9.74L12 16L8.91 9.74L2 9L8.91 8.26L12 2Z"/>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-green-800">{{ t('about.mission') }}</h3>
          </div>
          <p class="text-gray-700 leading-relaxed">
            {{ t('about.missionDescription') }}
          </p>
        </div>

        <div class="bg-white p-8 rounded-xl shadow-lg">
          <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-yellow-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-green-800">{{ t('about.vision') }}</h3>
          </div>
          <p class="text-gray-700 leading-relaxed">
            {{ t('about.visionDescription') }}
          </p>
        </div>
      </div>

      <!-- Équipe -->
      <div class="mt-16">
        <h3 class="text-2xl font-bold text-green-800 text-center mb-8">
          {{ t('about.team') }}
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center" v-for="member in teamMembers" :key="member.id">
            <div class="w-24 h-24 bg-gradient-to-r from-green-400 to-yellow-400 rounded-full mx-auto mb-4 flex items-center justify-center">
              <span class="text-white font-bold text-xl">{{ member.initials }}</span>
            </div>
            <h4 class="font-semibold text-green-800">{{ member.name }}</h4>
            <p class="text-gray-600">{{ member.role }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n()

const teamMembers = ref([
  {
    id: 1,
    name: t('about.teamMember1'),
    role: t('about.teamRole1'),
    initials: 'JK'
  },
  {
    id: 2,
    name: t('about.teamMember2'),
    role: t('about.teamRole2'),
    initials: 'AM'
  },
  {
    id: 3,
    name: t('about.teamMember3'),
    role: t('about.teamRole3'),
    initials: 'FK'
  }
])
</script>