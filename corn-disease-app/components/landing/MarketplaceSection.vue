<template>
  <div class="mt-8 bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
    <div class="px-6 py-5 border-b border-gray-200">
      <h3 class="text-lg leading-6 font-medium text-gray-900">{{ $t('community.marketplace.title') }}</h3>
      <p class="mt-1 text-sm text-gray-500">{{ $t('community.marketplace.description') }}</p>
    </div>

    <div class="bg-gray-50 px-6 py-4">
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">

        <!-- Products -->
        <MarketplaceProductCard
            v-for="product in products"
            :key="product.id"
            :product="product"
            @buy-product="handleBuyProduct"
        />

        <!-- Add Product -->
        <MarketplaceAddProductCard
            @add-product="handleAddProduct"
        />

      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// Définir les props
const props = defineProps({
  products: {
    type: Array,
    default: () => []
  }
})
// console.log(props.products.value)
// Définir les événements émis
const emit = defineEmits(['buy-product', 'add-product'])

// Méthodes
const handleBuyProduct = (product) => {
  emit('buy-product', product)
}

const handleAddProduct = () => {
  emit('add-product')
}
</script>
