<template>
  <div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
    <div class="p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-purple-100 p-3 rounded-full">
          <i class="fas fa-hands-helping text-purple-500 text-xl"></i>
        </div>
        <div class="ml-4">
          <h3 class="text-lg font-medium text-gray-900">{{ t('community.mentoring.title') }}</h3>
          <p class="mt-1 text-sm text-gray-500">{{ t('community.mentoring.description') }}</p>
        </div>
      </div>

      <div class="mt-6 space-y-4">
        <div
            v-for="mentor in mentors"
            :key="mentor.id"
            class="flex items-center cursor-pointer hover:bg-gray-50 p-2 rounded-md transition-colors"
            @click="handleMentorClick(mentor)"
        >
          <div class="flex-shrink-0">
            <img
                class="h-10 w-10 rounded-full object-cover"
                :src="mentor.avatar"
                :alt="mentor.name"
            >
          </div>
          <div class="ml-3 flex-1">
            <p class="text-sm font-medium text-gray-900">{{ mentor.name }} - {{ mentor.experience }}</p>
            <p class="text-sm text-gray-500">{{ mentor.specialty }}</p>
            <div class="mt-1 flex items-center">
              <div class="flex">
                <i
                    v-for="n in 5"
                    :key="n"
                    class="fas fa-star text-yellow-400 text-xs"
                    :class="n === 1 ? '' : 'ml-1'"
                ></i>
              </div>
              <span class="text-xs text-gray-500 ml-2">{{ mentor.rating }} ({{ mentor.reviews }})</span>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6">
        <button
            type="button"
            class="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
            @click="handleFindMentor"
        >
          <i class="fas fa-user-plus mr-2"></i> {{ t('community.mentoring.findButton') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()
const props = defineProps({
  mentors: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['find-mentor', 'mentor-click'])

const handleFindMentor = ()=> {
  emit('find-mentor')
}

const handleMentorClick = (mentor)=> {
  emit('mentor-click', mentor)
}
</script>


<style scoped>
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