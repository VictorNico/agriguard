<!-- components/sections/DiseaseDetectionSection.vue -->
<template>
  <div class="py-12 bg-gradient-to-r from-green-50 to-blue-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header Section -->
      <DiseasesSectionHeader
          :subtitle="t('diseaseDetection.subtitle')"
          :title="t('diseaseDetection.title')"
          :description="t('diseaseDetection.description')"
          centered
      />

      <!-- Feature Cards -->
      <div class="mt-10">
        <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <FeatureCard
              v-for="feature in features"
              :key="feature.id"
              :icon="feature.icon"
              :bg-color="feature.bgColor"
              :title="t(`diseaseDetection.features.${feature.id}.title`)"
              :description="t(`diseaseDetection.features.${feature.id}.description`)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()

const features = [
  {
    id: 'instant_analysis',
    icon: 'fas fa-camera-retro',
    bgColor: 'bg-primary'
  },
  {
    id: 'historical_tracking',
    icon: 'fas fa-chart-line',
    bgColor: 'bg-info'
  },
  {
    id: 'early_alerts',
    icon: 'fas fa-bell',
    bgColor: 'bg-warning'
  }
]
</script>