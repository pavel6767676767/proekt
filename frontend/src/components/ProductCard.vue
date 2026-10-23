<script setup>
defineProps({ product: { type: Object, required: true } })
const formatPrice = value => new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(value)
</script>
<template>
  <RouterLink :to="`/products/${product.id}`" class="product-card group">
    <div class="product-image"><img :src="product.image_url || 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1000&q=85'" :alt="product.name" loading="lazy"><span class="image-arrow">↗</span></div>
    <div class="product-meta"><span>{{ product.category.name }}</span><span>№ {{ String(product.id).padStart(3, '0') }}</span></div>
    <h3>{{ product.name }}</h3><p class="product-description">{{ product.description }}</p>
    <div class="product-bottom"><strong>{{ formatPrice(product.price) }}</strong><span>Подробнее <span aria-hidden="true">→</span></span></div>
  </RouterLink>
</template>
