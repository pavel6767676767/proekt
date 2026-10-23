<script setup>
defineProps({ categories: Array, selected: Number })
defineEmits(['select'])
</script>
<template><div class="filters" aria-label="Фильтр по категориям"><button :class="{ active: selected === null }" @click="$emit('select', null)">Всё оборудование</button><button v-for="category in categories" :key="category.id" :class="{ active: selected === category.id }" @click="$emit('select', category.id)">{{ category.name }}</button></div></template>
