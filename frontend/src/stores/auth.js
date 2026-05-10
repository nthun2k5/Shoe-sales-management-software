import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('access_token') || null,
    loading: false,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.user?.vai_tro === 'quan_tri',
    isClient: (state) => state.user?.vai_tro === 'khach',
  },
  actions: {
    async login(email, password) {
      this.loading = true
      try {
        const res = await api.post('/auth/login', { email, mat_khau: password })
        this.token = res.data.access_token
        this.user = res.data.nguoi_dung
        localStorage.setItem('access_token', res.data.access_token)
        localStorage.setItem('refresh_token', res.data.refresh_token)
        localStorage.setItem('user', JSON.stringify(res.data.nguoi_dung))
        return res.data
      } finally {
        this.loading = false
      }
    },
    async register(data) {
      this.loading = true
      try {
        const res = await api.post('/auth/register', {
          email: data.email,
          mat_khau: data.password,
          ho_ten: data.full_name,
          so_dien_thoai: data.phone || null
        })
        this.token = res.data.access_token
        this.user = res.data.nguoi_dung
        localStorage.setItem('access_token', res.data.access_token)
        localStorage.setItem('refresh_token', res.data.refresh_token)
        localStorage.setItem('user', JSON.stringify(res.data.nguoi_dung))
        return res.data
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },
    updateUser(userData) {
      this.user = { ...this.user, ...userData }
      localStorage.setItem('user', JSON.stringify(this.user))
    },
  },
})
