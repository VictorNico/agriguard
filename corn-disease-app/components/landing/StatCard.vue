<template>
  <div class="p-6 bg-white/10 rounded-xl">
    <div class="text-4xl font-bold">{{ value }}</div>
    <div class="mt-2 text-sm font-medium">{{ description }}</div>
    <!-- Source affichée uniquement si présente -->
    <div v-if="sourceTitle && sourceLink" class="mt-4">
      <a
          :href="sourceLink"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-block text-sm px-4 py-2 rounded-md border border-white/20 bg-white/5 text-white hover:bg-white/10 hover:underline transition"
      >
        🔗 {{ sourceTitle }}
      </a>
    </div>
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
  },
  sourceTitle: {
    type: String,
    required: false
  },
  sourceLink: {
    type: String,
    required: false
  }
})
</script>