<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import QRCode from 'qrcode'
import { createMachine, createZone as addZoneRequest, deleteMachine, deleteZone as deleteZoneRequest, getMachines, getZones, updateMachine, updateZone, verifyAdmin } from '../services/api'

const username = ref('moderator1474')
const password = ref('')
const authenticated = ref(false)
const busy = ref(false)
const error = ref('')
const notice = ref('')
const machines = ref([])
const zones = ref([])
const showForm = ref(false)
const editingId = ref(null)
const zoneForm = reactive({ name: '', description: '' })
const editingZoneId = ref(null)
const form = reactive({ name: '', description: '', image_url: '', zone_id: '', quantity: 1, status: 'available', specs_text: '{}' })
const qrMachine = ref(null)
const qrImage = ref('')
const submitLabel = computed(() => editingId.value ? 'Сохранить изменения' : 'Добавить оборудование')

async function loadData() { [zones.value, machines.value] = await Promise.all([getZones(), getMachines()]) }
async function login() {
  error.value = ''; busy.value = true
  try { await verifyAdmin(username.value, password.value); authenticated.value = true; await loadData() }
  catch (e) { error.value = e.response?.data?.detail || 'Проверьте логин и пароль администратора.' }
  finally { busy.value = false }
}
function logout() { password.value = ''; authenticated.value = false }
function clearForm() { editingId.value = null; Object.assign(form, { name: '', description: '', image_url: '', zone_id: zones.value[0]?.id || '', quantity: 1, status: 'available', specs_text: '{}' }); showForm.value = true }
function edit(machine) { editingId.value = machine.id; Object.assign(form, { name: machine.name, description: machine.description, image_url: machine.image_url || '', zone_id: machine.zone_id, quantity: machine.quantity, status: machine.status, specs_text: JSON.stringify(machine.specs || {}, null, 2) }); showForm.value = true }
async function saveMachine() {
  error.value = ''; notice.value = ''
  let specs
  try { specs = JSON.parse(form.specs_text || '{}'); if (!specs || Array.isArray(specs) || typeof specs !== 'object') throw new Error() }
  catch { error.value = 'Характеристики должны быть корректным JSON-объектом.'; return }
  busy.value = true
  const data = { name: form.name, description: form.description, image_url: form.image_url || null, zone_id: Number(form.zone_id), quantity: Number(form.quantity), status: form.status, specs }
  try { if (editingId.value) await updateMachine(username.value, password.value, editingId.value, data); else await createMachine(username.value, password.value, data); await loadData(); showForm.value = false; notice.value = 'Изменения сохранены.' }
  catch (e) { error.value = e.response?.data?.detail || 'Не удалось сохранить оборудование.' }
  finally { busy.value = false }
}
async function remove(machine) {
  if (!window.confirm(`Удалить «${machine.name}»?`)) return
  error.value = ''; busy.value = true
  try { await deleteMachine(username.value, password.value, machine.id); await loadData(); notice.value = 'Оборудование удалено.' }
  catch (e) { error.value = e.response?.data?.detail || 'Не удалось удалить оборудование.' }
  finally { busy.value = false }
}
async function addZone() {
  error.value = ''; busy.value = true
  try {
    const data = { ...zoneForm }
    if (editingZoneId.value) await updateZone(username.value, password.value, editingZoneId.value, data)
    else await addZoneRequest(username.value, password.value, data)
    editingZoneId.value = null; zoneForm.name = ''; zoneForm.description = ''; await loadData(); notice.value = 'Раздел сохранён.'
  }
  catch (e) { error.value = e.response?.data?.detail || 'Не удалось добавить раздел.' }
  finally { busy.value = false }
}
function editZone(zone) { editingZoneId.value = zone.id; Object.assign(zoneForm, { name: zone.name, description: zone.description }); document.getElementById('zone-editor')?.scrollIntoView({ behavior: 'smooth', block: 'center' }) }
async function removeZone(zone) {
  if (zone.machines_count) { error.value = 'Сначала перенесите или удалите оборудование из этого раздела.'; return }
  if (!window.confirm(`Удалить раздел «${zone.name}»?`)) return
  busy.value = true; error.value = ''
  try { await deleteZoneRequest(username.value, password.value, zone.id); await loadData(); notice.value = 'Раздел удалён.' }
  catch (e) { error.value = e.response?.data?.detail || 'Не удалось удалить раздел.' }
  finally { busy.value = false }
}
async function showQr(machine) {
  qrMachine.value = machine
  qrImage.value = await QRCode.toDataURL(`${window.location.origin}/machines/${machine.id}`, { width: 320, margin: 2, errorCorrectionLevel: 'H', color: { dark: '#160b26', light: '#ffffff' } })
}
function printQr() {
  if (!qrMachine.value || !qrImage.value) return
  const popup = window.open('', '_blank', 'width=460,height=560')
  if (!popup) { error.value = 'Разрешите всплывающие окна, чтобы распечатать QR-код.'; return }
  const safeName = qrMachine.value.name.replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char])
  popup.document.write(`<!doctype html><html lang="ru"><meta charset="utf-8"><title>QR — ${safeName}</title><style>body{font:16px Arial,sans-serif;text-align:center;padding:24px;color:#17131f}img{width:300px;height:300px}h1{font-size:20px}p{font-size:12px;color:#555}</style><h1>${safeName}</h1><img src="${qrImage.value}" alt="QR-код"><p>Сканируйте, чтобы открыть карточку оборудования</p><script>window.onload=()=>window.print()<\/script></html>`)
  popup.document.close()
}
</script>

