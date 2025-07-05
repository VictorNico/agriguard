<template>
  <button
      type="button"
      class="bg-gray-800 p-1 rounded-full text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white transition-colors"
      @click="handleNotificationClick"
  >
    <span class="sr-only">{{ $t('notifications.title') || 'Notifications' }}</span>
    <div class="notification-bell relative">
      <i class="fas fa-bell h-6 w-6"></i>
      <span
          v-if="hasUnreadNotifications"
          class="absolute top-0 right-0 h-2 w-2 rounded-full bg-danger animate-pulse"
      ></span>
    </div>
  </button>
</template>

<script setup>
import { ref } from 'vue'

const { t } = useI18n()
const hasUnreadNotifications = ref(true)

const handleNotificationClick = () => {
  // Logique pour afficher les notifications
  console.log('Afficher les notifications')
}
</script>

<style scoped>
.notification-bell {
  animation: ring 2s ease infinite;
  transform-origin: 50% 0;
}

@keyframes ring {
  0% { transform: rotate(0); }
  1% { transform: rotate(30deg); }
  3% { transform: rotate(-28deg); }
  5% { transform: rotate(34deg); }
  7% { transform: rotate(-32deg); }
  9% { transform: rotate(30deg); }
  11% { transform: rotate(-28deg); }
  13% { transform: rotate(26deg); }
  15% { transform: rotate(-24deg); }
  17% { transform: rotate(22deg); }
  19% { transform: rotate(-20deg); }
  21% { transform: rotate(18deg); }
  23% { transform: rotate(-16deg); }
  25% { transform: rotate(14deg); }
  27% { transform: rotate(-12deg); }
  29% { transform: rotate(10deg); }
  31% { transform: rotate(-8deg); }
  33% { transform: rotate(6deg); }
  35% { transform: rotate(-4deg); }
  37% { transform: rotate(2deg); }
  39% { transform: rotate(-1deg); }
  41% { transform: rotate(1deg); }
  43% { transform: rotate(0); }
  100% { transform: rotate(0); }
}
</style>