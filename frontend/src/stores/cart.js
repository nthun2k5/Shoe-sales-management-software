import { defineStore } from 'pinia'
import api from '@/services/api'
import { useAuthStore } from './auth'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    totalItems: 0,
    totalAmount: 0,
    loading: false,
    isDrawerOpen: false,
  }),
  actions: {
    toggleDrawer(open) {
      this.isDrawerOpen = open !== undefined ? open : !this.isDrawerOpen
    },
    async fetchCart() {
      if (!useAuthStore().isLoggedIn) { this.reset(); return }
      this.loading = true
      try {
        const res = await api.get('/cart')
        this.items = res.data.items
        this.totalItems = res.data.tong_so_luong
        this.totalAmount = res.data.tong_tien
      } catch { /* ignore */ }
      finally { this.loading = false }
    },
    async addToCart(productId, quantity = 1, size = null) {
      if (!useAuthStore().isLoggedIn) { window.location.href = '/login'; return }
      const res = await api.post('/cart', { id_san_pham: productId, so_luong: quantity, kich_thuoc: size ? String(size) : null })
      this.items = res.data.items
      this.totalItems = res.data.tong_so_luong
      this.totalAmount = res.data.tong_tien
      this.isDrawerOpen = true
    },
    async updateQuantity(cartId, quantity) {
      if (!useAuthStore().isLoggedIn) { window.location.href = '/login'; return }
      const res = await api.put(`/cart/${cartId}`, { so_luong: quantity })
      this.items = res.data.items
      this.totalItems = res.data.tong_so_luong
      this.totalAmount = res.data.tong_tien
    },
    async removeItem(cartId) {
      if (!useAuthStore().isLoggedIn) { window.location.href = '/login'; return }
      const res = await api.delete(`/cart/${cartId}`)
      this.items = res.data.items
      this.totalItems = res.data.tong_so_luong
      this.totalAmount = res.data.tong_tien
    },
    async clearCart() {
      if (!useAuthStore().isLoggedIn) { window.location.href = '/login'; return }
      await api.delete('/cart')
      this.items = []
      this.totalItems = 0
      this.totalAmount = 0
    },
    reset() {
      this.items = []
      this.totalItems = 0
      this.totalAmount = 0
    }
  },
})
