<template>
  <div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
    <div class="p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-red-100 p-3 rounded-full">
          <i class="fas fa-bell text-red-500 text-xl"></i>
        </div>
        <div class="ml-4">
          <h3 class="text-lg font-medium text-gray-900">{{ t('community.alerts.title') }}</h3>
          <p class="mt-1 text-sm text-gray-500">{{ t('community.alerts.description') }}</p>
        </div>
      </div>

      <div class="mt-6 space-y-4">
        <div
            v-for="alert in alerts"
            :key="alert.id"
            class="flex items-start"
        >
          <div class="flex-shrink-0">
            <img
                class="h-10 w-10 rounded-full object-cover"
                :src="alert.avatar"
                :alt="alert.name"
            >
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium text-gray-900">{{ alert.name }}</p>
            <p class="text-sm text-gray-500">"{{ alert.message }}"</p>
            <p class="mt-1 text-xs text-gray-400">{{ alert.time }}</p>
          </div>
        </div>
      </div>

      <div class="mt-6">
        <button
            type="button"
            class="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
            @click="handleAddAlert"
        >
          <i class="fas fa-plus mr-2"></i> {{ t('community.alerts.addButton') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()
const props = defineProps({
  alerts: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['add-alert'])

const handleAddAlert = () => {
  emit('add-alert')
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