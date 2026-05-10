<template>
  <div class="space-y-6 animate-fade-in">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4 flex-1">
        <div class="relative max-w-xs w-full">
          <input v-model="search" @input="fetchProducts" class="input-field pl-10" placeholder="Tìm sản phẩm..." />
          <svg class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
        <select v-model="filterCategory" @change="fetchProducts" class="select-modern max-w-[200px]">
          <option :value="null">Tất cả danh mục</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.ten }}</option>
        </select>
        <button @click="handleExport" class="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 rounded-lg text-sm font-medium hover:bg-green-100 transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          Xuất Excel
        </button>
      </div>
      <RouterLink to="/admin/products/new" class="btn-primary shadow-lg shadow-primary-500/20 transition-all hover:scale-105 active:scale-95">+ Thêm sản phẩm</RouterLink>
    </div>

    <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-6 py-4 font-semibold text-gray-600">Sản phẩm</th>
            <th class="text-left px-4 py-4 font-semibold text-gray-600">Danh mục</th>
            <th class="text-left px-4 py-4 font-semibold text-gray-600">Kích thước</th>
            <th class="text-right px-4 py-4 font-semibold text-gray-600">Giá</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Tồn kho</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Trạng thái</th>
            <th class="text-right px-6 py-4 font-semibold text-gray-600">Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id" class="border-b border-gray-50 hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-lg bg-gray-100 overflow-hidden shrink-0">
                  <img v-if="p.anh_san_phams?.[0]?.du_lieu_anh" :src="p.anh_san_phams[0].du_lieu_anh" class="w-full h-full object-cover" />
                </div>
                <div>
                  <p class="font-semibold text-gray-900 line-clamp-1">{{ p.ten }}</p>
                  <p class="text-xs text-gray-500">SKU: {{ p.ma_sku || 'N/A' }}</p>
                </div>
              </div>
            </td>
            <td class="px-4 py-4 text-gray-600">{{ p.ten_danh_muc || '—' }}</td>
            <td class="px-4 py-4 text-gray-500 text-xs">{{ p.cac_kich_thuoc || '—' }}</td>
            <td class="px-4 py-4 text-right font-semibold">
              <span v-if="p.gia_khuyen_mai" class="text-red-500">{{ formatPrice(p.gia_khuyen_mai) }}</span>
              <span :class="p.gia_khuyen_mai ? 'text-gray-400 line-through text-xs ml-1' : 'text-gray-900'">{{ formatPrice(p.gia) }}</span>
            </td>
            <td class="px-4 py-4 text-center">
              <span :class="p.so_luong_ton > 0 ? 'text-green-600' : 'text-red-600 font-bold'">{{ p.so_luong_ton }}</span>
            </td>
            <td class="px-4 py-4 text-center">
              <span :class="['badge', p.dang_hoat_dong ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500']">{{ p.dang_hoat_dong ? 'Đang bán' : 'Ẩn' }}</span>
            </td>
            <td class="px-6 py-4 text-right">
              <div class="flex items-center justify-end gap-2">
                <RouterLink :to="`/admin/products/${p.id}/edit`" class="p-2 text-blue-500 hover:bg-blue-50 rounded-lg transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                </RouterLink>
                <button @click="deleteProduct(p.id, p.name)" class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="products.length === 0" class="text-center py-12 text-gray-500">Chưa có sản phẩm nào</div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-center gap-2">
      <button v-for="p in totalPages" :key="p" @click="page = p; fetchProducts()"
        :class="['px-3 py-1.5 rounded-lg text-sm', p === page ? 'bg-primary-500 text-white' : 'border border-gray-200 hover:bg-gray-50']"
      >{{ p }}</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'
import { exportToExcel } from '@/utils/excel'

const { success, error: showError } = useToast()
const products = ref([])
const categories = ref([])
const search = ref('')
const filterCategory = ref(null)
const page = ref(1)
const totalPages = ref(1)

function handleExport() {
  const data = products.value.map(p => ({
    'ID': p.id,
    'Tên sản phẩm': p.ten,
    'SKU': p.ma_sku || '',
    'Danh mục': p.ten_danh_muc || '',
    'Giá gốc': p.gia,
    'Giá khuyến mãi': p.gia_khuyen_mai || '',
    'Tồn kho': p.so_luong_ton,
    'Kích thước': p.cac_kich_thuoc || '',
    'Trạng thái': p.dang_hoat_dong ? 'Đang bán' : 'Ẩn',
    'Ngày tạo': new Date(p.ngay_tao).toLocaleDateString('vi-VN')
  }))
  exportToExcel(data, 'Danh_sach_san_pham', 'San_pham')
}

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }

async function fetchProducts() {
  try {
    const params = { page: page.value, page_size: 20 }
    if (search.value) params.search = search.value
    if (filterCategory.value) params.id_danh_muc = filterCategory.value
    const res = await api.get('/products/admin', { params })
    products.value = res.data.items
    totalPages.value = res.data.total_pages
  } catch {}
}

async function deleteProduct(id, name) {
  if (!confirm(`Xóa sản phẩm "${name}"?`)) return
  try { await api.delete(`/products/${id}`); success('Đã xóa'); fetchProducts() }
  catch (e) { showError(e.response?.data?.detail || 'Lỗi') }
}

onMounted(async () => {
  try { const res = await api.get('/categories/all'); categories.value = res.data } catch {}
  fetchProducts()
})
</script>
