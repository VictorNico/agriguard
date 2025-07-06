<template>
  <div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
    <div class="p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-blue-100 p-3 rounded-full">
          <i class="fas fa-comments text-blue-500 text-xl"></i>
        </div>
        <div class="ml-4">
          <h3 class="text-lg font-medium text-gray-900">{{ t('community.forum.title') }}</h3>
          <p class="mt-1 text-sm text-gray-500">{{ t('community.forum.description') }}</p>
        </div>
      </div>

      <div class="mt-6 space-y-4">
        <div
            v-for="topic in topics"
            :key="topic.id"
            class="flex items-start cursor-pointer hover:bg-gray-50 p-2 rounded-md transition-colors"
            @click="handleTopicClick(topic)"
        >
          <div class="flex-shrink-0 rounded-full p-1" :class="topic.iconBg">
            <i :class="topic.icon"></i>
          </div>
          <div class="ml-3 flex-1">
            <p class="text-sm font-medium text-gray-900">{{ topic.title }}</p>
            <p class="text-sm text-gray-500">{{ topic.replies }} • {{ topic.distance }}</p>
          </div>
        </div>
      </div>

      <div class="mt-6">
        <button
            type="button"
            class="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
            @click="handleBrowseForum"
        >
          <i class="fas fa-search mr-2"></i> {{ t('community.forum.browseButton') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()
const props = defineProps({
  topics: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['browse-forum', 'topic-click'])

function handleBrowseForum() {
  emit('browse-forum')
}

function handleTopicClick(topic) {
  emit('topic-click', topic)
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