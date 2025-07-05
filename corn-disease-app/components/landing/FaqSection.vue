<!-- components/FaqSection.vue -->
<template>
  <section id="faq" class="py-16 bg-white">
    <div class="container mx-auto px-4">
      <!-- En-tête de section -->
      <div class="text-center mb-12">
        <h2 class="text-3xl md:text-4xl font-bold text-green-800 mb-4">
          {{ t('faq.pageTitle') }}
        </h2>
        <p class="text-xl text-green-600 max-w-2xl mx-auto">
          {{ t('faq.pageSubtitle') }}
        </p>
      </div>

      <!-- FAQ Items -->
      <div class="max-w-4xl mx-auto">
        <div class="space-y-4">
          <div
              v-for="(faq, index) in faqs"
              :key="index"
              class="bg-green-50 border border-green-200 rounded-lg overflow-hidden transition-all duration-300 hover:shadow-md"
          >
            <button
                @click="toggleFaq(index)"
                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-green-100 transition-colors"
            >
              <span class="font-semibold text-green-800 pr-4">
                {{ faq.question }}
              </span>
              <svg
                  :class="['w-5 h-5 text-green-600 transition-transform', { 'rotate-180': faq.isOpen }]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div
                v-if="faq.isOpen"
                class="px-6 pb-4 text-gray-700 leading-relaxed border-t border-green-200 bg-white"
            >
              <div class="pt-4" v-html="faq.answer"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Contact -->
      <div class="text-center mt-12">
        <div class="bg-gradient-to-r from-green-100 to-yellow-100 p-8 rounded-xl max-w-2xl mx-auto">
          <h3 class="text-xl font-bold text-green-800 mb-4">
            {{ t('faq.stillHaveQuestions') }}
          </h3>
          <p class="text-green-600 mb-6">
            {{ t('faq.contactDescription') }}
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <a
                href="mailto:support@agriguard.ai"
                class="bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 transition-colors"
            >
              {{ t('faq.contactSupport') }}
            </a>
            <NuxtLink
                to="/forum"
                class="bg-white text-green-600 px-6 py-3 rounded-lg font-medium border border-green-600 hover:bg-green-50 transition-colors"
            >
              {{ t('faq.joinForum') }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n()

const faqs = ref([
  {
    question: t('faq.questions.q1.question'),
    answer: t('faq.questions.q1.answer'),
    isOpen: false
  },
  {
    question: t('faq.questions.q2.question'),
    answer: t('faq.questions.q2.answer'),
    isOpen: false
  },
  {
    question: t('faq.questions.q3.question'),
    answer: t('faq.questions.q3.answer'),
    isOpen: false
  },
  {
    question: t('faq.questions.q4.question'),
    answer: t('faq.questions.q4.answer'),
    isOpen: false
  },
  {
    question: t('faq.questions.q5.question'),
    answer: t('faq.questions.q5.answer'),
    isOpen: false
  },
  {
    question: t('faq.questions.q6.question'),
    answer: t('faq.questions.q6.answer'),
    isOpen: false
  },
  {
    question: t('faq.questions.q7.question'),
    answer: t('faq.questions.q7.answer'),
    isOpen: false
  },
  {
    question: t('faq.questions.q8.question'),
    answer: t('faq.questions.q8.answer'),
    isOpen: false
  },
  {
    question: t('faq.questions.q9.question'),
    answer: t('faq.questions.q9.answer'),
    isOpen: false
  },
  {
    question: t('faq.questions.q10.question'),
    answer: t('faq.questions.q10.answer'),
    isOpen: false
  }
])

const toggleFaq = (index: number) => {
  faqs.value[index].isOpen = !faqs.value[index].isOpen
}
</script>