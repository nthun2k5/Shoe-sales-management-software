import { defineStore } from 'pinia'
import api from '@/services/api'

export const useWishlistStore = defineStore('wishlist', {
  state: () => ({
    items: [],
    loading: false,
  }),
  getters: {
    isWishlisted: (state) => (productId) => state.items.some(i => i.id_san_pham === productId),
    count: (state) => state.items.length,
  },
  actions: {
    async fetchWishlist() {
      try {
        const res = await api.get('/wishlists')
        this.items = res.data
      } catch { /* ignore */ }
    },
    async toggle(productId) {
      if (this.isWishlisted(productId)) {
        await api.delete(`/wishlists/${productId}`)
        this.items = this.items.filter(i => i.id_san_pham !== productId)
      } else {
        await api.post('/wishlists', { id_san_pham: productId })
        await this.fetchWishlist()
      }
    },
    reset() {
      this.items = []
    }
  },
})
