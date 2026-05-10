<template>
  <div>
    <!-- Loading State -->
    <div v-if="loading" class="animate-pulse space-y-6">
      <div class="skeleton h-96 md:h-[500px] w-full rounded-2xl"></div>
      <div class="max-w-4xl mx-auto space-y-3">
        <div class="skeleton h-8 w-1/3"></div>
        <div class="skeleton h-6 w-1/2"></div>
        <div class="skeleton h-4 w-2/3"></div>
      </div>
    </div>

    <div v-else-if="product" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Breadcrumb -->
      <nav class="flex items-center gap-2 text-xs text-gray-400 mb-6">
        <RouterLink to="/" class="hover:text-red-600 transition-colors">Trang chủ</RouterLink>
        <span>/</span>
        <RouterLink to="/products" class="hover:text-red-600 transition-colors">Sản phẩm</RouterLink>
        <span v-if="product.ten_danh_muc">/</span>
        <RouterLink v-if="product.ten_danh_muc" :to="`/products?danh_muc=${product.id_danh_muc}`" class="hover:text-red-600 transition-colors">{{ product.ten_danh_muc }}</RouterLink>
        <span>/</span>
        <span class="text-gray-600">{{ product.ten }}</span>
      </nav>

      <!-- Product Main -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
        <!-- Image Gallery -->
        <div class="space-y-4">
          <!-- Main Image -->
          <div class="relative aspect-[4/5] bg-gray-50 rounded-3xl overflow-hidden group shadow-sm border border-gray-100">
            <img
              v-if="mainImage"
              :src="mainImage"
              :alt="product.ten"
              class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
              id="main-product-image"
              @error="handleImgError"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
              <svg class="w-20 h-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            </div>
            <!-- Discount badge on image -->
            <div v-if="product.gia_khuyen_mai" class="absolute top-6 left-6 bg-red-600 text-white text-[10px] font-black px-4 py-2 rounded-full shadow-2xl uppercase tracking-widest animate-bounce">
              Giảm {{ Math.round((1 - product.gia_khuyen_mai / product.gia) * 100) }}%
            </div>
            
            <!-- Quick Action Overlay -->
            <div class="absolute inset-x-0 bottom-0 p-6 bg-linear-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex justify-center items-center">
               <button @click="mainImage = product.anh_san_phams[0].du_lieu_anh" class="bg-white/90 backdrop-blur-md text-gray-900 px-6 py-2.5 rounded-full text-xs font-bold shadow-xl hover:bg-white transition-all">Xem ảnh gốc</button>
            </div>
          </div>

          <!-- Thumbnail Gallery -->
          <div v-if="product.anh_san_phams?.length > 1" class="flex gap-3 overflow-x-auto pb-2 custom-scrollbar">
            <button
              v-for="(img, idx) in product.anh_san_phams"
              :key="img.id"
              @click="mainImage = img.du_lieu_anh; selectedIdx = idx"
              :class="['w-20 h-20 rounded-2xl overflow-hidden border-2 shrink-0 transition-all duration-300', mainImage === img.du_lieu_anh ? 'border-red-600 ring-4 ring-red-50' : 'border-gray-100 hover:border-red-200']"
            >
              <img :src="img.du_lieu_anh" class="w-full h-full object-cover" @error="handleImgError" />
            </button>
          </div>
        </div>

        <!-- Product Details -->
        <div class="lg:pl-4">
          <!-- Category & Stock -->
          <div class="flex items-center justify-between mb-4">
            <span v-if="product.ten_danh_muc" class="inline-block px-4 py-1.5 bg-gray-900 text-white text-[10px] font-black uppercase tracking-widest rounded-full">{{ product.ten_danh_muc }}</span>
            <span v-if="product.so_luong_ton > 0" class="text-xs font-bold" :class="product.so_luong_ton < 10 ? 'text-red-500' : 'text-green-500'">
               {{ product.so_luong_ton < 10 ? `Chỉ còn ${product.so_luong_ton} đôi cuối` : 'Còn hàng' }}
            </span>
          </div>

          <!-- Title -->
          <h1 class="text-3xl md:text-4xl font-black text-gray-900 mb-4 tracking-tight leading-tight">{{ product.ten }}</h1>

          <!-- Rating -->
          <div class="flex items-center gap-4 mb-8">
            <div class="flex items-center gap-1.5 px-3 py-1.5 bg-amber-50 rounded-xl">
               <span class="text-amber-500 font-black text-sm">{{ product.diem_danh_gia_tb || '5.0' }}</span>
               <div class="flex">
                  <span v-for="i in 5" :key="i" class="text-xs" :class="i <= Math.round(product.diem_danh_gia_tb || 5) ? 'text-amber-400' : 'text-gray-200'">★</span>
               </div>
            </div>
            <span class="w-px h-4 bg-gray-200"></span>
            <span class="text-sm text-gray-500 font-medium">{{ product.so_luong_danh_gia || 0 }} Đánh giá</span>
            <span class="w-px h-4 bg-gray-200"></span>
            <span class="text-sm text-gray-500 font-medium">100+ Đã bán</span>
          </div>

          <!-- Price Card -->
          <div class="bg-gray-50 rounded-3xl p-6 mb-8 border border-gray-100 relative overflow-hidden">
             <div class="absolute top-0 right-0 w-32 h-32 bg-red-500/5 rounded-full -mr-16 -mt-16 blur-2xl"></div>
             <div class="flex items-baseline gap-4 mb-1">
                <span class="text-4xl font-black text-red-600">{{ formatPrice(product.gia_khuyen_mai || product.gia) }}</span>
                <span v-if="product.gia_khuyen_mai" class="text-xl text-gray-400 line-through font-medium">{{ formatPrice(product.gia) }}</span>
             </div>
             <p v-if="product.gia_khuyen_mai" class="text-sm text-red-500 font-bold flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
                Giá tốt nhất thị trường — Tiết kiệm {{ formatPrice(product.gia - product.gia_khuyen_mai) }}
             </p>
          </div>

          <!-- Size Selector -->
          <div v-if="product.so_luong_ton > 0 && availableSizes.length > 0" class="mb-8">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-sm font-black text-gray-900 uppercase tracking-widest">Chọn Kích Thước</h4>
              <button class="text-[10px] text-gray-400 hover:text-red-600 font-bold uppercase tracking-widest flex items-center gap-1 transition-colors">
                 <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18" stroke-width="3"/></svg>
                 Bảng Size
              </button>
            </div>
            <div class="grid grid-cols-5 sm:grid-cols-8 gap-3">
              <button
                v-for="s in availableSizes" :key="s"
                @click="selectedSize = s; sizeError = false"
                :class="['h-12 rounded-2xl border-2 text-sm font-black transition-all duration-300 relative group overflow-hidden',
                  selectedSize === s
                    ? 'border-red-600 bg-red-600 text-white shadow-xl shadow-red-200'
                    : 'border-gray-100 text-gray-600 hover:border-red-600 hover:bg-red-50']"
              >
                {{ s }}
                <span v-if="selectedSize === s" class="absolute top-0 right-0 w-3 h-3 bg-white rotate-45 translate-x-1.5 -translate-y-1.5"></span>
              </button>
            </div>
            <Transition name="fade">
               <p v-if="sizeError" class="text-red-500 text-[10px] mt-3 font-black uppercase tracking-widest flex items-center gap-2">
                 <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2.5"/></svg>
                 Vui lòng chọn size để đặt hàng
               </p>
            </Transition>
          </div>

          <!-- Quantity & Actions -->
          <div v-if="product.so_luong_ton > 0" class="flex flex-col sm:flex-row items-stretch gap-4 mb-8">
            <div class="flex items-center border-2 border-gray-100 rounded-2xl bg-white h-14 p-1">
              <button @click="qty > 1 && qty--" class="w-12 h-full rounded-xl hover:bg-gray-50 text-gray-400 hover:text-red-600 transition-colors font-black text-xl flex items-center justify-center">−</button>
              <span class="w-12 text-center text-sm font-black text-gray-900">{{ qty }}</span>
              <button @click="qty < product.so_luong_ton && qty++" class="w-12 h-full rounded-xl hover:bg-gray-50 text-gray-400 hover:text-red-600 transition-colors font-black text-xl flex items-center justify-center">+</button>
            </div>
            <button @click="addToCart" class="flex-1 bg-red-600 text-white font-black text-sm uppercase tracking-widest h-14 rounded-2xl hover:bg-gray-900 transition-all shadow-2xl shadow-red-500/20 active:scale-95 flex items-center justify-center gap-3">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
              Thêm Vào Giỏ Hàng
            </button>
            <button @click="toggleWishlist" class="w-14 h-14 rounded-2xl border-2 flex items-center justify-center transition-all duration-300" 
              :class="isWishlisted ? 'border-pink-100 bg-pink-50 text-pink-500 shadow-lg shadow-pink-100' : 'border-gray-100 text-gray-400 hover:border-pink-200 hover:text-pink-500 hover:bg-pink-50'">
              <svg class="w-6 h-6" :fill="isWishlisted ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
            </button>
          </div>

          <!-- Trust Badges -->
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 py-8 border-t border-gray-100">
             <div class="flex flex-col items-center text-center gap-2 group">
                <div class="w-10 h-10 rounded-full bg-red-50 flex items-center justify-center text-red-600 group-hover:scale-110 transition-transform">
                   <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-width="3"/></svg>
                </div>
                <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">Chính Hãng 100%</p>
             </div>
             <div class="flex flex-col items-center text-center gap-2 group">
                <div class="w-10 h-10 rounded-full bg-red-50 flex items-center justify-center text-red-600 group-hover:scale-110 transition-transform">
                   <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2.5"/></svg>
                </div>
                <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">Giao Hỏa Tốc</p>
             </div>
             <div class="flex flex-col items-center text-center gap-2 group sm:col-span-1 col-span-2">
                <div class="w-10 h-10 rounded-full bg-red-50 flex items-center justify-center text-red-600 group-hover:scale-110 transition-transform">
                   <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke-width="2.5"/></svg>
                </div>
                <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">30 Ngày Đổi Trả</p>
             </div>
          </div>

          <!-- Product Info -->
          <div v-if="product.thuong_hieu || product.ma_sku" class="grid grid-cols-2 gap-4 mb-8 text-sm">
            <div v-if="product.thuong_hieu" class="flex gap-2">
              <span class="text-gray-400">Thương hiệu:</span>
              <span class="font-medium text-gray-700">{{ product.thuong_hieu }}</span>
            </div>
            <div v-if="product.ma_sku" class="flex gap-2">
              <span class="text-gray-400">Mã SP:</span>
              <span class="font-medium text-gray-700">{{ product.ma_sku }}</span>
            </div>
          </div>

          <!-- Description -->
          <div v-if="product.mo_ta" class="border-t border-gray-100 pt-8">
            <h3 class="font-bold text-gray-900 mb-4">Mô tả sản phẩm</h3>
            <div class="text-gray-600 leading-relaxed text-sm whitespace-pre-line">{{ product.mo_ta }}</div>
          </div>
        </div>
      </div>

      <!-- Reviews -->
      <div class="border-t border-gray-200 pt-10">
        <h2 class="text-2xl font-bold text-gray-900 mb-8">Đánh giá sản phẩm ({{ reviews.length }})</h2>
        <div v-if="reviews.length > 0" class="space-y-4 max-w-4xl">
          <div v-for="review in reviews" :key="review.id" class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center text-red-600 font-bold text-sm">{{ review.ho_ten?.charAt(0) || 'U' }}</div>
              <div>
                <p class="text-sm font-semibold text-gray-900">{{ review.ho_ten }}</p>
                <div class="flex">
                  <span v-for="i in 5" :key="i" class="text-sm" :class="i <= review.diem_danh_gia ? 'text-amber-400' : 'text-gray-200'">★</span>
                </div>
              </div>
            </div>
            <p class="text-sm text-gray-600 leading-relaxed">{{ review.binh_luan }}</p>
          </div>
        </div>
        <div v-else class="bg-gray-50 rounded-2xl p-8 text-center max-w-4xl">
          <p class="text-gray-500">Chưa có đánh giá nào cho sản phẩm này.</p>
        </div>
      </div>
    </div>

    <!-- Not Found / Error -->
    <div v-else class="text-center py-20">
      <svg class="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      <p class="text-red-500 text-lg">{{ error || 'Sản phẩm không tồn tại' }}</p>
      <RouterLink to="/products" class="btn-primary mt-4 inline-block">Xem sản phẩm khác</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const authStore = useAuthStore()
