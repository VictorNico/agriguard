<template>
  <Transition name="slide-down">
    <div v-if="!isOnline" class="fixed top-0 left-0 right-0 bg-orange-500 text-white p-2 text-center text-sm z-50">
      <div class="flex items-center justify-center space-x-2">
        <Icon name="heroicons:wifi-slash" class="w-4 h-4" />
        <span>{{ $t('offline.description') }}</span>
        <button
            @click="checkConnection"
            class="underline hover:no-underline"
        >
          {{ $t('offline.retry') }}
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isOnline = ref(navigator.onLine)

const updateOnlineStatus = () => {
  isOnline.value = navigator.onLine
}

const checkConnection = () => {
  updateOnlineStatus()
  if (isOnline.value) {
    // Optionnel: vérifier avec un ping
    fetch('/api/health', { method: 'HEAD' })
        .then(() => {
          isOnline.value = true
        })
        .catch(() => {
          isOnline.value = false
        })
  }
}

onMounted(() => {
  window.addEventListener('online', updateOnlineStatus)
  window.addEventListener('offline', updateOnlineStatus)
})

onUnmounted(() => {
  window.removeEventListener('online', updateOnlineStatus)
  window.removeEventListener('offline', updateOnlineStatus)
})
</script>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-100%);
}
</style>