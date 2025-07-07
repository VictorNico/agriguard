<!-- pages/faq.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-yellow-50">
    <!-- Header -->
    <div class="bg-gradient-to-r from-green-600 to-green-700 text-white py-16">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          {{ t('faq.pageTitle') }}
        </h1>
        <p class="text-xl text-green-100 max-w-3xl mx-auto">
          {{ t('faq.pageSubtitle') }}
        </p>
      </div>
    </div>

    <!-- Search FAQ -->
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-2xl mx-auto">
        <div class="relative">
          <input
              v-model="searchQuery"
              type="text"
              :placeholder="t('faq.searchPlaceholder')"
              class="w-full px-6 py-4 text-lg border-2 border-green-200 rounded-xl focus:outline-none focus:border-green-500 transition-colors"
          />
          <div class="absolute right-4 top-1/2 transform -translate-y-1/2">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ Categories -->
    <div class="container mx-auto px-4 pb-8">
      <div class="flex flex-wrap justify-center gap-4">
        <button
            v-for="category in categories"
            :key="category"
            @click="selectedCategory = category"
            :class="[
            'px-6 py-3 rounded-full font-medium transition-all',
            selectedCategory === category
              ? 'bg-green-600 text-white shadow-lg'
              : 'bg-white text-green-600 hover:bg-green-50 shadow-sm'
          ]"
        >
          {{ t(`faq.categories.${category}`) }}
        </button>
      </div>
    </div>

    <!-- FAQ Content -->
    <div class="container mx-auto px-4 pb-16">
      <div class="max-w-4xl mx-auto">
        <div class="space-y-6">
          <div
              v-for="faq in filteredFAQs"
              :key="faq.id"
              class="bg-white rounded-xl shadow-lg overflow-hidden"
          >
            <button
                @click="toggleFAQ(faq.id)"
                class="w-full px-8 py-6 text-left hover:bg-green-50 transition-colors flex items-center justify-between"
            >
              <h3 class="text-lg font-semibold text-green-800 pr-4">
                {{ t(faq.question) }}
              </h3>
              <div class="flex-shrink-0">
                <svg
                    :class="['w-5 h-5 text-green-600 transition-transform', openFAQs.includes(faq.id) ? 'rotate-180' : '']"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>
            </button>

            <div
                v-if="openFAQs.includes(faq.id)"
                class="px-8 pb-6 border-t border-green-100"
            >
              <div class="pt-4 text-gray-700 leading-relaxed">
                <p v-html="t(faq.answer)"></p>
              </div>
            </div>
          </div>
        </div>

        <!-- No Results -->
        <div v-if="filteredFAQs.length === 0" class="text-center py-12">
          <div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
            <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-700 mb-2">{{ t('faq.noResults') }}</h3>
          <p class="text-gray-500">{{ t('faq.tryDifferentSearch') }}</p>
        </div>
      </div>
    </div>

    <!-- Contact Section -->
    <div class="bg-white py-16">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold text-green-800 mb-4">
          {{ t('faq.stillHaveQuestions') }}
        </h2>
        <p class="text-gray-600 mb-8 max-w-2xl mx-auto">
          {{ t('faq.contactDescription') }}
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors">
            {{ t('faq.contactSupport') }}
          </button>
          <button class="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold border-2 border-green-600 hover:bg-green-50 transition-colors">
            {{ t('faq.joinForum') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

// SEO Meta
useHead({
  title: computed(() => t('faq.metaTitle')),
  meta: [
    {
      name: 'description',
      content: computed(() => t('faq.metaDescription'))
    }
  ]
})

// Reactive data
const searchQuery = ref('')
const selectedCategory = ref('all')
const openFAQs = ref<number[]>([])

// Categories
const categories = ['all', 'diagnosis', 'diseases', 'treatment', 'prevention', 'app', 'technical']

// FAQ Data
const faqData = ref([
  {
    id: 1,
    category: 'diagnosis',
    question: 'faq.questions.q1.question',
    answer: 'faq.questions.q1.answer'
  },
  {
    id: 2,
    category: 'diagnosis',
    question: 'faq.questions.q2.question',
    answer: 'faq.questions.q2.answer'
  },
  {
    id: 3,
    category: 'diseases',
    question: 'faq.questions.q3.question',
    answer: 'faq.questions.q3.answer'
  },
  {
    id: 4,
    category: 'diseases',
    question: 'faq.questions.q4.question',
    answer: 'faq.questions.q4.answer'
  },
  {
    id: 5,
    category: 'treatment',
    question: 'faq.questions.q5.question',
    answer: 'faq.questions.q5.answer'
  },
  {
    id: 6,
    category: 'prevention',
    question: 'faq.questions.q6.question',
    answer: 'faq.questions.q6.answer'
  },
  {
    id: 7,
    category: 'app',
    question: 'faq.questions.q7.question',
    answer: 'faq.questions.q7.answer'
  },
  {
    id: 8,
    category: 'technical',
    question: 'faq.questions.q8.question',
    answer: 'faq.questions.q8.answer'
  },
  {
    id: 9,
    category: 'technical',
    question: 'faq.questions.q9.question',
    answer: 'faq.questions.q9.answer'
  },
  {
    id: 10,
    category: 'prevention',
    question: 'faq.questions.q10.question',
    answer: 'faq.questions.q10.answer'
  }
])

// Computed
const filteredFAQs = computed(() => {
  let filtered = faqData.value

  // Filter by category
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(faq => faq.category === selectedCategory.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(faq =>
        t(faq.question).toLowerCase().includes(query) ||
        t(faq.answer).toLowerCase().includes(query)
    )
  }

  return filtered
})

// Methods
const toggleFAQ = (id: number) => {
  const index = openFAQs.value.indexOf(id)
  if (index > -1) {
    openFAQs.value.splice(index, 1)
  } else {
    openFAQs.value.push(id)
  }
}
</script>