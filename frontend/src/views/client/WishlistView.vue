<template>
  <div class="space-y-6 animate-fade-in">
    <div class="flex items-center justify-between mb-10" data-aos="fade-down">
      <div>
        <h1 class="text-3xl font-black text-slate-900 tracking-tight mb-2">Sản phẩm yêu thích</h1>
        <p class="text-slate-500 text-sm font-medium">Lưu giữ những siêu phẩm bạn yêu thích nhất.</p>
      </div>
      <div v-if="wishlistStore.items.length > 0" class="px-4 py-2 bg-red-50 text-red-600 rounded-full text-xs font-bold border border-red-100">
        {{ wishlistStore.items.length }} Sản phẩm
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="wishlistStore.items.length === 0" 
      class="text-center py-24 bg-white rounded-3xl border border-slate-100 shadow-xl shadow-slate-100/50"
      data-aos="zoom-in">
      <div class="w-24 h-24 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-6 text-red-500">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
      </div>
      <h3 class="text-xl font-bold text-slate-900 mb-2">Danh sách trống</h3>
      <p class="text-slate-500 text-sm max-w-xs mx-auto mb-8">Hãy dạo quanh cửa hàng và chọn cho mình những mẫu giày ưng ý nhất nhé!</p>
      <RouterLink to="/products" class="btn-primary px-10 py-4 text-sm inline-flex items-center gap-2 shadow-xl shadow-red-200">
        Khám phá ngay
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
      </RouterLink>
    </div>

    <!-- Grid -->
    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <div v-for="(item, index) in wishlistStore.items" :key="item.id_yeu_thich" 
        class="product-card group bg-white rounded-2xl shadow-sm hover:shadow-2xl transition-all duration-500 border border-slate-50 overflow-hidden"
        data-aos="fade-up" :data-aos-delay="index * 50">
        
        <div class="relative aspect-square overflow-hidden bg-slate-50">
          <img v-if="item.anh_san_pham" :src="item.anh_san_pham" :alt="item.ten" 
            class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
          <div v-else class="w-full h-full flex items-center justify-center text-5xl opacity-20">👟</div>
          
          <!-- Remove button overlay -->
          <button @click.stop="wishlistStore.toggle(item.id_san_pham)"
            class="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/90 backdrop-blur shadow-sm flex items-center justify-center text-red-500 hover:bg-red-500 hover:text-white transition-all duration-300 transform scale-0 group-hover:scale-100">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
          </button>

          <!-- Badges -->
          <span v-if="item.gia_khuyen_mai" class="sale-badge absolute bottom-3 left-3">
            -{{ Math.round((1 - item.gia_khuyen_mai / item.gia) * 100) }}%
          </span>
        </div>

        <div class="p-4">
          <RouterLink :to="`/products/${item.id_san_pham}`" class="block mb-2">
            <h3 class="text-xs font-bold text-slate-800 line-clamp-2 leading-snug group-hover:text-red-600 transition-colors">{{ item.ten }}</h3>
          </RouterLink>
          <div class="flex items-center gap-2 mb-4">
            <span class="text-sm font-black text-red-600">{{ formatPrice(item.gia_khuyen_mai || item.gia) }}</span>
            <span v-if="item.gia_khuyen_mai" class="text-[10px] text-slate-400 line-through">{{ formatPrice(item.gia) }}</span>
          </div>
          
          <button @click="addToCart(item)" 
            class="w-full py-2.5 rounded-xl bg-slate-900 text-white text-[10px] font-black uppercase tracking-widest hover:bg-red-600 transition-all shadow-lg shadow-slate-100 hover:shadow-red-200">
            Thêm vào giỏ
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWishlistStore } from '@/stores/wishlist'
import { useCartStore } from '@/stores/cart'
import { useToast } from '@/composables/useToast'

const router = useRouter()

const wishlistStore = useWishlistStore()
const cartStore = useCartStore()
const { success, error } = useToast()

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }

async function addToCart(item) {
  router.push(`/products/${item.id_san_pham}`)
}

onMounted(() => { wishlistStore.fetchWishlist() })
</script>
