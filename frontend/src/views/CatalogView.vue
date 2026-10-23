<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useCatalogStore } from '../stores/catalog'
import CategoryFilter from '../components/CategoryFilter.vue'
import ProductCard from '../components/ProductCard.vue'
const store = useCatalogStore(); const { categories, products, total, selectedCategory, loading, error } = storeToRefs(store)
onMounted(() => store.load())
</script>
<template>
  <main>
    <section class="hero"><div class="hero-grid"></div><div class="hero-content"><div class="eyebrow"><span></span> ИНЖЕНЕРНЫЙ МАРКЕТПЛЕЙС</div><h1>Форма<br><em>будущего.</em></h1><p class="hero-copy">Оборудование, которое превращает смелые идеи в реальные вещи. От первого прототипа до серийного производства.</p><a href="#catalog" class="hero-link">Смотреть каталог <span>↓</span></a></div><div class="hero-image-wrap"><img src="https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1600&q=90" alt="Современное производственное оборудование"><div class="hero-stamp">ТЕХНОЛОГИИ<br>В ДЕЙСТВИИ <span>✳</span></div><div class="hero-caption"><span>01 / 04</span><span>Машины для нового поколения</span></div></div><div class="hero-index">МАТЕРИАЛИЗУЕМ ИДЕИ — С 2018</div></section>
    <section id="catalog" class="catalog-section"><div class="section-heading"><div><div class="eyebrow dark"><span></span> НАЙДИТЕ СВОЁ</div><h2>Инструменты<br>для <em>больших идей.</em></h2></div><p>Точное оборудование для людей,<br>которые не боятся делать по-своему.</p></div><CategoryFilter :categories="categories" :selected="selectedCategory" @select="store.filterBy"/><div class="catalog-count"><span>{{ String(products.length).padStart(2, '0') }} МОДЕЛЕЙ</span><span>ПОДОБРАНО ДЛЯ ВАШЕГО ПРОЕКТА</span></div><div v-if="loading" class="notice">Загружаем оборудование…</div><div v-else-if="error" class="notice error">{{ error }} <button @click="store.load">Повторить</button></div><div v-else-if="!products.length" class="notice">В этой категории пока нет оборудования.</div><div v-else class="product-grid"><ProductCard v-for="product in products" :key="product.id" :product="product" /></div><div class="catalog-end"><span>ПОКАЗАНО {{ products.length }} ИЗ {{ total }}</span><span>КАЧЕСТВО, ПРОВЕРЕННОЕ ПРАКТИКОЙ&nbsp; ✳</span></div></section>
    <section id="about" class="manifesto"><div class="manifesto-side">НАША ФИЛОСОФИЯ<br>01 — 03</div><div><div class="eyebrow"><span></span> ОТ ИДЕИ К ОБЪЕКТУ</div><h2>Мы верим, что<br>инструменты должны<br><em>расширять границы.</em></h2><p>Подбираем технологии для мастерских и производств, которым важно не просто работать быстрее — а создавать то, чего ещё не существовало.</p><a class="hero-link" href="mailto:hello@forma.example">Расскажите о проекте <span>↗</span></a></div><div class="manifesto-decoration">Ф</div></section>
  </main>
</template>
