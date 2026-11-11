import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || '/api', timeout: 10000 })
export const getZones = () => api.get('/zones').then(r => r.data)
export const getMachines = (params = {}) => api.get('/machines', { params }).then(r => r.data)
export const getMachine = id => api.get(`/machines/${id}`).then(r => r.data)

const admin = (username, password) => axios.create({ baseURL: import.meta.env.VITE_API_URL || '/api', timeout: 10000, auth: { username, password } })
export const verifyAdmin = (username, password) => axios.post(`${import.meta.env.VITE_API_URL || '/api'}/admin/login`, { username, password }).then(r => r.data)
export const createMachine = (username, password, data) => admin(username, password).post('/machines', data).then(r => r.data)
export const updateMachine = (username, password, id, data) => admin(username, password).put(`/machines/${id}`, data).then(r => r.data)
export const deleteMachine = (username, password, id) => admin(username, password).delete(`/machines/${id}`)
export const createZone = (username, password, data) => admin(username, password).post('/zones', data).then(r => r.data)
export const updateZone = (username, password, id, data) => admin(username, password).put(`/zones/${id}`, data).then(r => r.data)
export const deleteZone = (username, password, id) => admin(username, password).delete(`/zones/${id}`)
