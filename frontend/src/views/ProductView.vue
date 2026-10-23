<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getProduct } from '../services/api'
const route = useRoute(); const product = ref(null); const error = ref(''); const loading = ref(true)
async function load() { loading.value = true; error.value = ''; try { product.value = await getProduct(route.params.id) } catch { error.value = 'Не удалось найти товар.' } finally { loading.value = false } }
onMounted(load); watch(() => route.params.id, load)
const formatPrice = value => new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(value)
</script>
<template><main class="detail-page"><RouterLink to="/" class="back-link">← Вернуться в каталог</RouterLink><p v-if="loading" class="notice">Загружаем…</p><p v-else-if="error" class="notice error">{{ error }}</p><div v-else-if="product" class="detail-grid"><div class="detail-image"><img :src="product.image_url" :alt="product.name"></div><div class="detail-copy"><div class="eyebrow dark"><span></span> {{ product.category.name.toUpperCase() }} · № {{ String(product.id).padStart(3, '0') }}</div><h1>{{ product.name }}</h1><p class="detail-description">{{ product.description || 'Оборудование для профессиональных задач.' }}</p><div class="detail-price">{{ formatPrice(product.price) }}</div><a class="contact-button" :href="`mailto:hello@forma.example?subject=${encodeURIComponent('Запрос: ' + product.name)}`">Запросить предложение <span>↗</span></a><p class="detail-note">Поможем подобрать конфигурацию и рассчитать доставку.</p></div></div></main></template>
