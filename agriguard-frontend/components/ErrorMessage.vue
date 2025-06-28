<template>
  <div v-if="message" class="bg-red-50 border border-red-200 rounded-xl p-6 mb-8">
    <div class="flex items-center">
      <div class="flex-shrink-0">
        <span class="text-red-500 text-xl">⚠️</span>
      </div>
      <div class="ml-3">
        <h3 class="text-sm font-medium text-red-800">{{ $t('status.error') }}</h3>
        <p class="mt-1 text-sm text-red-700">{{ message }}</p>
        <button
            @click="$emit('retry')"
            class="mt-2 text-sm text-red-600 hover:text-red-800 underline"
        >
          {{ $t('buttons.retry') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: String
})

defineEmits(['retry'])

const { t } = useI18n()
</script>