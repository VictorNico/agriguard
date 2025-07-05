<!-- pages/forum.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-gradient-to-r from-green-600 to-green-700 text-white py-12">
      <div class="container mx-auto px-4">
        <div class="flex flex-col lg:flex-row items-center justify-between">
          <div>
            <h1 class="text-4xl font-bold mb-2">
              {{ t('forum.pageTitle') }}
            </h1>
            <p class="text-green-100 text-lg">
              {{ t('forum.pageSubtitle') }}
            </p>
          </div>
          <div class="mt-6 lg:mt-0 flex gap-4">
            <button
                @click="showCreatePost = true"
                class="bg-white text-green-600 px-6 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors"
            >
              {{ t('forum.createPost') }}
            </button>
            <button class="bg-green-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-400 transition-colors">
              {{ t('forum.joinCommunity') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Forum Stats -->
    <div class="bg-white border-b">
      <div class="container mx-auto px-4 py-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="text-2xl font-bold text-green-600">{{ forumStats.totalPosts }}</div>
            <div class="text-sm text-gray-600">{{ t('forum.stats.totalPosts') }}</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-blue-600">{{ forumStats.activeUsers }}</div>
            <div class="text-sm text-gray-600">{{ t('forum.stats.activeUsers') }}</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-purple-600">{{ forumStats.totalTopics }}</div>
            <div class="text-sm text-gray-600">{{ t('forum.stats.totalTopics') }}</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-yellow-600">{{ forumStats.expertsOnline }}</div>
            <div class="text-sm text-gray-600">{{ t('forum.stats.expertsOnline') }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Categories Sidebar -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow-sm p-6 sticky top-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">{{ t('forum.categories.title') }}</h3>
            <div class="space-y-2">
              <button
                  v-for="category in categories"
                  :key="category.id"
                  @click="selectedCategory = category.id"
                  :class="[
                  'w-full text-left px-4 py-3 rounded-lg transition-colors flex items-center justify-between',
                  selectedCategory === category.id
                    ? 'bg-green-100 text-green-700 font-medium'
                    : 'hover:bg-gray-50 text-gray-700'
                ]"
              >
                <div class="flex items-center">
                  <span class="mr-3">{{ category.icon }}</span>
                  <span>{{ t(category.name) }}</span>
                </div>
                <span class="text-sm text-gray-500">{{ category.postCount }}</span>
              </button>
            </div>

            <!-- Online Users -->
            <div class="mt-8">
              <h4 class="text-md font-semibold text-gray-800 mb-4">{{ t('forum.onlineUsers') }}</h4>
              <div class="space-y-2">
                <div v-for="user in onlineUsers" :key="user.id" class="flex items-center">
                  <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white text-sm font-bold mr-3">
                    {{ user.name.charAt(0) }}
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-800">{{ user.name }}</div>
                    <div class="text-xs text-gray-500">{{ user.role }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Posts Feed -->
        <div class="lg:col-span-3">
          <!-- Search and Filter -->
          <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
            <div class="flex flex-col md:flex-row gap-4">
              <div class="flex-1">
                <input
                    v-model="searchQuery"
                    type="text"
                    :placeholder="t('forum.searchPlaceholder')"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
              <div class="flex gap-2">
                <select
                    v-model="sortBy"
                    class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="latest">{{ t('forum.sort.latest') }}</option>
                  <option value="popular">{{ t('forum.sort.popular') }}</option>
                  <option value="answered">{{ t('forum.sort.answered') }}</option>
                  <option value="unanswered">{{ t('forum.sort.unanswered') }}</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Posts List -->
          <div class="space-y-4">
            <div
                v-for="post in filteredPosts"
                :key="post.id"
                class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                @click="navigateToPost(post.id)"
            >
              <div class="p-6">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-2">
                      <span
                          :class="[
                          'px-3 py-1 rounded-full text-xs font-medium mr-3',
                          getCategoryColor(post.category)
                        ]"
                      >
                        {{ t(`forum.categories.${post.category}`) }}
                      </span>
                      <span v-if="post.isPinned" class="text-yellow-500 mr-2">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M16,12V4H17V2H7V4H8V12L6,14V16H11.2V22H12.8V16H18V14L16,12Z" />
                        </svg>
                      </span>
                      <span v-if="post.isAnswered" class="text-green-500 mr-2">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M9,20.42L2.79,14.21L5.62,11.38L9,14.77L18.88,4.88L21.71,7.71L9,20.42Z" />
                        </svg>
                      </span>
                    </div>

                    <h3 class="text-xl font-semibold text-gray-800 mb-2 hover:text-green-600 transition-colors">
                      {{ t(post.title) }}
                    </h3>

                    <p class="text-gray-600 mb-4 line-clamp-2">
                      {{ t(post.excerpt) }}
                    </p>

                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white text-sm font-bold mr-3">
                          {{ post.author.charAt(0) }}
                        </div>
                        <div>
                          <div class="text-sm font-medium text-gray-800">{{ post.author }}</div>
                          <div class="text-xs text-gray-500">{{ formatDate(post.createdAt) }}</div>
                        </div>
                      </div>

                      <div class="flex items-center space-x-4 text-sm text-gray-500">
                        <div class="flex items-center">
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                          </svg>
                          {{ post.repliesCount }}
                        </div>
                        <div class="flex items-center">
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                          </svg>
                          {{ post.views }}
                        </div>
                        <div class="flex items-center">
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                          </svg>
                          {{ post.likes }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Load More -->
          <div v-if="hasMorePosts" class="text-center mt-8">
            <button
                @click="loadMorePosts"
                class="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
            >
              {{ t('forum.loadMore') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Post Modal -->
    <div v-if="showCreatePost" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-800">{{ t('forum.createPost') }}</h2>
            <button @click="showCreatePost = false" class="text-gray-500 hover:text-gray-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <form @submit.prevent="submitPost" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('forum.postTitle') }}</label>
              <input
                  v-model="newPost.title"
                  type="text"
                  :placeholder="t('forum.postTitlePlaceholder')"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('forum.category') }}</label>
              <select
                  v-model="newPost.category"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  required
              >
                <option value="">{{ t('forum.selectCategory') }}</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ t(category.name) }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('forum.postContent') }}</label>
              <textarea
                  v-model="newPost.content"
                  :placeholder="t('forum.postContentPlaceholder')"
                  rows="8"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  required
              ></textarea>
            </div>

            <div class="flex items-center space-x-4">
              <label class="flex items-center">
                <input v-model="newPost.isQuestion" type="checkbox" class="mr-2">
                <span class="text-sm text-gray-700">{{ t('forum.markAsQuestion') }}</span>
              </label>
            </div>

            <div class="flex justify-end space-x-4">
              <button
                  type="button"
                  @click="showCreatePost = false"
                  class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                {{ t('forum.cancel') }}
              </button>
              <button
                  type="submit"
                  class="px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors"
              >
                {{ t('forum.publishPost') }}
              </button>
            </div>
          </form>
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
  title: computed(() => t('forum.metaTitle')),
  meta: [
    {
      name: 'description',
      content: computed(() => t('forum.metaDescription'))
    }
  ]
})

