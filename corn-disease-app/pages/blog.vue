<!-- pages/blog.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-yellow-50">
    <!-- Header -->
    <div class="bg-gradient-to-r from-green-600 to-green-700 text-white py-16">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          {{ t('blog.pageTitle') }}
        </h1>
        <p class="text-xl text-green-100 max-w-3xl mx-auto">
          {{ t('blog.pageSubtitle') }}
        </p>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="container mx-auto px-4 py-8">
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- Search -->
        <div class="flex-1">
          <div class="relative">
            <input
                v-model="searchQuery"
                type="text"
                :placeholder="t('blog.searchPlaceholder')"
                class="w-full px-6 py-3 border-2 border-green-200 rounded-xl focus:outline-none focus:border-green-500 transition-colors"
            />
            <div class="absolute right-4 top-1/2 transform -translate-y-1/2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Category Filter -->
        <div class="lg:w-64">
          <select
              v-model="selectedCategory"
              class="w-full px-4 py-3 border-2 border-green-200 rounded-xl focus:outline-none focus:border-green-500 transition-colors"
          >
            <option value="all">{{ t('blog.categories.all') }}</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ t(`blog.categories.${category}`) }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Featured Article -->
    <div v-if="featuredArticle && !searchQuery" class="container mx-auto px-4 pb-12">
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div class="order-2 lg:order-1 p-8">
            <div class="flex items-center mb-4">
              <span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                {{ t('blog.featured') }}
              </span>
              <span class="ml-3 text-gray-500 text-sm">{{ formatDate(featuredArticle.date) }}</span>
            </div>
            <h2 class="text-3xl font-bold text-green-800 mb-4">
              {{ t(featuredArticle.title) }}
            </h2>
            <p class="text-gray-600 mb-6 leading-relaxed">
              {{ t(featuredArticle.excerpt) }}
            </p>
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">
                  {{ featuredArticle.author.charAt(0) }}
                </div>
                <div class="ml-3">
                  <p class="font-medium text-gray-800">{{ featuredArticle.author }}</p>
                  <p class="text-sm text-gray-500">{{ t('blog.readTime', { minutes: featuredArticle.readTime }) }}</p>
                </div>
              </div>
              <button class="bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 transition-colors">
                {{ t('blog.readMore') }}
              </button>
            </div>
          </div>
          <div class="order-1 lg:order-2 h-64 lg:h-auto bg-gradient-to-br from-green-400 to-yellow-400 flex items-center justify-center">
            <div class="text-white text-center">
              <svg class="w-24 h-24 mx-auto mb-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
              </svg>
              <p class="text-lg font-semibold">{{ t('blog.featuredImage') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Articles Grid -->
    <div class="container mx-auto px-4 pb-16">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <article
            v-for="article in filteredArticles"
            :key="article.id"
            class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow cursor-pointer"
            @click="navigateToArticle(article.slug)"
        >
          <!-- Article Image -->
          <div class="h-48 bg-gradient-to-br from-green-400 to-yellow-400 flex items-center justify-center">
            <div class="text-white text-center">
              <svg class="w-16 h-16 mx-auto mb-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
              </svg>
            </div>
          </div>

          <!-- Article Content -->
          <div class="p-6">
            <div class="flex items-center mb-3">
              <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                {{ t(`blog.categories.${article.category}`) }}
              </span>
              <span class="ml-2 text-gray-500 text-sm">{{ formatDate(article.date) }}</span>
            </div>

            <h3 class="text-xl font-bold text-green-800 mb-3 line-clamp-2">
              {{ t(article.title) }}
            </h3>

            <p class="text-gray-600 mb-4 line-clamp-3">
              {{ t(article.excerpt) }}
            </p>

            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                  {{ article.author.charAt(0) }}
                </div>
                <div class="ml-2">
                  <p class="text-sm font-medium text-gray-800">{{ article.author }}</p>
                  <p class="text-xs text-gray-500">{{ t('blog.readTime', { minutes: article.readTime }) }}</p>
                </div>
              </div>
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </div>
          </div>
        </article>
      </div>

      <!-- No Results -->
      <div v-if="filteredArticles.length === 0" class="text-center py-12">
        <div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
          <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9.5a2 2 0 00-2-2h-1"/>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-700 mb-2">{{ t('blog.noResults') }}</h3>
        <p class="text-gray-500">{{ t('blog.tryDifferentSearch') }}</p>
      </div>

      <!-- Load More Button -->
      <div v-if="filteredArticles.length > 0 && hasMore" class="text-center mt-12">
        <button
            @click="loadMore"
            class="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
        >
          {{ t('blog.loadMore') }}
        </button>
      </div>
    </div>

    <!-- Newsletter Signup -->
    <div class="bg-white py-16">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold text-green-800 mb-4">
          {{ t('blog.newsletter.title') }}
        </h2>
        <p class="text-gray-600 mb-8 max-w-2xl mx-auto">
          {{ t('blog.newsletter.description') }}
        </p>
        <div class="max-w-md mx-auto flex gap-4">
          <input
              v-model="newsletterEmail"
              type="email"
              :placeholder="t('blog.newsletter.placeholder')"
              class="flex-1 px-4 py-3 border-2 border-green-200 rounded-lg focus:outline-none focus:border-green-500 transition-colors"
          />
          <button
              @click="subscribeNewsletter"
              class="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
          >
            {{ t('blog.newsletter.subscribe') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
const router = useRouter()

// SEO Meta
useHead({
  title: computed(() => t('blog.metaTitle')),
  meta: [
    {
      name: 'description',
      content: computed(() => t('blog.metaDescription'))
    }
  ]
})

// Reactive data
const searchQuery = ref('')
const selectedCategory = ref('all')
const newsletterEmail = ref('')
const hasMore = ref(true)

// Categories
const categories = ['diseases', 'prevention', 'treatment', 'farming', 'research', 'technology']

// Sample articles data
const articlesData = ref([
  {
    id: 1,
    title: 'blog.articles.article1.title',
    excerpt: 'blog.articles.article1.excerpt',
    category: 'diseases',
    author: 'Dr. John Mwangi',
    date: '2024-01-15',
    readTime: 5,
    slug: 'common-maize-diseases-tanzania',
    featured: true
  },
  {
    id: 2,
    title: 'blog.articles.article2.title',
    excerpt: 'blog.articles.article2.excerpt',
    category: 'prevention',
    author: 'Sarah Johnson',
    date: '2024-01-10',
    readTime: 3,
    slug: 'early-detection-techniques'
  },
  {
    id: 3,
    title: 'blog.articles.article3.title',
    excerpt: 'blog.articles.article3.excerpt',
    category: 'treatment',
    author: 'Prof. Ahmed Hassan',
    date: '2024-01-05',
    readTime: 7,
    slug: 'sustainable-treatment-methods'
  },
  {
    id: 4,
    title: 'blog.articles.article4.title',
    excerpt: 'blog.articles.article4.excerpt',
    category: 'farming',
    author: 'Mary Kimani',
    date: '2024-01-01',
    readTime: 4,
    slug: 'best-farming-practices'
  },
  {
    id: 5,
    title: 'blog.articles.article5.title',
    excerpt: 'blog.articles.article5.excerpt',
    category: 'technology',
    author: 'Tech Team',
    date: '2023-12-28',
    readTime: 6,
    slug: 'ai-maize-disease-detection'
  },
  {
    id: 6,
    title: 'blog.articles.article6.title',
    excerpt: 'blog.articles.article6.excerpt',
    category: 'research',
    author: 'Dr. Grace Mbeki',
    date: '2023-12-20',
    readTime: 8,
    slug: 'climate-change-impact'
  }
])

// Computed
const featuredArticle = computed(() => {
  return articlesData.value.find(article => article.featured)
})

const filteredArticles = computed(() => {
  let filtered = articlesData.value.filter(article => !article.featured)

  // Filter by category
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(article => article.category === selectedCategory.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(article =>
        t(article.title).toLowerCase().includes(query) ||
        t(article.excerpt).toLowerCase().includes(query) ||
        article.author.toLowerCase().includes(query)
    )
  }

  return filtered
})

// Methods
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const navigateToArticle = (slug: string) => {
  router.push(`/blog/${slug}`)
}

const loadMore = () => {
  // Simulate loading more articles
  hasMore.value = false
}

const subscribeNewsletter = () => {
  if (newsletterEmail.value) {
    // Handle newsletter subscription
    console.log('Subscribing email:', newsletterEmail.value)
    newsletterEmail.value = ''
    // Show success message
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>