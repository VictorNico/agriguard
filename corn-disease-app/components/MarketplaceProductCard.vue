<template>
  <div class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 p-3 rounded-full" :class="product.iconBg">
          <i :class="product.icon"></i>
        </div>
        <div class="ml-3 flex-1">
          <h3 class="text-md font-medium text-gray-900">{{ product.name }}</h3>
          <p class="text-sm text-gray-500">{{ product.details }}</p>
        </div>
      </div>

      <div class="mt-4 flex justify-between items-center">
        <span class="text-lg font-bold text-gray-900">{{ product.price }}</span>
        <span class="text-xs font-medium text-gray-500">{{ product.distance }}</span>
      </div>
    </div>

    <div class="px-4 py-4 bg-gray-50 border-t border-gray-200">
      <button
          type="button"
          class="w-full inline-flex items-center justify-center px-3 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
          @click="handleBuyProduct"
      >
        <i class="fas fa-shopping-cart mr-2"></i> {{ t('community.marketplace.buyButton') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const props = defineProps<{
  product: {
    id: number
    name: string
    details: string
    price: string
    distance: string
    icon: string
    iconBg: string
  }
}>()

const emit = defineEmits<{
  (e: 'buy-product', product: typeof props.product): void
}>()

const { t } = useI18n()

function handleBuyProduct() {
  emit('buy-product', props.product)
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