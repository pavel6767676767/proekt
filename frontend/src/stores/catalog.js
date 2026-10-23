import { defineStore } from 'pinia'
import { getCategories, getProducts } from '../services/api'

export const useCatalogStore = defineStore('catalog', {
  state: () => ({ categories: [], products: [], total: 0, selectedCategory: null, loading: false, error: '' }),
  actions: {
    async load() {
      this.loading = true; this.error = ''
      try { this.categories = await getCategories(); const result = await getProducts(this.selectedCategory); this.products = result.items; this.total = result.total }
      catch { this.error = 'Не удалось загрузить каталог. Проверьте, запущен ли API.' }
      finally { this.loading = false }
    },
    async filterBy(id) { this.selectedCategory = id; await this.load() },
  },
})
