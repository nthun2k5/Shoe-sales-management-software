<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex flex-col lg:flex-row gap-8">
      <!-- Sidebar Filters -->
      <aside class="lg:w-72 shrink-0">
        <div class="bg-white rounded-3xl shadow-xl shadow-gray-200/50 border border-gray-100 p-7 sticky top-24">
          <div class="flex items-center justify-between mb-8">
            <h3 class="text-lg font-black text-gray-900 tracking-tight flex items-center gap-2">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/></svg>
              Bộ lọc
            </h3>
            <button @click="resetFilters" class="text-xs font-bold text-gray-400 hover:text-red-600 transition-colors uppercase tracking-widest">Làm mới</button>
          </div>

          <!-- Search Box -->
          <div class="mb-8">
            <h4 class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-4">Tìm nhanh</h4>
            <div class="relative group">
              <input
                v-model="searchQueryInput"
                @keyup.enter="applySearch"
                type="text"
                placeholder="Tìm sản phẩm..."
                class="w-full bg-gray-50 border-2 border-transparent focus:border-red-500/20 focus:bg-white rounded-2xl py-3 pl-11 pr-4 text-sm font-medium transition-all outline-none"
              />
              <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-gray-400 group-focus-within:text-red-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
          </div>

          <!-- Category Selection -->
          <div class="mb-8">
            <h4 class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-4">Danh mục</h4>
            <div class="space-y-1.5 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
              <button
                @click="filters.id_danh_muc = null; fetchProducts()"
                class="w-full flex items-center justify-between px-4 py-2.5 rounded-xl text-sm font-bold transition-all group"
                :class="!filters.id_danh_muc ? 'bg-red-600 text-white shadow-lg shadow-red-200' : 'text-gray-600 hover:bg-gray-50'"
              >
                <span>Tất cả</span>
                <span v-if="!filters.id_danh_muc" class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
              </button>
              <button
                v-for="cat in categories"
                :key="cat.id"
                @click="filters.id_danh_muc = cat.id; fetchProducts()"
                class="w-full flex items-center justify-between px-4 py-2.5 rounded-xl text-sm font-bold transition-all group"
                :class="filters.id_danh_muc === cat.id ? 'bg-red-600 text-white shadow-lg shadow-red-200' : 'text-gray-600 hover:bg-gray-50'"
              >
                <span class="line-clamp-1">{{ cat.ten }}</span>
                <span v-if="filters.id_danh_muc === cat.id" class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
              </button>
            </div>
          </div>

          <!-- Price range -->
          <div class="mb-8">
            <h4 class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-4">Khoảng giá</h4>
            <div class="space-y-3">
              <div class="grid grid-cols-2 gap-3">
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[10px] font-bold text-gray-400">Từ</span>
                  <input v-model.number="filters.min_price" @change="fetchProducts" type="number" class="w-full bg-gray-50 border-2 border-transparent focus:border-red-100 rounded-xl py-2.5 pl-8 pr-2 text-xs font-bold outline-none" />
                </div>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[10px] font-bold text-gray-400">Đến</span>
                  <input v-model.number="filters.max_price" @change="fetchProducts" type="number" class="w-full bg-gray-50 border-2 border-transparent focus:border-red-100 rounded-xl py-2.5 pl-8 pr-2 text-xs font-bold outline-none" />
                </div>
              </div>
              <!-- Quick price chips -->
              <div class="flex flex-wrap gap-2 pt-1">
                <button v-for="p in [{l:'< 500k', v:500000}, {l:'< 1tr', v:1000000}]" :key="p.l" 
                  @click="filters.max_price = p.v; fetchProducts()"
                  class="text-[10px] font-black px-2.5 py-1.5 rounded-lg border-2 border-gray-50 text-gray-500 hover:border-red-200 hover:text-red-600 transition-all">
                  {{ p.l }}
                </button>
              </div>
            </div>
          </div>

          <!-- Sort -->
          <div>
            <h4 class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-4">Sắp xếp theo</h4>
            <div class="relative">
              <select v-model="filters.sap_xep_theo" @change="fetchProducts" class="w-full appearance-none bg-gray-900 text-white rounded-2xl py-3 px-5 text-sm font-bold outline-none cursor-pointer border-r-8 border-transparent">
                <option value="ngay_tao">✨ Mới nhất</option>
                <option value="gia">💰 Giá: Thấp đến Cao</option>
                <option value="gia_desc">💸 Giá: Cao đến Thấp</option>
                <option value="ten">🔠 Tên: A - Z</option>
              </select>
              <svg class="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-width="3"/></svg>
            </div>
          </div>
        </div>
      </aside>

      <!-- Products Grid -->
      <div class="flex-1">
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-xl md:text-2xl font-bold text-gray-900">
            {{ searchQuery ? `Kết quả: "${searchQuery}"` : 'Tất cả sản phẩm' }}
          </h1>
          <span class="text-sm text-gray-400">{{ tong }} sản phẩm</span>
        </div>

        <!-- Skeleton Loading -->
        <div v-if="loading" class="grid grid-cols-2 md:grid-cols-3 gap-6">
          <div v-for="i in 6" :key="i" class="rounded-2xl overflow-hidden bg-white">
            <div class="skeleton h-56 w-full"></div>
            <div class="p-4 space-y-3">
              <div class="skeleton h-3 w-1/3"></div>
              <div class="skeleton h-4 w-3/4"></div>
              <div class="skeleton h-5 w-1/2"></div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="san_phams.length === 0" class="text-center py-20 bg-white rounded-2xl border border-gray-100">
          <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/></svg>
          <p class="text-gray-500 text-lg font-medium">Không tìm thấy sản phẩm nào</p>
          <p class="text-gray-400 text-sm mt-1">Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm</p>
          <button @click="resetFilters" class="mt-4 btn-primary text-sm py-2">Xóa bộ lọc</button>
        </div>

        <!-- Product Grid -->
        <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 stagger-children">
          <div
            v-for="sp in san_phams"
            :key="sp.id"
            class="group bg-white rounded-2xl shadow-sm hover:shadow-2xl hover-lift transition-all duration-500 overflow-hidden border border-gray-100 cursor-pointer"
            @click="$router.push(`/products/${sp.id}`)"
          >
            <!-- Image Container -->
            <div class="relative overflow-hidden aspect-square bg-gray-50">
              <img
                v-if="sp.anh_san_phams?.[0]?.du_lieu_anh"
                :src="sp.anh_san_phams[0].du_lieu_anh"
                :alt="sp.ten"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                loading="lazy"
                @error="handleImgError"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-300 bg-gray-50">
                <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              </div>

              <!-- Badges -->
              <div class="absolute top-3 left-3 flex flex-col gap-1.5">
                <span v-if="sp.gia_khuyen_mai" class="bg-red-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg">
                  -{{ Math.round((1 - sp.gia_khuyen_mai / sp.gia) * 100) }}%
                </span>
                <span v-if="sp.la_noi_bat" class="bg-amber-400 text-amber-900 text-xs font-bold px-3 py-1 rounded-full shadow-lg">HOT</span>
              </div>

              <!-- Quick add to cart -->
              <button
                @click.stop="quickAdd(sp)"
                class="absolute bottom-3 right-3 w-10 h-10 rounded-full bg-white shadow-lg flex items-center justify-center text-gray-700 hover:text-red-600 hover:scale-110 transition-all opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
              </button>
            </div>

            <!-- Product Info -->
            <div class="p-3">
              <p v-if="sp.ten_danh_muc" class="text-xs text-red-600 font-medium mb-1">{{ sp.ten_danh_muc }}</p>
              <h3 class="font-semibold text-gray-900 text-xs line-clamp-2 mb-1.5 group-hover:text-red-600 transition-colors leading-snug">{{ sp.ten }}</h3>

              <!-- Rating -->
              <div class="flex items-center gap-1 mb-1.5" v-if="sp.diem_danh_gia_tb">
                <div class="flex">
                  <span v-for="i in 5" :key="i" class="text-xs" :class="i <= Math.round(sp.diem_danh_gia_tb) ? 'text-amber-400' : 'text-gray-200'">★</span>
                </div>
                <span class="text-xs text-gray-400">({{ sp.so_luong_danh_gia }})</span>
              </div>

              <!-- Price -->
              <div class="flex items-baseline gap-2">
                <span class="text-sm font-bold text-gray-900">{{ formatPrice(sp.gia_khuyen_mai || sp.gia) }}</span>
                <span v-if="sp.gia_khuyen_mai" class="text-xs text-gray-400 line-through">{{ formatPrice(sp.gia) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="tong_so_trang > 1" class="flex items-center justify-center gap-1.5 mt-10">
          <button @click="goPage(trang - 1)" :disabled="trang <= 1" class="w-10 h-10 rounded-xl border border-gray-200 text-sm hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
          </button>
          <button
            v-for="p in visiblePages"
            :key="p"
            @click="goPage(p)"
            :class="['w-10 h-10 rounded-xl text-sm font-medium transition-all', p === trang ? 'bg-red-600 text-white shadow-lg shadow-red-200' : 'border border-gray-200 hover:bg-gray-50']"
          >{{ p }}</button>
          <button @click="goPage(trang + 1)" :disabled="trang >= tong_so_trang" class="w-10 h-10 rounded-xl border border-gray-200 text-sm hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const san_phams = ref([])
const categories = ref([])
const loading = ref(true)
const trang = ref(1)
const tong = ref(0)
const tong_so_trang = ref(1)
const searchQueryInput = ref('')

const filters = reactive({
  id_danh_muc: null,
  min_price: null,
  max_price: null,
  sap_xep_theo: 'ngay_tao',
})

const searchQuery = computed(() => route.query.search || '')

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, trang.value - 2)
  const end = Math.min(tong_so_trang.value, trang.value + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

function formatPrice(p) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p)
}

