import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || '/api', timeout: 10000 })
export const getCategories = () => api.get('/categories').then(r => r.data)
export const getProducts = (categoryId = null) => api.get('/products', { params: categoryId ? { category_id: categoryId } : {} }).then(r => r.data)
export const getProduct = id => api.get(`/products/${id}`).then(r => r.data)
