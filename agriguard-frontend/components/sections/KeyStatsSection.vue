<template>
  <div class="py-12 bg-green-600 text-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
        <StatCard
            v-for="stat in stats"
            :key="stat.id"
            :value="stat.value"
            :description="$t(stat.descriptionKey)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()

const stats = [
  {
    id: 1,
    value: '40%',
    descriptionKey: 'stats.agricultural_losses'
  },
  {
    id: 2,
    value: '600 000',
    descriptionKey: 'stats.cocoa_families'
  },
  {
    id: 3,
    value: '100M+',
    descriptionKey: 'stats.corn_weevil_losses'
  }
]
</script>