<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-gray-900">Quản lý mã giảm giá</h2>
      <button @click="openForm()" class="btn-primary w-10 h-10 rounded-xl flex items-center justify-center" title="Thêm mã giảm giá">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
      </button>
    </div>

    <!-- Coupons Table -->
    <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-6 py-4 font-semibold text-gray-600">Mã</th>
            <th class="text-left px-4 py-4 font-semibold text-gray-600">Loại</th>
            <th class="text-right px-4 py-4 font-semibold text-gray-600">Giá trị</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Đơn tối thiểu</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Đã dùng</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Thời gian</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Trạng thái</th>
            <th class="text-right px-6 py-4 font-semibold text-gray-600">Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in coupons" :key="c.id" class="border-b border-gray-50 hover:bg-gray-50/50">
            <td class="px-6 py-4">
              <span class="font-mono font-bold text-red-600">{{ c.ma }}</span>
            </td>
            <td class="px-4 py-4">
              <span :class="['badge', c.loai_giam_gia === 'phan_tram' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700']">
                {{ c.loai_giam_gia === 'phan_tram' ? 'Phần trăm' : 'Cố định' }}
              </span>
            </td>
            <td class="px-4 py-4 text-right font-semibold">
              {{ c.loai_giam_gia === 'phan_tram' ? c.gia_tri_giam + '%' : formatPrice(c.gia_tri_giam) }}
            </td>
            <td class="px-4 py-4 text-center text-gray-600">{{ c.gia_tri_don_toi_thieu > 0 ? formatPrice(c.gia_tri_don_toi_thieu) : '—' }}</td>
            <td class="px-4 py-4 text-center">
              <span class="text-sm">{{ c.so_lan_da_su_dung }} / <span class="text-gray-400">{{ c.so_lan_su_dung_toi_da || '∞' }}</span></span>
            </td>
            <td class="px-4 py-4 text-center">
              <div v-if="c.ngay_bat_dau || c.ngay_ket_thuc" class="text-xs text-gray-500">
                <div v-if="c.ngay_bat_dau">{{ formatDate(c.ngay_bat_dau) }}</div>
                <div v-if="c.ngay_ket_thuc">{{ formatDate(c.ngay_ket_thuc) }}</div>
              </div>
              <span v-else class="text-xs text-gray-400">Vô hạn</span>
            </td>
            <td class="px-4 py-4 text-center">
              <button @click="toggleActive(c)" :class="['badge cursor-pointer hover:opacity-80 transition-opacity', c.dang_hoat_dong ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500']">
                {{ c.dang_hoat_dong ? 'Hoạt động' : 'Tắt' }}
              </button>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end gap-1">
                <button @click="openForm(c)" class="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors flex items-center justify-center" title="Sửa">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.586a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                </button>
                <button @click="deleteCoupon(c.id)" class="w-8 h-8 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 transition-colors flex items-center justify-center" title="Xóa">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <Teleport to="body">
      <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showForm = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg z-10 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-1">{{ editingId ? 'Sửa mã giảm giá' : 'Thêm mã giảm giá mới' }}</h3>
          <p class="text-sm text-gray-500 mb-6">{{ editingId ? 'Cập nhật thông tin mã giảm giá' : 'Nhập thông tin mã giảm giá mới' }}</p>

          <form @submit.prevent="saveCoupon" class="space-y-4">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Mã giảm giá *</label>
              <input v-model="formData.ma" type="text" required class="input-field" placeholder="SALE20" :disabled="!!editingId" />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Loại giảm giá</label>
                <select v-model="formData.loai_giam_gia" class="select-modern">
                  <option value="phan_tram">Phần trăm (%)</option>
                  <option value="co_dinh">Số tiền cố định (₫)</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Giá trị *</label>
                <input v-model="formattedGiaTri" type="text" required class="input-field" :placeholder="formData.loai_giam_gia === 'phan_tram' ? '10' : '50.000'" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Đơn tối thiểu (₫)</label>
                <input v-model="formattedToiThieu" type="text" class="input-field" placeholder="0" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Lượt dùng tối đa (0 = ∞)</label>
                <input v-model="formattedLuotDung" type="text" class="input-field" placeholder="0" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Ngày bắt đầu</label>
                <input v-model="formData.ngay_bat_dau" type="datetime-local" class="input-field" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Ngày kết thúc</label>
                <input v-model="formData.ngay_ket_thuc" type="datetime-local" class="input-field" />
              </div>
            </div>

            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" v-model="formData.dang_hoat_dong" class="w-4 h-4 rounded border-gray-300 text-red-600 focus:ring-red-500" />
              <span class="text-sm">Kích hoạt</span>
            </label>

            <div class="flex gap-3 pt-4">
              <button type="button" @click="showForm = false" class="flex-1 py-3 border border-gray-200 rounded-xl text-sm font-medium hover:bg-gray-50 transition-colors">Hủy</button>
              <button type="submit" :disabled="formLoading" class="flex-1 py-3 bg-red-600 text-white rounded-xl text-sm font-bold hover:bg-red-700 transition-colors disabled:opacity-50">
                {{ formLoading ? 'Đang lưu...' : (editingId ? 'Cập nhật' : 'Tạo mới') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

const { success, error: showError } = useToast()
const coupons = ref([])
const showForm = ref(false)
const editingId = ref(null)
const formLoading = ref(false)

const formData = reactive({
  ma: '',
  loai_giam_gia: 'phan_tram',
  gia_tri_giam: 10,
  gia_tri_don_toi_thieu: 0,
  so_lan_su_dung_toi_da: 0,
  ngay_bat_dau: '',
  ngay_ket_thuc: '',
  dang_hoat_dong: true,
})

const formattedGiaTri = computed({
  get: () => formData.gia_tri_giam !== null && formData.gia_tri_giam !== undefined ? new Intl.NumberFormat('vi-VN').format(formData.gia_tri_giam) : '',
  set: (val) => { formData.gia_tri_giam = Number(val.toString().replace(/[^\d]/g, '')) || 0 }
})

const formattedToiThieu = computed({
  get: () => formData.gia_tri_don_toi_thieu ? new Intl.NumberFormat('vi-VN').format(formData.gia_tri_don_toi_thieu) : '0',
  set: (val) => { formData.gia_tri_don_toi_thieu = Number(val.toString().replace(/[^\d]/g, '')) || 0 }
})

const formattedLuotDung = computed({
  get: () => formData.so_lan_su_dung_toi_da ? new Intl.NumberFormat('vi-VN').format(formData.so_lan_su_dung_toi_da) : '0',
  set: (val) => { formData.so_lan_su_dung_toi_da = Number(val.toString().replace(/[^\d]/g, '')) || 0 }
})

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }
function formatDate(d) { return new Date(d).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' }) }

async function fetchCoupons() {
  try { const res = await api.get('/coupons'); coupons.value = res.data } catch {}
}

function openForm(coupon = null) {
  if (coupon) {
    editingId.value = coupon.id
    Object.assign(formData, {
      ma: coupon.ma,
      loai_giam_gia: coupon.loai_giam_gia,
      gia_tri_giam: coupon.gia_tri_giam,
      gia_tri_don_toi_thieu: coupon.gia_tri_don_toi_thieu,
      so_lan_su_dung_toi_da: coupon.so_lan_su_dung_toi_da,
      ngay_bat_dau: coupon.ngay_bat_dau ? coupon.ngay_bat_dau.slice(0, 16) : '',
      ngay_ket_thuc: coupon.ngay_ket_thuc ? coupon.ngay_ket_thuc.slice(0, 16) : '',
      dang_hoat_dong: coupon.dang_hoat_dong,
    })
  } else {
    editingId.value = null
    Object.assign(formData, {
      ma: '', loai_giam_gia: 'phan_tram', gia_tri_giam: 10,
      gia_tri_don_toi_thieu: 0, so_lan_su_dung_toi_da: 0,
      ngay_bat_dau: '', ngay_ket_thuc: '', dang_hoat_dong: true,
    })
  }
  showForm.value = true
}

async function saveCoupon() {
  formLoading.value = true
  try {
    const data = { ...formData }
    if (!data.ngay_bat_dau) delete data.ngay_bat_dau
    if (!data.ngay_ket_thuc) delete data.ngay_ket_thuc
    if (editingId.value) {
      await api.put(`/coupons/${editingId.value}`, data)
      success('Đã cập nhật mã giảm giá')
    } else {
      await api.post('/coupons', data)
      success('Đã tạo mã giảm giá mới')
    }
    showForm.value = false
    fetchCoupons()
  } catch (e) {
    showError(e.response?.data?.detail || 'Có lỗi xảy ra')
  } finally {
    formLoading.value = false
  }
}

async function deleteCoupon(id) {
  if (!confirm('Bạn có chắc muốn xóa mã này?')) return
  try {
    await api.delete(`/coupons/${id}`)
    success('Đã xóa mã giảm giá')
    fetchCoupons()
  } catch (e) {
    showError(e.response?.data?.detail || 'Có lỗi xảy ra')
  }
}

async function toggleActive(coupon) {
  try {
    await api.put(`/coupons/${coupon.id}`, { dang_hoat_dong: !coupon.dang_hoat_dong })
    success('Đã cập nhật trạng thái')
    fetchCoupons()
  } catch (e) {
    showError(e.response?.data?.detail || 'Có lỗi xảy ra')
  }
}

onMounted(fetchCoupons)
</script>
