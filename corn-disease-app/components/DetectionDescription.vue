<template>
  <p class="text-gray-700 mb-4">{{ description }}</p>
</template>

<script setup>
defineProps({
  description: String
})
</script>