<template>
  <div class="space-y-6 animate-fade-in">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-900">Quản lý tồn kho</h2>
      <div class="flex items-center gap-3">
        <select v-model="stockFilter" @change="fetchProducts" class="select-modern w-auto text-sm py-2">
          <option value="all">Tất cả</option>
          <option value="low">Sắp hết (≤10)</option>
          <option value="out">Hết hàng (0)</option>
        </select>
        <input v-model="search" @input="fetchProducts" class="input-field max-w-xs text-sm py-2" placeholder="Tìm sản phẩm..." />
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-3 gap-4">
      <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <p class="text-xs text-gray-500 mb-1">Tổng sản phẩm</p>
        <p class="text-2xl font-bold text-gray-900">{{ summary.total }}</p>
      </div>
      <div class="bg-white rounded-xl p-5 border border-yellow-100 shadow-sm">
        <p class="text-xs text-yellow-600 mb-1">Sắp hết hàng</p>
        <p class="text-2xl font-bold text-yellow-600">{{ summary.low }}</p>
      </div>
      <div class="bg-white rounded-xl p-5 border border-red-100 shadow-sm">
        <p class="text-xs text-red-600 mb-1">Hết hàng</p>
        <p class="text-2xl font-bold text-red-600">{{ summary.out }}</p>
      </div>
    </div>

    <!-- Products Table -->
    <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-6 py-4 font-semibold text-gray-600">Sản phẩm</th>
            <th class="text-left px-4 py-4 font-semibold text-gray-600">SKU</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Tồn kho</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Trạng thái</th>
            <th class="text-right px-6 py-4 font-semibold text-gray-600">Giá</th>
            <th class="text-right px-6 py-4 font-semibold text-gray-600">Cập nhật</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id" class="border-b border-gray-50 hover:bg-gray-50">
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-gray-100 overflow-hidden shrink-0">
                  <img v-if="p.anh_san_phams?.[0]?.du_lieu_anh" :src="p.anh_san_phams[0].du_lieu_anh" class="w-full h-full object-cover" />
                </div>
                <span class="font-medium text-gray-900 line-clamp-1">{{ p.ten }}</span>
              </div>
            </td>
            <td class="px-4 py-4 text-gray-500 font-mono text-xs">{{ p.ma_sku || '—' }}</td>
            <td class="px-4 py-4 text-center">
              <div class="flex items-center justify-center gap-2">
                <input type="number" :value="p.so_luong_ton" @change="updateStock(p.id, $event.target.value)" class="w-20 text-center input-field text-sm py-1" min="0" />
              </div>
            </td>
            <td class="px-4 py-4 text-center">
              <span v-if="p.so_luong_ton === 0" class="badge bg-red-100 text-red-700">Hết hàng</span>
              <span v-else-if="p.so_luong_ton <= 10" class="badge bg-yellow-100 text-yellow-700">Sắp hết</span>
              <span v-else class="badge bg-green-100 text-green-700">Còn hàng</span>
            </td>
            <td class="px-6 py-4 text-right font-semibold">{{ formatPrice(p.gia_khuyen_mai || p.gia) }}</td>
            <td class="px-6 py-4 text-right">
              <RouterLink :to="`/admin/products/${p.id}/edit`" class="text-red-600 hover:underline text-xs font-medium">Sửa</RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="products.length === 0" class="text-center py-8 text-gray-400 text-sm">Không có sản phẩm</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

const { success, error: showError } = useToast()
const products = ref([])
const search = ref('')
const stockFilter = ref('all')
const summary = reactive({ total: 0, low: 0, out: 0 })

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }

async function fetchProducts() {
  try {
    const params = { page_size: 100 }
    if (search.value) params.search = search.value
    const res = await api.get('/products/admin', { params })
    let items = res.data.items || []
    summary.total = items.length
    summary.low = items.filter(p => p.so_luong_ton > 0 && p.so_luong_ton <= 10).length
    summary.out = items.filter(p => p.so_luong_ton <= 0).length
    if (stockFilter.value === 'low') items = items.filter(p => p.so_luong_ton > 0 && p.so_luong_ton <= 10)
    else if (stockFilter.value === 'out') items = items.filter(p => p.so_luong_ton <= 0)
    products.value = items
  } catch {}
}

async function updateStock(id, val) {
  try {
    await api.put(`/products/${id}`, { so_luong_ton: parseInt(val) })
    success('Đã cập nhật tồn kho')
  } catch (e) { showError('Lỗi cập nhật') }
}

onMounted(fetchProducts)
</script>
