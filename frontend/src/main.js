import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import CatalogView from './views/CatalogView.vue'
import ProductView from './views/ProductView.vue'
import './style.css'

const router = createRouter({ history: createWebHistory(), routes: [
  { path: '/', component: CatalogView },
  { path: '/products/:id', component: ProductView },
] })
createApp(App).use(createPinia()).use(router).mount('#app')
