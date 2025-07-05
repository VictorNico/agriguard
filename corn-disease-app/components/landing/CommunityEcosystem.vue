<template>
  <div id="community" class="py-12 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <!-- Header Section -->
      <div class="lg:text-center">
        <h2 class="text-base text-primary font-semibold tracking-wide uppercase">
          {{ t('community.title') }}
        </h2>
        <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          {{ t('community.subtitle') }}
        </p>
        <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
          {{ t('community.description') }}
        </p>
      </div>

      <!-- Main Cards Grid -->
      <div class="mt-10">
        <div class="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">

          <!-- Community Alerts -->
          <CommunityAlertCard
              :alerts="alerts"
              @add-alert="addAlert"
          />

          <!-- Forum -->
          <ForumCard
              :topics="forumTopics"
              @browse-forum="browseForum"
              @topic-click="topicClick"
          />

          <!-- Mentoring -->
          <MentoringCard
              :mentors="mentors"
              @find-mentor="findMentor"
              @mentor-click="clickMentor"
          />

        </div>

        <!-- Marketplace Section -->
        <MarketplaceSection
            :products="products"
            @buy-product="buyProduct"
            @add-product="addProduct"
        />

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { defineProps, defineEmits } from 'vue'

// Internationalisation
const { t } = useI18n()

// Props
const props = defineProps({
  initialAlerts: {
    type: Array,
    default: null
  },
  initialTopics: {
    type: Array,
    default: null
  },
  initialMentors: {
    type: Array,
    default: null
  },
  initialProducts: {
    type: Array,
    default: null
  }
})

// Événements
const emit = defineEmits([
  'add-alert',
  'browse-forum',
  'find-mentor',
  'buy-product',
  'add-product'
])

// Données locales
const alerts = ref([
  {
    id: 1,
    name: 'Marie D.',
    message: t('community.alerts.messages.aphids'),
    time: t('community.alerts.times.twoHours'),
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?...'
  },
  {
    id: 2,
    name: 'Pierre L.',
    message: t('community.alerts.messages.mildew'),
    time: t('community.alerts.times.today'),
    avatar: 'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?...'
  }
])

const forumTopics = ref([
  {
    id: 1,
    title: t('community.forum.topics.bioTreatment'),
    replies: t('community.forum.replies.twelve'),
    distance: t('community.forum.distances.threeKm'),
    icon: 'fas fa-seedling text-green-500 text-lg',
    iconBg: 'bg-green-50'
  },
  {
    id: 2,
    title: t('community.forum.topics.cornSowing'),
    replies: t('community.forum.replies.twentyFour'),
    distance: t('community.forum.distances.eightKm'),
    icon: 'fas fa-tractor text-yellow-500 text-lg',
    iconBg: 'bg-yellow-50'
  },
  {
    id: 3,
    title: t('community.forum.topics.newPest'),
    replies: t('community.forum.replies.seven'),
    distance: t('community.forum.distances.fiveKm'),
    icon: 'fas fa-bug text-red-500 text-lg',
    iconBg: 'bg-red-50'
  }
])

const mentors = ref([
  {
    id: 1,
    name: 'Jean M.',
    experience: t('community.mentoring.experiences.twentyFive'),
    specialty: t('community.mentoring.specialties.organic'),
    rating: '4.9',
    reviews: t('community.mentoring.reviews.thirtyTwo'),
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5cd?...'
  },
  {
    id: 2,
    name: 'Sophie R.',
    experience: t('community.mentoring.experiences.fifteen'),
    specialty: t('community.mentoring.specialties.pestManagement'),
    rating: '4.8',
    reviews: t('community.mentoring.reviews.twentyEight'),
    avatar: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?...'
  }
])

const products = ref([
  {
    id: 1,
    name: t('community.marketplace.products.bioFungicide.name'),
    details: t('community.marketplace.products.bioFungicide.details'),
    price: '4500 FCFA',
    distance: t('community.marketplace.distances.eightKm'),
    icon: 'fas fa-spray-can text-green-500 text-xl',
    iconBg: 'bg-green-100'
  },
  {
    id: 2,
    name: t('community.marketplace.products.sprayer.name'),
    details: t('community.marketplace.products.sprayer.details'),
    price: '12000 FCFA',
    distance: t('community.marketplace.distances.fifteenKm'),
    icon: 'fas fa-tractor text-blue-500 text-xl',
    iconBg: 'bg-blue-100'
  },
  {
    id: 3,
    name: t('community.marketplace.products.seeds.name'),
    details: t('community.marketplace.products.seeds.details'),
    price: '8500 FCFA',
    distance: t('community.marketplace.distances.fiveKm'),
    icon: 'fas fa-seedling text-yellow-500 text-xl',
    iconBg: 'bg-yellow-100'
  }
])

// Méthodes
const addAlert = () => emit('add-alert')
const browseForum = () => emit('browse-forum')
const topicClick = () => emit('topic-click')
const clickMentor = () => emit('click-mentor')
const findMentor = () => emit('find-mentor')
const buyProduct = (product) => emit('buy-product', product)
const addProduct = () => emit('add-product')

</script>


<style scoped>
.text-primary {
  color: #10B981; /* Adjust primary color as needed */
}

.bg-primary {
  background-color: #10B981;
}

.bg-secondary {
  background-color: #059669;
}

.hover\:bg-secondary:hover {
  background-color: #059669;
}

.focus\:ring-primary:focus {
  --tw-ring-color: #10B981;
}
</style>