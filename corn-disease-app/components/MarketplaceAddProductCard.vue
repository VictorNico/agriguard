<template>
  <div class="bg-white overflow-hidden shadow rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 transition-colors">
    <div class="px-4 py-12 sm:p-6 text-center">
      <i class="fas fa-plus-circle text-gray-400 text-4xl mb-4"></i>
      <h3 class="text-sm font-medium text-gray-900">{{ t('community.marketplace.addProduct.title') }}</h3>
      <p class="mt-1 text-sm text-gray-500">{{ t('community.marketplace.addProduct.description') }}</p>

      <div class="mt-6">
        <button
            type="button"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
            @click="handleAddProduct"
        >
          <i class="fas fa-plus mr-2"></i> {{ t('community.marketplace.addProduct.button') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()
const emit = defineEmits(['add-product'])

const handleAddProduct = () => {
  emit('add-product')
}
</script>


<style scoped>
.bg-primary {
  background-color: #10B981;
}

.bg-secondary {
  background-color: #059669;
}

.hover\:bg-secondary:hover {
  background-color: #059669;
}

.focus\:ring-primary:focus {
  --tw-ring-color: #10B981;
}
</style>