// Reactive data
const searchQuery = ref('')
const selectedCategory = ref('all')
const sortBy = ref('latest')
const showCreatePost = ref(false)
const hasMorePosts = ref(true)

// New post form
const newPost = ref({
  title: '',
  category: '',
  content: '',
  isQuestion: false
})

// Forum stats
const forumStats = ref({
  totalPosts: '2,847',
  activeUsers: '234',
  totalTopics: '89',
  expertsOnline: '12'
})

// Categories
const categories = ref([
  {
    id: 'all',
    name: 'forum.categories.all',
    icon: '🏠',
    postCount: 2847
  },
  {
    id: 'diseases',
    name: 'forum.categories.diseases',
    icon: '🦠',
    postCount: 856
  },
  {
    id: 'diagnosis',
    name: 'forum.categories.diagnosis',
    icon: '🔍',
    postCount: 634
  },
  {
    id: 'treatment',
    name: 'forum.categories.treatment',
    icon: '💊',
    postCount: 423
  },
  {
    id: 'prevention',
    name: 'forum.categories.prevention',
    icon: '🛡️',
    postCount: 398
  },
  {
    id: 'farming',
    name: 'forum.categories.farming',
    icon: '🌾',
    postCount: 312
  },
  {
    id: 'general',
    name: 'forum.categories.general',
    icon: '💬',
    postCount: 224
  }
])

