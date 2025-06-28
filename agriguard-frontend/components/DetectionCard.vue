<template>
  <div class="border border-gray-200 rounded-xl p-6">
    <DetectionHeader :detection="detection" />
    <DetectionDescription :description="detection.description" />
    <TreatmentSection v-if="detection.treatment?.length" :treatments="detection.treatment" />
  </div>
</template>

<script setup>
defineProps({
  detection: Object
})
</script>