const { success, error: showError } = useToast()

const product = ref(null)
const reviews = ref([])
const loading = ref(true)
const error = ref(null)
const qty = ref(1)
const mainImage = ref(null)
const selectedIdx = ref(0)
const selectedSize = ref(null)
const sizeError = ref(false)

const availableSizes = computed(() => {
  if (product.value && product.value.cac_kich_thuoc) {
    return product.value.cac_kich_thuoc.split(',').map(s => s.trim()).filter(s => s)
  }
  return [] // No sizes configured
})

const isWishlisted = computed(() => product.value ? wishlistStore.isWishlisted(product.value.id) : false)

function formatPrice(p) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p)
}

async function addToCart() {
  if (!authStore.isLoggedIn) return router.push('/login')
  if (availableSizes.value.length > 0 && !selectedSize.value) {
    sizeError.value = true
    return
  }
  sizeError.value = false
  try {
    await cartStore.addToCart(product.value.id, qty.value, selectedSize.value)
    success(selectedSize.value ? `Đã thêm vào giỏ hàng! (Size ${selectedSize.value})` : 'Đã thêm vào giỏ hàng!')
  } catch (e) { showError(e.response?.data?.detail || 'Lỗi') }
}

async function toggleWishlist() {
  if (!authStore.isLoggedIn) return router.push('/login')
  try { await wishlistStore.toggle(product.value.id) } catch {}
}

