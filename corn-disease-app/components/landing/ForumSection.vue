<!-- components/ForumSection.vue -->
<template>
  <section id="forum" class="py-16 bg-white">
    <div class="container mx-auto px-4">
      <!-- En-tête de section -->
      <div class="text-center mb-12">
        <h2 class="text-3xl md:text-4xl font-bold text-green-800 mb-4">
          {{ t('forum.title') }}
        </h2>
        <p class="text-xl text-green-600 max-w-2xl mx-auto">
          {{ t('forum.subtitle') }}
        </p>
      </div>

      <!-- Stats du Forum -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <div class="text-center p-6 bg-green-50 rounded-xl">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <div class="text-2xl font-bold text-green-800">{{ t('forum.stats.members') }}</div>
          <div class="text-sm text-gray-600">{{ t('forum.stats.activeFarmers') }}</div>
        </div>

        <div class="text-center p-6 bg-yellow-50 rounded-xl">
          <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-yellow-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20 6L9 17l-5-5 1.41-1.41L9 14.17l9.59-9.58L20 6z"/>
            </svg>
          </div>
          <div class="text-2xl font-bold text-yellow-700">{{ t('forum.stats.solved') }}</div>
          <div class="text-sm text-gray-600">{{ t('forum.stats.problemsSolved') }}</div>
        </div>

        <div class="text-center p-6 bg-blue-50 rounded-xl">
          <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
          </div>
          <div class="text-2xl font-bold text-blue-700">{{ t('forum.stats.discussions') }}</div>
          <div class="text-sm text-gray-600">{{ t('forum.stats.activeDiscussions') }}</div>
        </div>

        <div class="text-center p-6 bg-purple-50 rounded-xl">
          <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M9 11H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm2-7h-1V2h-2v2H8V2H6v2H5c-1.1 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z"/>
            </svg>
          </div>
          <div class="text-2xl font-bold text-purple-700">{{ t('forum.stats.daily') }}</div>
          <div class="text-sm text-gray-600">{{ t('forum.stats.dailyPosts') }}</div>
        </div>
      </div>

      <!-- Discussions récentes -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <div>
          <h3 class="text-xl font-bold text-green-800 mb-6">{{ t('forum.recentDiscussions') }}</h3>
          <div class="space-y-4">
            <div v-for="discussion in recentDiscussions" :key="discussion.id"
                 class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div class="flex items-start space-x-3">
                <div class="w-10 h-10 bg-gradient-to-r from-green-400 to-yellow-400 rounded-full flex items-center justify-center">
                  <span class="text-white font-medium text-sm">{{ discussion.author.initials }}</span>
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-gray-900 mb-1">{{ discussion.title }}</h4>
                  <p class="text-sm text-gray-600 mb-2">{{ discussion.excerpt }}</p>
                  <div class="flex items-center space-x-4 text-xs text-gray-500">
                    <span>{{ discussion.author.name }}</span>
                    <span>{{ discussion.date }}</span>
                    <span class="flex items-center space-x-1">
                      <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                      </svg>
                      <span>{{ discussion.replies }}</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Catégories populaires -->
        <div>
          <h3 class="text-xl font-bold text-green-800 mb-6">{{ t('forum.popularCategories') }}</h3>
          <div class="grid grid-cols-1 gap-4">
            <div v-for="category in categories" :key="category.id"
                 class="bg-gradient-to-r from-green-50 to-yellow-50 p-4 rounded-lg border border-green-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
                    </svg>
                  </div>
                  <div>
                    <h4 class="font-semibold text-green-800">{{ category.name }}</h4>
                    <p class="text-sm text-gray-600">{{ category.description }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-sm font-medium text-green-600">{{ category.posts }}</div>
                  <div class="text-xs text-gray-500">{{ t('forum.posts') }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="text-center bg-gradient-to-r from-green-100 to-yellow-100 p-8 rounded-xl">
        <h3 class="text-2xl font-bold text-green-800 mb-4">
          {{ t('forum.joinCommunity') }}
        </h3>
        <p class="text-green-600 mb-6 max-w-2xl mx-auto">
          {{ t('forum.joinDescription') }}
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <NuxtLink
              to="/forum"
              class="bg-green-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-green-700 transition-colors inline-flex items-center justify-center space-x-2"
          >
            <span>{{ t('forum.browseForum') }}</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </NuxtLink>
          <button
              class="bg-white text-green-600 px-8 py-3 rounded-lg font-medium border border-green-600 hover:bg-green-50 transition-colors"
          >
            {{ t('forum.askQuestion') }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n()

const recentDiscussions = ref([
  {
    id: 1,
    title: t('forum.discussions.discussion1.title'),
    excerpt: t('forum.discussions.discussion1.excerpt'),
    author: {
      name: 'Mwalimu Juma',
      initials: 'MJ'
    },
    date: '2h ago',
    replies: 12
  },
  {
    id: 2,
    title: t('forum.discussions.discussion2.title'),
    excerpt: t('forum.discussions.discussion2.excerpt'),
    author: {
      name: 'Fatuma Hassan',
      initials: 'FH'
    },
    date: '4h ago',
    replies: 8
  },
  {
    id: 3,
    title: t('forum.discussions.discussion3.title'),
    excerpt: t('forum.discussions.discussion3.excerpt'),
    author: {
      name: 'Ahmed Mwangi',
      initials: 'AM'
    },
    date: '1d ago',
    replies: 15
  }
])

const categories = ref([
  {
    id: 1,
    name: t('forum.categories.diseases'),
    description: t('forum.categories.diseasesDesc'),
    posts: 234
  },
  {
    id: 2,
    name: t('forum.categories.prevention'),
    description: t('forum.categories.preventionDesc'),
    posts: 156
  },
  {
    id: 3,
    name: t('forum.categories.treatment'),
    description: t('forum.categories.treatmentDesc'),
    posts: 189
  },
  {
    id: 4,
    name: t('forum.categories.general'),
    description: t('forum.categories.generalDesc'),
    posts: 98
  }
])
</script>