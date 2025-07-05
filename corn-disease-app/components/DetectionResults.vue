<template>
  <div v-if="results" class="bg-white rounded-2xl shadow-lg p-8">
    <h3 class="text-2xl font-bold text-gray-900 mb-6">{{ $t('results.title') }}</h3>

    <NoDetectionMessage v-if="results.detections.length === 0" />

    <div v-else class="space-y-6">
      <DetectionCard
          v-for="(detection, index) in results.detections"
          :key="index"
          :detection="detection"
      />
    </div>
<!--    -->
  </div>
</template>

<script setup>
defineProps({
  results: Object
})

const { t } = useI18n()
</script>