onMounted(async () => {
  try {
    const [prodRes, revRes] = await Promise.all([
      api.get(`/products/${route.params.id}`),
      api.get(`/reviews/san-pham/${route.params.id}`)
    ])
    product.value = prodRes.data
    reviews.value = revRes.data

    if (product.value.anh_san_phams?.length > 0) {
      const primary = product.value.anh_san_phams.find(i => i.la_anh_chinh)
      mainImage.value = primary ? primary.du_lieu_anh : product.value.anh_san_phams[0].du_lieu_anh
    }
  } catch (e) {
    console.error(e)
    error.value = e.response?.status === 404 ? 'Sản phẩm không tồn tại' : 'Không thể tải thông tin sản phẩm. Vui lòng thử lại sau.'
    product.value = null
  } finally {
    loading.value = false
  }
})

function handleImgError(e) {
  e.target.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8fafc"/><path d="M160 220l30-30a28.28 28.28 0 0140 0l30 30m-30-30l20-20a28.28 28.28 0 0140 0l20 20m-80-80h.01M100 280h200a28.28 28.28 0 0028.28-28.28v-103.44a28.28 28.28 0 00-28.28-28.28H100a28.28 28.28 0 00-28.28 28.28v103.44A28.28 28.28 0 00100 280z" fill="none" stroke="#cbd5e1" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>')))
}
</script>
