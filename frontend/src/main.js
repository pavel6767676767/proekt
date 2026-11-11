import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import CatalogView from './views/CatalogView.vue'
import ProductView from './views/ProductView.vue'
import './style.css'
import './edu.css'

const router = createRouter({ history: createWebHistory(), routes: [
  { path: '/', component: CatalogView },
  { path: '/machines/:id', component: ProductView },
  { path: '/admin', component: () => import('./views/AdminView.vue') },
] })
createApp(App).use(createPinia()).use(router).mount('#app')
