<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { getMachines, getZones } from '../services/api'

const zones = ref([])
const machines = ref([])
const selectedZone = ref(null)
const opened = ref(false)
const loading = ref(true)
const error = ref('')
let refreshTimer
const shownMachines = computed(() => selectedZone.value == null ? machines.value : machines.value.filter(machine => machine.zone_id === selectedZone.value))
const icons = { 'Автоматизация': '🌱', 'Робототехника': '🦾', '3D-печать': '🖨', 'Авиамоделирование': '🚁', '3D-сканирование': '📡', 'Станки': '⚙️' }

function toggleCatalog() {
  opened.value = !opened.value
  if (opened.value) setTimeout(() => document.getElementById('catalog')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 80)
}
async function load() {
  loading.value = true
  error.value = ''
  try { [zones.value, machines.value] = await Promise.all([getZones(), getMachines()]) }
  catch { error.value = 'Не удалось получить каталог. Убедитесь, что API запущен.' }
  finally { loading.value = false }
}
onMounted(() => {
  load()
  refreshTimer = window.setInterval(async () => {
    try { [zones.value, machines.value] = await Promise.all([getZones(), getMachines()]); error.value = '' }
    catch { /* Keep the last successful catalog while the API is temporarily unavailable. */ }
  }, 15000)
  if (window.location.hash === '#catalog') {
    opened.value = true
    setTimeout(() => document.getElementById('catalog')?.scrollIntoView({ block: 'start' }), 80)
  }
})
onBeforeUnmount(() => window.clearInterval(refreshTimer))
</script>

<template>
  <main class="edu-page">
    <section class="edu-intro">
      <div class="edu-kicker"><span></span> ОБОРУДОВАНИЕ ДЛЯ ОБУЧЕНИЯ И ТВОРЧЕСТВА</div>
      <h1>Идеи становятся<br><em>реальными.</em></h1>
      <p>Станки, роботы, 3D-принтеры и лабораторные комплексы для проектов, которые хочется воплощать.</p>
      <button class="edu-catalog-toggle" :aria-expanded="opened" @click="toggleCatalog"><span class="edu-burger" :class="{ active: opened }"><i></i><i></i><i></i></span>{{ opened ? 'Закрыть каталог' : 'Открыть каталог' }}</button>
      <div class="edu-orbit">ОБУЧАЙСЯ<br>СОЗДАВАЙ<br>ИССЛЕДУЙ <b>✳</b></div>
    </section>

    <section id="catalog" class="edu-catalog" :class="{ expanded: opened }">
      <div class="edu-catalog-head"><div><div class="edu-kicker"><span></span> КАТАЛОГ ОБОРУДОВАНИЯ</div><h2>Выбери направление</h2></div><span class="edu-count">{{ String(shownMachines.length).padStart(2, '0') }} ПОЗИЦИЙ</span></div>
      <div class="edu-zone-list"><button :class="{ active: selectedZone === null }" @click="selectedZone = null">Всё оборудование</button><button v-for="zone in zones" :key="zone.id" :class="{ active: selectedZone === zone.id }" @click="selectedZone = zone.id">{{ zone.name }}</button></div>
      <p v-if="loading" class="edu-message">Загружаем оборудование…</p><p v-else-if="error" class="edu-message is-error">{{ error }} <button @click="load">Повторить</button></p><p v-else-if="!shownMachines.length" class="edu-message">В выбранном разделе оборудования пока нет.</p>
      <div v-else class="edu-cards">
        <RouterLink v-for="machine in shownMachines" :key="machine.id" :to="`/machines/${machine.id}`" class="edu-card">
          <div class="edu-card-art"><img v-if="machine.image_url" :src="machine.image_url" :alt="machine.name" loading="lazy"><span v-else>{{ icons[zones.find(zone => zone.id === machine.zone_id)?.name] || '🛠' }}</span><i>↗</i></div>
          <div class="edu-card-meta"><span>{{ zones.find(zone => zone.id === machine.zone_id)?.name || 'Оборудование' }}</span><span>№ {{ String(machine.id).padStart(3, '0') }}</span></div>
          <h3>{{ machine.name }}</h3><p>{{ machine.description }}</p><div class="edu-card-foot"><span>{{ machine.quantity }} шт.</span><b>Подробнее&nbsp; →</b></div>
        </RouterLink>
      </div>
    </section>

    <section id="about" class="edu-about"><div class="edu-kicker"><span></span> ТЕХНОЛОГИИ В ДЕЙСТВИИ</div><h2>Учиться, создавая.<br><em>Создавать, исследуя.</em></h2><p>Каталог объединяет оборудование для школьных мастерских и лабораторий: от первых экспериментов с роботами до точной обработки деталей.</p></section>
  </main>
</template>
