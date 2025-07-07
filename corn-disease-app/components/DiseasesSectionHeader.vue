<!-- components/ui/SectionHeader.vue -->
<template>
  <div :class="{ 'lg:text-center': centered }">
    <h2 class="text-base text-green-600 font-semibold tracking-wide uppercase">
      {{ subtitle }}
    </h2>
    <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
      {{ title }}
    </p>
    <p
        class="mt-4 text-xl text-gray-500"
        :class="{ 'max-w-2xl lg:mx-auto': centered }"
    >
      {{ description }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  subtitle: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  centered: {
    type: Boolean,
    default: true
  }
})
</script>