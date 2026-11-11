<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getMachine, getZones } from '../services/api'

const route = useRoute()
const machine = ref(null)
const zone = ref(null)
const error = ref('')
const loading = ref(true)
async function load() {
  loading.value = true
  error.value = ''
  try {
    const [item, zones] = await Promise.all([getMachine(route.params.id), getZones()])
    machine.value = item
    zone.value = zones.find(entry => entry.id === item.zone_id)
  } catch { error.value = 'Не удалось найти оборудование.' }
  finally { loading.value = false }
}
onMounted(load)
watch(() => route.params.id, load)
</script>

<template>
  <main class="edu-detail">
    <RouterLink to="/#catalog" class="edu-back">← Вернуться в каталог</RouterLink>
    <p v-if="loading" class="edu-message">Загружаем…</p><p v-else-if="error" class="edu-message is-error">{{ error }}</p>
    <section v-else-if="machine" class="edu-detail-grid">
      <div class="edu-detail-image"><img v-if="machine.image_url" :src="machine.image_url" :alt="machine.name"><span v-else>⚙️</span></div>
      <div><div class="edu-kicker"><span></span> {{ zone?.name || 'ОБОРУДОВАНИЕ' }} · № {{ String(machine.id).padStart(3, '0') }}</div><h1>{{ machine.name }}</h1><p class="edu-detail-description">{{ machine.description || 'Описание будет добавлено.' }}</p><div class="edu-detail-data"><span>Количество</span><b>{{ machine.quantity }} шт.</b><span>Состояние</span><b>{{ machine.status === 'available' ? 'Доступно' : 'На обслуживании' }}</b><template v-for="(value, key) in machine.specs" :key="key"><span>{{ key }}</span><b>{{ value }}</b></template></div><p class="edu-contact-note">Уточните наличие и характеристики у ответственного за мастерскую.</p></div>
    </section>
  </main>
</template>
