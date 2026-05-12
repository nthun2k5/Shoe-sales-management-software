<template>
  <div class="space-y-6">
    <!-- Welcome Banner -->
    <div class="relative bg-linear-to-r from-red-600 via-red-500 to-orange-500 rounded-2xl p-6 lg:p-8 text-white overflow-hidden">
      <div class="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/4"></div>
      <div class="absolute bottom-0 left-1/4 w-32 h-32 bg-white/5 rounded-full translate-y-1/2"></div>
      <div class="relative z-10">
        <p class="text-red-100 text-sm font-medium">Xin chào,</p>
        <h2 class="text-2xl lg:text-3xl font-black mt-1">{{ authStore.user?.ho_ten || 'Khách hàng' }}</h2>
        <p class="text-red-100 text-sm mt-2">Chào mừng bạn quay trở lại với GIÀYĐẸP</p>
      </div>
      <div class="relative z-10 mt-6 flex flex-wrap gap-3">
        <RouterLink to="/products" class="inline-flex items-center gap-2 bg-white text-red-600 px-5 py-2.5 rounded-xl text-sm font-bold hover:bg-red-50 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
          Mua sắm ngay
        </RouterLink>
        <RouterLink to="/account/orders" class="inline-flex items-center gap-2 bg-white/20 text-white px-5 py-2.5 rounded-xl text-sm font-bold hover:bg-white/30 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
          Xem đơn hàng
        </RouterLink>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="stat in stats" :key="stat.label" class="bg-white rounded-xl p-5 border border-gray-100 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all duration-300">
        <div class="flex items-center gap-3 mb-3">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center shadow-lg', stat.bg]">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path :d="stat.icon" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
        </div>
        <p class="text-2xl font-black text-gray-900">{{ stat.value }}</p>
        <p class="text-xs text-gray-500 mt-1">{{ stat.label }}</p>
      </div>
    </div>

    <!-- Address Section -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </div>
          <div>
            <h3 class="font-bold text-gray-900">Địa chỉ nhận hàng</h3>
            <p class="text-xs text-gray-500 mt-0.5">Quản lý địa chỉ giao hàng của bạn</p>
          </div>
        </div>
        <button @click="openAddAddress" class="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-xl text-sm font-bold hover:bg-black transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
          Thêm địa chỉ
        </button>
      </div>

      <!-- Loading -->
      <div v-if="addressLoading" class="p-6 space-y-4">
        <div v-for="i in 2" :key="i" class="animate-pulse flex items-center gap-4 p-4 border border-gray-100 rounded-xl">
          <div class="w-12 h-12 bg-gray-100 rounded-xl"></div>
          <div class="flex-1 space-y-2">
            <div class="h-4 bg-gray-100 rounded w-1/3"></div>
            <div class="h-3 bg-gray-50 rounded w-2/3"></div>
          </div>
        </div>
      </div>

      <!-- Address List -->
      <div v-else-if="addresses.length > 0" class="p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="addr in addresses" :key="addr.id"
          class="relative border-2 rounded-2xl p-5 transition-all duration-300 hover:shadow-md"
          :class="addr.la_mac_dinh ? 'border-red-200 bg-red-50/30' : 'border-gray-100 bg-white hover:border-red-100'">
          <!-- Default Badge -->
          <div v-if="addr.la_mac_dinh" class="absolute top-4 right-4 px-3 py-1 bg-red-600 text-white text-[10px] font-bold rounded-full">
            MẶC ĐỊNH
          </div>
          <!-- Address Info -->
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center shrink-0"
              :class="addr.la_mac_dinh ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-400'">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <h4 class="font-bold text-gray-900 text-sm">{{ addr.ten_nguoi_nhan }}</h4>
              </div>
              <p class="text-xs text-gray-500 mb-1">{{ addr.so_dien_thoai }}</p>
              <p class="text-sm text-gray-700 leading-relaxed">{{ addr.dia_chi }}</p>
            </div>
          </div>
          <!-- Actions -->
          <div class="flex items-center gap-2 mt-4 pt-4 border-t border-gray-100">
            <button @click="openEditAddress(addr)" class="flex-1 bg-gray-50 text-gray-700 py-2 rounded-xl text-xs font-bold hover:bg-gray-100 transition-all">
              Chỉnh sửa
            </button>
            <button v-if="!addr.la_mac_dinh" @click="setDefault(addr.id)" class="flex-1 bg-red-50 text-red-600 py-2 rounded-xl text-xs font-bold hover:bg-red-100 transition-all">
              Đặt mặc định
            </button>
            <button @click="deleteAddress(addr.id)" class="w-10 h-9 rounded-xl bg-red-50 text-red-500 flex items-center justify-center hover:bg-red-100 transition-all">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="p-12 text-center">
        <div class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
          <svg class="w-10 h-10 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        </div>
        <p class="text-gray-500 font-medium mb-1">Chưa có địa chỉ nào</p>
        <p class="text-gray-400 text-sm mb-4">Thêm địa chỉ để dễ dàng đặt hàng hơn</p>
        <button @click="openAddAddress" class="inline-flex items-center gap-2 px-6 py-3 bg-gray-900 text-white rounded-xl text-sm font-bold hover:bg-black transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
          Thêm địa chỉ đầu tiên
        </button>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Recent Orders -->
      <div class="lg:col-span-2 bg-white rounded-xl border border-gray-100 shadow-xs overflow-hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-50">
          <h3 class="font-bold text-gray-900">Đơn hàng gần đây</h3>
          <RouterLink to="/account/orders" class="text-sm text-red-600 hover:underline font-medium">Xem tất cả →</RouterLink>
        </div>
        <div v-if="dashboard.don_hang_gan_day?.length" class="divide-y divide-gray-50">
          <div v-for="o in dashboard.don_hang_gan_day" :key="o.id" @click="$router.push(`/account/orders/${o.id}`)"
            class="px-6 py-4 hover:bg-gray-50/50 transition-all cursor-pointer group">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-red-50 flex items-center justify-center group-hover:bg-red-100 transition-colors">
                  <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
                </div>
                <div>
                  <p class="font-mono text-sm font-semibold text-red-600 group-hover:text-red-700 transition-colors">{{ o.ma_don_hang }}</p>
                  <p class="text-xs text-gray-400">{{ new Date(o.ngay_tao).toLocaleDateString('vi-VN') }}</p>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <div class="text-right">
                  <p class="font-bold text-sm">{{ formatPrice(o.thanh_tien) }}</p>
                  <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold mt-1', statusClasses[o.trang_thai]]">{{ statusLabels[o.trang_thai] }}</span>
                </div>
                <svg class="w-4 h-4 text-gray-300 group-hover:text-red-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="px-6 py-12 text-center">
          <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-3">
            <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
          </div>
          <p class="text-gray-500 text-sm">Chưa có đơn hàng nào</p>
          <RouterLink to="/products" class="inline-block mt-3 text-sm font-bold text-red-600 hover:underline">Mua sắm ngay →</RouterLink>
        </div>
      </div>

      <!-- Right Sidebar -->
      <div class="space-y-6">
        <!-- Total Spent -->
        <div class="bg-linear-to-br from-red-600 via-red-500 to-red-600 rounded-xl p-6 text-white relative overflow-hidden">
          <div class="absolute -top-6 -right-6 w-24 h-24 bg-white/10 rounded-full"></div>
          <div class="absolute -bottom-4 -left-4 w-16 h-16 bg-white/5 rounded-full"></div>
          <p class="text-sm text-red-100 font-medium">Tổng chi tiêu</p>
          <p class="text-3xl font-black mt-2 relative z-10">{{ formatPrice(dashboard.tong_chi_tieu || 0) }}</p>
          <p class="text-xs text-red-200 mt-2">Từ {{ dashboard.tong_don_hang || 0 }} đơn hàng</p>
        </div>

        <!-- Order Status -->
        <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-xs">
          <h4 class="font-bold text-gray-900 mb-4 text-sm">Trạng thái đơn hàng</h4>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-yellow-400"></span> Chờ xử lý</span>
              <span class="text-sm font-bold text-yellow-600">{{ dashboard.don_cho_xu_ly || 0 }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-400"></span> Đã xác nhận</span>
              <span class="text-sm font-bold text-blue-600">{{ dashboard.don_da_xac_nhan || 0 }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-indigo-400"></span> Đang giao</span>
              <span class="text-sm font-bold text-indigo-600">{{ dashboard.don_dang_giao || 0 }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-green-400"></span> Đã giao</span>
              <span class="text-sm font-bold text-green-600">{{ dashboard.don_da_giao || 0 }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-pink-400"></span> Yêu thích</span>
              <span class="text-sm font-bold text-pink-600">{{ dashboard.so_yeu_thich || 0 }}</span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-xs">
          <h4 class="font-bold text-gray-900 mb-4 text-sm">Thao tác nhanh</h4>
          <div class="grid grid-cols-2 gap-3">
            <RouterLink v-for="action in quickActions" :key="action.path" :to="action.path"
              class="flex flex-col items-center gap-2 p-3 rounded-xl hover:bg-gray-50 transition-all group">
              <div :class="['w-10 h-10 rounded-xl flex items-center justify-center transition-transform group-hover:scale-110', action.bg]">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path :d="action.icon" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </div>
              <span class="text-xs font-bold text-gray-700">{{ action.label }}</span>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Address Drawer -->
    <div v-if="drawerOpen" class="fixed inset-0 z-50 overflow-hidden">
      <div class="absolute inset-0 bg-black/30" @click="closeDrawer"></div>
      <div class="absolute top-0 right-0 h-full w-full max-w-lg bg-white shadow-xl transform transition-transform duration-300 translate-x-0 flex flex-col">
        <!-- Drawer Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-100">
          <h3 class="text-lg font-bold text-gray-900">{{ isEditing ? 'Chỉnh sửa địa chỉ' : 'Thêm địa chỉ mới' }}</h3>
          <button @click="closeDrawer" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>

        <!-- Drawer Body -->
        <div class="flex-1 overflow-y-auto p-6 space-y-4">
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1">Tên người nhận</label>
            <input v-model="addressForm.ten_nguoi_nhan" class="input-field" placeholder="Nguyễn Văn A" />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1">Số điện thoại</label>
            <input v-model="addressForm.so_dien_thoai" class="input-field" placeholder="0912345678" />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1">Địa chỉ chi tiết</label>
            <textarea v-model="addressForm.dia_chi" rows="3" class="input-field" placeholder="Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành phố"></textarea>
          </div>
          <label class="flex items-center gap-2 text-sm cursor-pointer">
            <input v-model="addressForm.la_mac_dinh" type="checkbox" class="rounded text-red-600" />
            <span>Đặt làm địa chỉ mặc định</span>
          </label>
        </div>

        <!-- Drawer Footer -->
        <div class="p-6 border-t border-gray-100 flex gap-3">
          <button @click="closeDrawer" class="flex-1 px-4 py-2.5 bg-gray-100 text-gray-700 rounded-xl text-sm font-bold hover:bg-gray-200 transition-all">
            Hủy
          </button>
          <button @click="saveAddress" :disabled="saving" class="flex-1 px-4 py-2.5 bg-gray-900 text-white rounded-xl text-sm font-bold hover:bg-black transition-all disabled:opacity-50">
            {{ saving ? 'Đang lưu...' : 'Lưu địa chỉ' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

const authStore = useAuthStore()
const { success, error: showError } = useToast()
const dashboard = ref({})
const addresses = ref([])
const addressLoading = ref(true)
const drawerOpen = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const editingId = ref(null)

const addressForm = ref({
  ten_nguoi_nhan: '',
  so_dien_thoai: '',
  dia_chi: '',
  la_mac_dinh: false
})

const statusLabels = {
  cho_xu_ly: 'Chờ xử lý',
  da_xac_nhan: 'Đã xác nhận',
  dang_giao: 'Đang giao',
  da_giao: 'Đã giao',
  da_huy: 'Đã hủy'
}
const statusClasses = {
  cho_xu_ly: 'bg-yellow-100 text-yellow-700',
  da_xac_nhan: 'bg-blue-100 text-blue-700',
  dang_giao: 'bg-indigo-100 text-indigo-700',
  da_giao: 'bg-green-100 text-green-700',
  da_huy: 'bg-red-100 text-red-700'
}

function formatPrice(p) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p)
}

function resetForm() {
  addressForm.value = {
    ten_nguoi_nhan: '',
    so_dien_thoai: '',
    dia_chi: '',
    la_mac_dinh: false
  }
}

function openAddAddress() {
  resetForm()
  isEditing.value = false
  editingId.value = null
  drawerOpen.value = true
}

function openEditAddress(addr) {
  isEditing.value = true
  editingId.value = addr.id
  addressForm.value = {
    ten_nguoi_nhan: addr.ten_nguoi_nhan,
    so_dien_thoai: addr.so_dien_thoai,
    dia_chi: addr.dia_chi,
    la_mac_dinh: addr.la_mac_dinh
  }
  drawerOpen.value = true
}

function closeDrawer() {
  drawerOpen.value = false
  editingId.value = null
  resetForm()
}

async function fetchAddresses() {
  try {
    const res = await api.get('/addresses')
    addresses.value = res.data
  } catch (e) {
    console.error('Address fetch error:', e)
  }
}

async function saveAddress() {
  saving.value = true
  try {
    if (isEditing.value) {
      await api.put(`/addresses/${editingId.value}`, addressForm.value)
      success('Đã cập nhật địa chỉ')
    } else {
      await api.post('/addresses', addressForm.value)
      success('Đã thêm địa chỉ mới')
    }
    closeDrawer()
    await fetchAddresses()
  } catch (e) {
    showError(e.response?.data?.detail || 'Lưu thất bại')
  } finally {
    saving.value = false
  }
}

async function deleteAddress(id) {
  if (!confirm('Bạn chắc chắn muốn xóa địa chỉ này?')) return
  try {
    await api.delete(`/addresses/${id}`)
    success('Đã xóa địa chỉ')
    await fetchAddresses()
  } catch (e) {
    showError('Xóa thất bại')
  }
}

async function setDefault(id) {
  try {
    await api.post(`/addresses/${id}/set-default`)
    success('Đã đặt làm mặc định')
    await fetchAddresses()
  } catch (e) {
    showError('Thao tác thất bại')
  }
}

const stats = computed(() => [
  { label: 'Tổng đơn hàng', value: dashboard.value.tong_don_hang || 0, icon: 'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z', bg: 'bg-linear-to-r from-red-500 to-red-600 shadow-red-500/25' },
  { label: 'Chờ xử lý', value: dashboard.value.don_cho_xu_ly || 0, icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 01 18 0z', bg: 'bg-linear-to-r from-yellow-400 to-yellow-500 shadow-yellow-500/25' },
  { label: 'Đã giao', value: dashboard.value.don_da_giao || 0, icon: 'M5 13l4 4L19 7', bg: 'bg-linear-to-r from-green-500 to-green-600 shadow-green-500/25' },
  { label: 'Yêu thích', value: dashboard.value.so_yeu_thich || 0, icon: 'M4.318 6.318a4.5 4.5 0 00 0 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z', bg: 'bg-linear-to-r from-pink-500 to-pink-600 shadow-pink-500/25' },
])

const quickActions = [
  { path: '/products', label: 'Mua sắm', icon: 'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z', bg: 'bg-linear-to-r from-red-500 to-red-600' },
  { path: '/cart', label: 'Giỏ hàng', icon: 'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z', bg: 'bg-linear-to-r from-yellow-400 to-yellow-500' },
  { path: '/account/wishlist', label: 'Yêu thích', icon: 'M4.318 6.318a4.5 4.5 0 00 0 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z', bg: 'bg-linear-to-r from-pink-500 to-pink-600' },
  { path: '/account/profile', label: 'Hồ sơ', icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z', bg: 'bg-linear-to-r from-blue-500 to-blue-600' },
]

onMounted(async () => {
  try {
    const [dashRes, addrRes] = await Promise.all([
      api.get('/dashboard/client'),
      api.get('/addresses')
    ])
    dashboard.value = dashRes.data
    addresses.value = addrRes.data
  } catch (e) {
    console.error('Dashboard error:', e)
  } finally {
    addressLoading.value = false
  }
})
</script>
