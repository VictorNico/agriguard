<!-- components/BlogSection.vue -->
<template>
  <section id="blog" class="py-16 bg-gradient-to-br from-green-50 to-yellow-50">
    <div class="container mx-auto px-4">
      <!-- En-tête de section -->
      <div class="text-center mb-12">
        <h2 class="text-3xl md:text-4xl font-bold text-green-800 mb-4">
          {{ t('blog.title') }}
        </h2>
        <p class="text-xl text-green-600 max-w-2xl mx-auto">
          {{ t('blog.subtitle') }}
        </p>
      </div>

      <!-- Articles du blog -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
        <article
            v-for="post in blogPosts"
            :key="post.id"
            class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300"
        >
          <!-- Image -->
          <div class="h-48 bg-gradient-to-r from-green-400 to-yellow-400 flex items-center justify-center">
            <svg class="w-16 h-16 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
            </svg>
          </div>

          <!-- Contenu -->
          <div class="p-6">
            <!-- Catégorie et date -->
            <div class="flex items-center justify-between mb-3">
              <span class="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                {{ post.category }}
              </span>
              <span class="text-gray-500 text-sm">{{ post.date }}</span>
            </div>

            <!-- Titre -->
            <h3 class="text-xl font-bold text-green-800 mb-3 hover:text-green-600 transition-colors">
              <NuxtLink :to="`/blog/${post.slug}`">
                {{ post.title }}
              </NuxtLink>
            </h3>

            <!-- Extrait -->
            <p class="text-gray-600 mb-4 line-clamp-3">
              {{ post.excerpt }}
            </p>

            <!-- Auteur et lien -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 bg-gradient-to-r from-green-400 to-yellow-400 rounded-full flex items-center justify-center">
                  <span class="text-white font-medium text-sm">{{ post.author.initials }}</span>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ post.author.name }}</p>
                  <p class="text-xs text-gray-500">{{ post.author.role }}</p>
                </div>
              </div>
              <NuxtLink
                  :to="`/blog/${post.slug}`"
                  class="text-green-600 hover:text-green-700 font-medium text-sm transition-colors"
              >
                {{ t('blog.readMore') }} →
              </NuxtLink>
            </div>
          </div>
        </article>
      </div>

      <!-- Bouton voir plus -->
      <div class="text-center">
        <NuxtLink
            to="/blog"
            class="bg-green-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-green-700 transition-colors inline-flex items-center space-x-2"
        >
          <span>{{ t('blog.viewAll') }}</span>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n()

interface BlogPost {
  id: number
  title: string
  excerpt: string
  slug: string
  category: string
  date: string
  author: {
    name: string
    role: string
    initials: string
  }
}

const blogPosts = ref<BlogPost[]>([
  {
    id: 1,
    title: t('blog.post1.title'),
    excerpt: t('blog.post1.excerpt'),
    slug: 'identifying-corn-leaf-blight',
    category: t('blog.categories.disease'),
    date: '15 Jun 2024',
    author: {
      name: 'Dr. John Kiprotich',
      role: t('blog.roles.agronomist'),
      initials: 'JK'
    }
  },
  {
    id: 2,
    title: t('blog.post2.title'),
    excerpt: t('blog.post2.excerpt'),
    slug: 'ai-revolution-agriculture',
    category: t('blog.categories.technology'),
    date: '12 Jun 2024',
    author: {
      name: 'Anna Mwangi',
      role: t('blog.roles.developer'),
      initials: 'AM'
    }
  },
  {
    id: 3,
    title: t('blog.post3.title'),
    excerpt: t('blog.post3.excerpt'),
    slug: 'sustainable-farming-practices',
    category: t('blog.categories.farming'),
    date: '10 Jun 2024',
    author: {
      name: 'Francis Kimani',
      role: t('blog.roles.farmer'),
      initials: 'FK'
    }
  }
])
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>