// Online users
const onlineUsers = ref([
  { id: 1, name: 'Dr. John Mwangi', role: 'Expert' },
  { id: 2, name: 'Sarah Johnson', role: 'Farmer' },
  { id: 3, name: 'Ahmed Hassan', role: 'Researcher' },
  { id: 4, name: 'Mary Kimani', role: 'Agronomist' }
])

// Sample posts
const postsData = ref([
  {
    id: 1,
    title: 'forum.posts.post1.title',
    excerpt: 'forum.posts.post1.excerpt',
    category: 'diseases',
    author: 'Dr. John Mwangi',
    createdAt: '2024-01-15T10:30:00Z',
    repliesCount: 23,
    views: 456,
    likes: 34,
    isAnswered: true,
    isPinned: true
  },
  {
    id: 2,
    title: 'forum.posts.post2.title',
    excerpt: 'forum.posts.post2.excerpt',
    category: 'diagnosis',
    author: 'Sarah Johnson',
    createdAt: '2024-01-14T15:45:00Z',
    repliesCount: 12,
    views: 234,
    likes: 18,
    isAnswered: false,
    isPinned: false
  },
  {
    id: 3,
    title: 'forum.posts.post3.title',
    excerpt: 'forum.posts.post3.excerpt',
    category: 'treatment',
    author: 'Ahmed Hassan',
    createdAt: '2024-01-13T08:20:00Z',
    repliesCount: 8,
    views: 189,
    likes: 12,
    isAnswered: true,
    isPinned: false
  },
  {
    id: 4,
    title: 'forum.posts.post4.title',
    excerpt: 'forum.posts.post4.excerpt',
    category: 'prevention',
    author: 'Mary Kimani',
    createdAt: '2024-01-12T14:10:00Z',
    repliesCount: 15,
    views: 298,
    likes: 25,
    isAnswered: false,
    isPinned: false
  },
  {
    id: 5,
    title: 'forum.posts.post5.title',
    excerpt: 'forum.posts.post5.excerpt',
    category: 'farming',
    author: 'Peter Njoroge',
    createdAt: '2024-01-11T11:55:00Z',
    repliesCount: 6,
    views: 145,
    likes: 9,
    isAnswered: true,
    isPinned: false
  }
])

// Computed
const filteredPosts = computed(() => {
  let filtered = postsData.value

  // Filter by category
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(post => post.category === selectedCategory.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(post =>
        t(post.title).toLowerCase().includes(query) ||
        t(post.excerpt).toLowerCase().includes(query) ||
        post.author.toLowerCase().includes(query)
    )
  }

  // Sort posts
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'popular':
        return b.likes - a.likes
      case 'answered':
        return b.isAnswered ? 1 : -1
      case 'unanswered':
        return a.isAnswered ? 1 : -1
      default: // latest
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    }
  })

  return filtered
})

// Methods
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return t('forum.today')
  if (days === 1) return t('forum.yesterday')
  if (days < 7) return t('forum.daysAgo', { days })

  return date.toLocaleDateString()
}

const getCategoryColor = (category: string) => {
  const colors = {
    diseases: 'bg-red-100 text-red-800',
    diagnosis: 'bg-blue-100 text-blue-800',
    treatment: 'bg-green-100 text-green-800',
    prevention: 'bg-purple-100 text-purple-800',
    farming: 'bg-yellow-100 text-yellow-800',
    general: 'bg-gray-100 text-gray-800'
  }
  return colors[category] || 'bg-gray-100 text-gray-800'
}

const navigateToPost = (postId: number) => {
  router.push(`/forum/post/${postId}`)
}

const loadMorePosts = () => {
  // Simulate loading more posts
  hasMorePosts.value = false
}

const submitPost = () => {
  // Handle post submission
  console.log('Submitting post:', newPost.value)
  showCreatePost.value = false
  // Reset form
  newPost.value = {
    title: '',
    category: '',
    content: '',
    isQuestion: false
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
</style>