function handleImgError(e) {
  e.target.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8fafc"/><path d="M160 220l30-30a28.28 28.28 0 0140 0l30 30m-30-30l20-20a28.28 28.28 0 0140 0l20 20m-80-80h.01M100 280h200a28.28 28.28 0 0028.28-28.28v-103.44a28.28 28.28 0 00-28.28-28.28H100a28.28 28.28 0 00-28.28 28.28v103.44A28.28 28.28 0 00100 280z" fill="none" stroke="#cbd5e1" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>')))
}

async function fetchProducts() {
  loading.value = true
  try {
    const params = {
      page: trang.value,
      page_size: 12,
    }

    // Sort mapping
    if (filters.sap_xep_theo === 'gia') {
      params.sort_by = 'gia'
      params.sort_order = 'asc'
    } else if (filters.sap_xep_theo === 'gia_desc') {
      params.sort_by = 'gia'
      params.sort_order = 'desc'
    } else if (filters.sap_xep_theo === 'ten') {
      params.sort_by = 'ten'
      params.sort_order = 'asc'
    } else {
      params.sort_by = 'ngay_tao'
      params.sort_order = 'desc'
    }

    if (searchQuery.value) params.search = searchQuery.value
    if (filters.id_danh_muc) params.id_danh_muc = filters.id_danh_muc
    if (filters.min_price) params.min_price = filters.min_price
    if (filters.max_price) params.max_price = filters.max_price

    const res = await api.get('/products', { params })
    san_phams.value = res.data.items
    tong.value = res.data.tong
    tong_so_trang.value = res.data.tong_so_trang
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

function goPage(p) {
  if (p >= 1 && p <= tong_so_trang.value) { trang.value = p; fetchProducts() }
}

function resetFilters() {
  Object.assign(filters, { id_danh_muc: null, min_price: null, max_price: null, sap_xep_theo: 'ngay_tao' })
  trang.value = 1
  router.push({ name: 'products', query: {} })
  fetchProducts()
}

function applySearch() {
  trang.value = 1
  router.push({ name: 'products', query: searchQuery.value ? { search: searchQuery.value } : {} })
  fetchProducts()
}

async function quickAdd(sp) {
  // Redirect to detail page to force size selection
  router.push(`/products/${sp.id}`)
}

watch(() => route.query.search, (val) => { trang.value = 1; fetchProducts() })

onMounted(async () => {
  try {
    const res = await api.get('/categories/all')
    categories.value = res.data
  } catch {}
  if (route.query.search) {
    // searchQuery will be set via computed
  }
  if (route.query.danh_muc) filters.id_danh_muc = parseInt(route.query.danh_muc)
  fetchProducts()
})
</script>
