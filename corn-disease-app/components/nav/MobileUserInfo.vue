<template>
  <div class="flex items-center px-5">
    <div class="flex-shrink-0">
      <img
          class="h-10 w-10 rounded-full"
          :src="user.avatar"
          :alt="user.name"
      >
    </div>
    <div class="ml-3">
      <div class="text-base font-medium text-gray-800">{{ user.name }}</div>
      <div class="text-sm font-medium text-gray-500">{{ user.email }}</div>
    </div>
    <button
        type="button"
        class="ml-auto flex-shrink-0 bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
    >
      <span class="sr-only">{{ $t('notifications.title') || 'Notifications' }}</span>
      <i class="fas fa-bell h-6 w-6"></i>
    </button>
  </div>
</template>

<script setup>
defineProps({
  user: Object
})

const { t } = useI18n()
</script>