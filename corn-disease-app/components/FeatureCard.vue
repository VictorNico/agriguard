<!-- components/ui/FeatureCard.vue -->
<template>
  <div class="pt-6">
    <div class="flow-root bg-white rounded-lg px-6 pb-8 h-full shadow-sm hover:shadow-md transition-shadow">
      <div class="-mt-6">
        <div>
          <span
              class="inline-flex items-center justify-center p-3 rounded-md shadow-lg"
              :class="getColorClass(bgColor)"
          >
            <i :class="`${icon} text-white text-2xl`"></i>
          </span>
        </div>
        <h3 class="mt-8 text-lg font-medium text-gray-900 tracking-tight">
          {{ title }}
        </h3>
        <p class="mt-5 text-base text-gray-500">
          {{ description }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  icon: {
    type: String,
    required: true
  },
  bgColor: {
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
  }
})

const getColorClass = (color) => {
  const colorMap = {
    'bg-primary': 'bg-green-600',
    'bg-info': 'bg-blue-600',
    'bg-warning': 'bg-yellow-600',
    'bg-danger': 'bg-red-600',
    'bg-success': 'bg-green-600',
    'bg-secondary': 'bg-gray-600'
  }
  return colorMap[color] || 'bg-green-600'
}
</script>