<template>
  <main class="admin-page">
    <RouterLink to="/" class="edu-back">← На сайт</RouterLink>
    <section v-if="!authenticated" class="admin-login"><div class="edu-kicker"><span></span> ДОСТУП СОТРУДНИКАМ</div><h1>Вход в админку</h1><p>Войдите, чтобы управлять оборудованием и QR-кодами.</p><form @submit.prevent="login"><label>Логин<input v-model="username" autocomplete="username" required></label><label>Пароль<input v-model="password" type="password" autocomplete="current-password" required></label><button class="edu-primary" :disabled="busy">{{ busy ? 'Проверяем…' : 'Войти' }} <span>→</span></button></form><p v-if="error" class="admin-error">{{ error }}</p></section>

    <template v-else>
      <div class="admin-heading"><div><div class="edu-kicker"><span></span> УПРАВЛЕНИЕ КАТАЛОГОМ</div><h1>Админ-панель</h1><p>Добавляйте, редактируйте и удаляйте оборудование.</p></div><button class="admin-logout" @click="logout">Выйти</button></div>
      <p v-if="notice" class="admin-notice">{{ notice }}</p><p v-if="error" class="admin-error">{{ error }}</p>

      <section class="admin-section"><div class="admin-section-head"><h2>Оборудование <span>{{ machines.length }}</span></h2><button class="edu-primary" @click="clearForm">+ Добавить позицию</button></div>
        <form v-if="showForm" class="admin-form" @submit.prevent="saveMachine"><h3>{{ editingId ? 'Редактирование позиции' : 'Новая позиция' }}</h3><div class="admin-fields"><label>Название<input v-model="form.name" required maxlength="150"></label><label>Раздел<select v-model="form.zone_id" required><option v-for="zone in zones" :key="zone.id" :value="zone.id">{{ zone.name }}</option></select></label><label class="wide">Описание<textarea v-model="form.description" rows="3"></textarea></label><label class="wide">Ссылка на изображение<input v-model="form.image_url" type="url" placeholder="https://…"></label><label>Количество<input v-model.number="form.quantity" type="number" min="1" required></label><label>Состояние<select v-model="form.status"><option value="available">Доступно</option><option value="maintenance">На обслуживании</option></select></label><label class="wide">Характеристики (JSON)<textarea v-model="form.specs_text" rows="4" spellcheck="false"></textarea></label></div><div class="admin-form-actions"><button class="edu-primary" :disabled="busy">{{ submitLabel }}</button><button type="button" class="admin-cancel" @click="showForm = false">Отмена</button></div></form>
        <div class="admin-table-wrap"><table class="admin-table"><thead><tr><th>Оборудование</th><th>Раздел</th><th>Кол-во</th><th>Состояние</th><th></th></tr></thead><tbody><tr v-for="machine in machines" :key="machine.id"><td><strong>{{ machine.name }}</strong><small>ID {{ machine.id }}</small></td><td>{{ zones.find(zone => zone.id === machine.zone_id)?.name }}</td><td>{{ machine.quantity }}</td><td><span class="admin-status" :class="machine.status">{{ machine.status === 'available' ? 'Доступно' : 'Обслуживание' }}</span></td><td class="admin-actions"><button @click="showQr(machine)">QR / печать</button><button @click="edit(machine)">Изменить</button><button class="danger" :disabled="busy" @click="remove(machine)">Удалить</button></td></tr></tbody></table></div>
      </section>
      <section class="admin-section"><h2>Разделы каталога</h2><div class="admin-zone-grid"><div v-for="zone in zones" :key="zone.id" class="admin-zone"><b>{{ zone.name }}</b><span>{{ zone.machines_count }} позиций</span><button @click="editZone(zone)">Изменить</button><button :disabled="busy || zone.machines_count > 0" @click="removeZone(zone)">Удалить</button></div></div><form id="zone-editor" class="admin-zone-form" @submit.prevent="addZone"><label>{{ editingZoneId ? 'Название раздела' : 'Новый раздел' }}<input v-model="zoneForm.name" required maxlength="100" placeholder="Например, Лазерная резка"></label><label>Описание<input v-model="zoneForm.description" placeholder="Краткое описание"></label><div class="zone-form-actions"><button class="edu-primary" :disabled="busy">{{ editingZoneId ? 'Сохранить раздел' : 'Добавить раздел' }}</button><button v-if="editingZoneId" type="button" class="admin-cancel" @click="editingZoneId = null; zoneForm.name = ''; zoneForm.description = ''">Отмена</button></div></form></section>
      <div v-if="qrMachine" class="qr-overlay" @click.self="qrMachine = null"><section class="qr-dialog"><button class="qr-close" aria-label="Закрыть" @click="qrMachine = null">×</button><h2>{{ qrMachine.name }}</h2><img :src="qrImage" alt="QR-код для карточки оборудования"><p>QR-код откроет карточку этого оборудования на сайте.</p><button class="edu-primary" @click="printQr">Распечатать QR-код</button></section></div>
    </template>
  </main>
</template>
