<template>
  <div class="p-6 bg-white/10 rounded-xl">
    <div class="text-4xl font-bold">{{ value }}</div>
    <div class="mt-2 text-sm font-medium">{{ description }}</div>
  </div>
</template>

<script setup>
defineProps({
  value: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  }
})
</script>