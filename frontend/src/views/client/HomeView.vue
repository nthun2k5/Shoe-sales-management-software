<template>
  <div style="background:#f5f5f5">

    <!-- ── HERO SLIDER ── -->
    <section class="relative overflow-hidden group" style="background:linear-gradient(135deg, #f8fafc, #f1f5f9);height:600px">
      <!-- Loading State -->
      <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-slate-50">
        <div class="flex flex-col items-center gap-4">
          <div class="w-12 h-12 border-4 border-red-100 border-t-red-600 rounded-full animate-spin"></div>
          <p class="text-sm text-slate-400 font-medium">Đang tải siêu phẩm...</p>
        </div>
      </div>

      <!-- Slides -->
      <div v-else v-for="(product, idx) in displaySlides" :key="product.id"
        class="absolute inset-0 flex items-center justify-center transition-all duration-1000 ease-in-out"
        :style="{ 
          opacity: currentSlide === idx ? 1 : 0, 
          zIndex: currentSlide === idx ? 10 : 0, 
          pointerEvents: currentSlide === idx ? 'auto' : 'none',
          visibility: currentSlide === idx ? 'visible' : 'hidden'
        }">
        
        <div class="max-w-7xl mx-auto px-6 lg:px-8 w-full h-full flex flex-col md:flex-row items-center relative z-10">
          
          <!-- Text Content -->
          <div class="w-full md:w-1/2 pt-12 md:pt-0 pr-0 md:pr-12 text-center md:text-left">
            <div class="overflow-hidden mb-4">
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded text-[10px] font-bold uppercase tracking-widest transition-all duration-700"
                :style="{ 
                  background: 'rgba(232,25,26,0.1)', 
                  color: '#e8191a',
                  transform: currentSlide === idx ? 'translateY(0)' : 'translateY(100%)',
                  opacity: currentSlide === idx ? 1 : 0
                }">
                <span class="w-1.5 h-1.5 rounded-full animate-pulse" style="background:#e8191a"></span>
                {{ product.thuong_hieu || 'BST Mới Nhất' }}
              </div>
            </div>
            
            <h1 class="text-4xl md:text-5xl lg:text-7xl font-black text-slate-900 leading-[1.1] mb-6 transition-all duration-700 delay-100"
              :style="{ 
                transform: currentSlide === idx ? 'translateY(0)' : 'translateY(30px)',
                opacity: currentSlide === idx ? 1 : 0
              }">
              {{ product.ten }}
            </h1>
            
            <p class="text-slate-500 mb-8 text-sm md:text-lg max-w-md mx-auto md:mx-0 leading-relaxed transition-all duration-700 delay-200"
              :style="{ 
                transform: currentSlide === idx ? 'translateY(0)' : 'translateY(20px)',
                opacity: currentSlide === idx ? 1 : 0
              }">
              {{ product.mo_ta_ngan || 'Trải nghiệm sự êm ái và phong cách vượt trội cùng siêu phẩm giày mới nhất tại Giày Đẹp Store.' }}
            </p>
            
            <div class="flex flex-wrap justify-center md:justify-start gap-4 transition-all duration-700 delay-300"
              :style="{ 
                transform: currentSlide === idx ? 'translateY(0)' : 'translateY(20px)',
                opacity: currentSlide === idx ? 1 : 0
              }">
              <RouterLink :to="`/products/${product.id}`" class="btn-primary px-10 py-4 text-sm flex items-center gap-3 shadow-xl shadow-red-200">
                Sở hữu ngay
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
              </RouterLink>
              <div class="flex items-center gap-2 px-6 py-4 rounded-lg bg-white shadow-sm border border-slate-100">
                <span class="text-xs text-slate-400 font-medium">Chỉ từ:</span>
                <span class="text-xl font-black text-red-600">{{ formatPrice(product.gia_khuyen_mai || product.gia) }}</span>
              </div>
            </div>
          </div>
 
          <!-- Product Image -->
          <div class="w-full md:w-1/2 h-1/2 md:h-full relative flex items-center justify-center group/img">
            <!-- Decorative circles -->
            <div class="absolute w-[120%] aspect-square bg-red-50 rounded-full -z-10 animate-blob"></div>
            <div class="absolute w-[80%] aspect-square border border-red-100 rounded-full -z-10 animate-blob animation-delay-2000"></div>
            
            <div class="relative transition-all duration-1000 ease-out"
              :style="{ 
                transform: currentSlide === idx ? 'scale(1) rotate(-8deg) translateY(0)' : 'scale(0.8) rotate(10deg) translateY(50px)', 
                opacity: currentSlide === idx ? 1 : 0 
              }">
              <img :src="product.anh_san_phams?.[0]?.du_lieu_anh || '/images/hero1.png'" 
                :alt="product.ten" 
                class="max-w-full max-h-[450px] object-contain drop-shadow-[0_35px_35px_rgba(0,0,0,0.25)] transition-transform duration-700 group-hover/img:scale-110" />
            </div>
          </div>
        </div>
      </div>

      <!-- Slide navigation removed -->
    </section>

    <!-- ── SERVICE STRIP ── -->
    <div class="bg-white border-b border-gray-100 relative" data-aos="fade-up" data-aos-duration="400">
      <div class="max-w-7xl mx-auto px-4">
        <div class="grid grid-cols-2 lg:grid-cols-4">
          <div v-for="(s, i) in services" :key="s.label"
            class="flex items-center gap-4 py-5 px-5 group cursor-default transition-all duration-300 hover:bg-linear-to-r hover:from-red-50 hover:to-transparent relative"
            :class="i < 3 ? 'lg:border-r border-gray-100' : ''">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center shrink-0 transition-all duration-300 group-hover:scale-110 group-hover:shadow-lg"
              :class="s.bg">
              <span class="text-xl">{{ s.icon }}</span>
            </div>
            <div>
              <p class="text-sm font-bold text-gray-900 group-hover:text-red-600 transition-colors">{{ s.label }}</p>
              <p class="text-xs text-gray-400 mt-0.5">{{ s.sub }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── CATEGORIES ── -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10" data-aos="fade-up">
      <div class="flex items-center justify-between mb-6">
        <h2 class="section-title">Danh mục nổi bật</h2>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        <RouterLink
          v-for="cat in categories"
          :key="cat.id"
          :to="`/products?danh_muc=${cat.id}`"
          class="cat-card group rounded-lg overflow-hidden"
          style="aspect-ratio:3/4;background:#eee">
          <div class="w-full h-full relative overflow-hidden">
            <img v-if="cat.anh" :src="cat.anh" :alt="cat.ten" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
            <div v-else class="absolute inset-0 flex items-center justify-center" style="background:linear-gradient(135deg,#1a1a1a,#333)">
              <span class="text-5xl select-none">👟</span>
            </div>
            
            <!-- Dark overlay for readability -->
            <div v-if="cat.anh" class="absolute inset-0 bg-black/30 group-hover:bg-black/20 transition-colors"></div>

            <div class="cat-card-overlay">
              <h3 class="font-bold text-white text-base">{{ cat.ten }}</h3>
              <p class="text-xs text-white/70 mt-0.5">{{ cat.so_luong_san_pham || 0 }} sản phẩm</p>
            </div>
            <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-x-2 group-hover:translate-x-0">
              <div class="w-7 h-7 rounded-full bg-white/20 backdrop-blur flex items-center justify-center">
                <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>
          </div>
        </RouterLink>
      </div>
    </section>

    <!-- ── FLASH SALE ── -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-10" data-aos="fade-up" data-aos-delay="100">
      <div class="rounded-lg overflow-hidden" style="background:white;box-shadow:0 2px 12px rgba(0,0,0,0.06)">
        <!-- Header -->
        <div class="flash-sale-header px-6 py-4 flex items-center justify-between flex-wrap gap-4">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <span class="text-2xl">⚡</span>
              <span class="text-white font-black text-xl uppercase tracking-wide">Flash Sale</span>
            </div>
            <!-- Countdown -->
            <div class="flex items-center gap-1">
              <div class="countdown-box">{{ countdown.h }}</div>
              <span class="countdown-sep">:</span>
              <div class="countdown-box">{{ countdown.m }}</div>
              <span class="countdown-sep">:</span>
              <div class="countdown-box">{{ countdown.s }}</div>
            </div>
          </div>
          <RouterLink to="/products" class="text-white/80 text-sm font-semibold hover:text-white flex items-center gap-1 transition-colors">
            Xem tất cả
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/></svg>
          </RouterLink>
        </div>

        <!-- Flash sale products -->
        <div class="p-4 relative">
          <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
            <div v-for="i in 5" :key="i" class="rounded overflow-hidden">
              <div class="skeleton" style="height:180px"></div>
              <div class="p-2 space-y-2">
                <div class="skeleton h-3 w-3/4"></div>
                <div class="skeleton h-4 w-1/2"></div>
              </div>
            </div>
          </div>
          
          <div v-else-if="error" class="text-center py-8 text-red-500 font-medium">
            {{ error }}
          </div>
          
          <!-- Product Carousel -->
          <div v-else class="relative group/slider">
            <div id="flash-sale-slider" class="flex gap-4 overflow-x-auto pb-4 scrollbar-hide scroll-smooth snap-x snap-mandatory">
              <div v-for="(product, index) in featuredProducts" :key="product.id"
                class="min-w-[180px] sm:min-w-[220px] md:min-w-[240px] snap-start"
                data-aos="fade-up" :data-aos-delay="index * 50">
                
                <div class="product-card group" @click="$router.push(`/products/${product.id}`)">
                  <!-- Image -->
                  <div class="relative overflow-hidden bg-gray-50" style="aspect-ratio:1">
                    <img v-if="product.anh_san_phams?.[0]?.du_lieu_anh"
                      :src="product.anh_san_phams[0].du_lieu_anh" :alt="product.ten"
                      class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                      loading="lazy" @error="handleImgError" />
                    <div v-else class="w-full h-full flex items-center justify-center text-gray-200 text-5xl">👟</div>
                    
                    <!-- Discount badge -->
                    <span v-if="product.gia_khuyen_mai" class="sale-badge">
                      -{{ Math.round((1 - product.gia_khuyen_mai / product.gia) * 100) }}%
                    </span>
                    
                    <!-- Wishlist -->
                    <button @click.stop="quickToggleWishlist(product)"
                      class="absolute top-2 right-2 w-8 h-8 rounded-full bg-white/90 backdrop-blur shadow-sm flex items-center justify-center text-gray-400 hover:text-pink-500 transition-all duration-300 opacity-0 group-hover:opacity-100 -translate-y-2 group-hover:translate-y-0"
                      :class="{'text-pink-500 opacity-100 translate-y-0': isWishlisted(product.id)}">
                      <svg class="w-4 h-4" :fill="isWishlisted(product.id) ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                    </button>

                    <!-- Quick add -->
                    <button @click.stop="quickAddToCart(product)"
                      class="absolute bottom-2 right-2 w-8 h-8 rounded-full bg-white shadow-lg flex items-center justify-center text-gray-600 hover:text-white transition-all duration-300 opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0"
                      @mouseenter="e=>{ e.currentTarget.style.background='#e8191a'; e.currentTarget.style.color='white' }"
                      @mouseleave="e=>{ e.currentTarget.style.background='white'; e.currentTarget.style.color='#444' }">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
                    </button>
                  </div>
                  <!-- Info -->
                  <div class="p-3">
                    <p v-if="product.ten_danh_muc" class="text-[10px] font-semibold uppercase tracking-wide mb-1" style="color:#e8191a">{{ product.ten_danh_muc }}</p>
                    <h3 class="text-xs font-semibold text-gray-800 line-clamp-2 mb-2 leading-snug">{{ product.ten }}</h3>
                    <div class="flex items-baseline gap-1.5">
                      <span class="text-sm font-black" style="color:#e8191a">{{ formatPrice(product.gia_khuyen_mai || product.gia) }}</span>
                      <span v-if="product.gia_khuyen_mai" class="text-[10px] text-gray-400 line-through">{{ formatPrice(product.gia) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Carousel arrows removed -->
          </div>
        </div>
      </div>
    </section>

    <!-- ── BANNER PAIR ── -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-10">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <RouterLink to="/products?danh_muc=1"
          class="relative rounded-lg overflow-hidden flex items-center justify-between px-8 py-10 group"
          style="background:linear-gradient(135deg,#1a1a1a,#333);min-height:160px">
          <div>
            <p class="text-xs text-gray-400 uppercase tracking-wider mb-1">Bộ sưu tập 2026</p>
            <h3 class="text-2xl font-black text-white mb-3">Giày Nam</h3>
            <span class="text-xs font-bold text-white px-4 py-2 rounded inline-block transition-all group-hover:scale-105"
              style="background:#e8191a">Mua ngay →</span>
          </div>
          <span class="text-7xl opacity-60 group-hover:scale-110 transition-transform duration-500 select-none">👟</span>
        </RouterLink>
        <RouterLink to="/products?danh_muc=2"
          class="relative rounded-lg overflow-hidden flex items-center justify-between px-8 py-10 group"
          style="background:linear-gradient(135deg,#2d1a1a,#4d2626);min-height:160px">
          <div>
            <p class="text-xs text-gray-400 uppercase tracking-wider mb-1">Phong cách thời thượng</p>
            <h3 class="text-2xl font-black text-white mb-3">Giày Nữ</h3>
            <span class="text-xs font-bold text-white px-4 py-2 rounded inline-block transition-all group-hover:scale-105"
              style="background:#e8191a">Mua ngay →</span>
          </div>
          <span class="text-7xl opacity-60 group-hover:scale-110 transition-transform duration-500 select-none">👠</span>
        </RouterLink>
      </div>
    </section>

    <!-- ── NEW ARRIVALS ── -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-10">
      <div style="background:white;border-radius:8px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.06)">
        <div class="flex items-center justify-between mb-6">
          <h2 class="section-title">Sản phẩm mới nhất</h2>
          <RouterLink to="/products" class="text-sm font-bold flex items-center gap-1 hover:gap-2 transition-all"
            style="color:#e8191a">
            Xem tất cả
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/></svg>
          </RouterLink>
        </div>

        <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <div v-for="i in 10" :key="i" class="rounded overflow-hidden">
            <div class="skeleton" style="height:200px"></div>
            <div class="p-3 space-y-2">
              <div class="skeleton h-3 w-3/4"></div>
              <div class="skeleton h-4 w-1/2"></div>
            </div>
          </div>
        </div>

        <div v-else-if="error" class="text-center py-8 text-red-500">
          {{ error }}
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <div v-for="(product, index) in newProducts" :key="product.id"
            class="product-card group"
            data-aos="fade-up" :data-aos-delay="index * 50"
            @click="$router.push(`/products/${product.id}`)">
            <div class="relative overflow-hidden bg-gray-50" style="aspect-ratio:1">
              <img v-if="product.anh_san_phams?.[0]?.du_lieu_anh"
                :src="product.anh_san_phams[0].du_lieu_anh" :alt="product.ten"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                loading="lazy" @error="handleImgError" />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-200 text-5xl">👟</div>
              <span class="new-badge">Mới</span>
              <span v-if="product.gia_khuyen_mai" class="absolute top-8 left-2 sale-badge">
                -{{ Math.round((1 - product.gia_khuyen_mai / product.gia) * 100) }}%
              </span>
              
              <!-- Wishlist -->
              <button @click.stop="quickToggleWishlist(product)"
                class="absolute top-2 right-2 w-8 h-8 rounded-full bg-white/90 backdrop-blur shadow-sm flex items-center justify-center text-gray-400 hover:text-pink-500 transition-all duration-300 opacity-0 group-hover:opacity-100 -translate-y-2 group-hover:translate-y-0"
                :class="{'text-pink-500 opacity-100 translate-y-0': isWishlisted(product.id)}">
                <svg class="w-4 h-4" :fill="isWishlisted(product.id) ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
              </button>
              <button @click.stop="quickAddToCart(product)"
                class="absolute bottom-2 right-2 w-8 h-8 rounded-full bg-white shadow-lg flex items-center justify-center transition-all duration-300 opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0"
                @mouseenter="e=>{ e.currentTarget.style.background='#e8191a'; e.currentTarget.style.color='white' }"
                @mouseleave="e=>{ e.currentTarget.style.background='white'; e.currentTarget.style.color='#444' }">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
              </button>
            </div>
            <div class="p-3">
              <p v-if="product.ten_danh_muc" class="text-[10px] font-semibold uppercase tracking-wide mb-1" style="color:#999">{{ product.ten_danh_muc }}</p>
              <h3 class="text-xs font-semibold text-gray-800 line-clamp-2 mb-2 leading-snug">{{ product.ten }}</h3>
              <div class="flex items-baseline gap-1.5">
                <span class="text-sm font-black" style="color:#e8191a">{{ formatPrice(product.gia_khuyen_mai || product.gia) }}</span>
                <span v-if="product.gia_khuyen_mai" class="text-[10px] text-gray-400 line-through">{{ formatPrice(product.gia) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>


  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const authStore = useAuthStore()
const { success } = useToast()

const featuredProducts = ref([])
const newProducts = ref([])
const categories = ref([])
const loading = ref(true)
const error = ref(null)
const currentSlide = ref(0)
let slideTimer = null
let countdownTimer = null

const displaySlides = computed(() => {
  if (featuredProducts.value.length > 0) {
    return featuredProducts.value.slice(0, 3)
  }
  return []
})

const services = [
  { icon: '🚚', label: 'Miễn phí vận chuyển', sub: 'Đơn hàng từ 500K', bg: 'bg-blue-50' },
  { icon: '🔄', label: 'Đổi trả dễ dàng', sub: 'Trong vòng 30 ngày', bg: 'bg-green-50' },
  { icon: '✅', label: 'Hàng chính hãng', sub: 'Cam kết 100%', bg: 'bg-amber-50' },
  { icon: '📞', label: 'Hỗ trợ 24/7', sub: 'Hotline: 0123 456 789', bg: 'bg-red-50' },
]

// Countdown (end of day)
const now = new Date()
const endOfDay = new Date(now)
endOfDay.setHours(23, 59, 59, 0)
const countdown = ref({ h: '00', m: '00', s: '00' })

function updateCountdown() {
  const diff = Math.max(0, endOfDay - new Date())
  const h = Math.floor(diff / 3600000)
  const m = Math.floor((diff % 3600000) / 60000)
  const s = Math.floor((diff % 60000) / 1000)
  countdown.value = {
    h: String(h).padStart(2, '0'),
    m: String(m).padStart(2, '0'),
    s: String(s).padStart(2, '0'),
  }
}

function nextSlide() { 
  if (displaySlides.value.length > 0) {
    currentSlide.value = (currentSlide.value + 1) % displaySlides.value.length 
  }
}
function prevSlide() { 
  if (displaySlides.value.length > 0) {
    currentSlide.value = (currentSlide.value - 1 + displaySlides.value.length) % displaySlides.value.length 
  }
}

function scrollSlider(id, direction) {
  const el = document.getElementById(id)
  if (el) {
    el.scrollLeft += direction * 300
  }
}

function formatPrice(p) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p)
}

function handleImgError(e) {
  e.target.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8fafc"/><path d="M160 220l30-30a28.28 28.28 0 0140 0l30 30m-30-30l20-20a28.28 28.28 0 0140 0l20 20m-80-80h.01M100 280h200a28.28 28.28 0 0028.28-28.28v-103.44a28.28 28.28 0 00-28.28-28.28H100a28.28 28.28 0 00-28.28 28.28v103.44A28.28 28.28 0 00100 280z" fill="none" stroke="#cbd5e1" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>')))
}

async function quickAddToCart(product) {
  // Redirect to detail page to force size selection
  router.push(`/products/${product.id}`)
}

function isWishlisted(id) {
  return wishlistStore.isWishlisted(id)
}

async function quickToggleWishlist(product) {
  if (!authStore.isLoggedIn) return router.push('/login')
  try {
    await wishlistStore.toggle(product.id)
  } catch {}
}

onMounted(async () => {
  updateCountdown()
  countdownTimer = setInterval(updateCountdown, 1000)
  slideTimer = setInterval(nextSlide, 4000)

  try {
    const [featuredRes, newRes, catsRes] = await Promise.all([
      api.get('/products', { params: { page_size: 10, la_noi_bat: true } }),
      api.get('/products', { params: { page_size: 10 } }),
      api.get('/categories'),
    ])
    featuredProducts.value = featuredRes.data.items?.length ? featuredRes.data.items : newRes.data.items
    newProducts.value = newRes.data.items
    categories.value = catsRes.data
  } catch (e) {
    console.error(e)
    error.value = 'Không thể tải dữ liệu sản phẩm. Vui lòng thử lại sau.'
  } finally { loading.value = false }
})

onUnmounted(() => {
  clearInterval(slideTimer)
  clearInterval(countdownTimer)
})
</script>
 
<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
</style>
