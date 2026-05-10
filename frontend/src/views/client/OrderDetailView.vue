<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Back Button -->
    <button @click="$router.back()" class="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-red-600 font-medium transition-colors">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      Quay lại danh sách đơn hàng
    </button>

    <div v-if="loading" class="space-y-4">
      <div class="skeleton h-40 w-full rounded-xl"></div>
      <div class="skeleton h-60 w-full rounded-xl"></div>
    </div>

    <template v-else-if="order">
      <!-- Order Header -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h2 class="text-xl font-bold text-gray-900">{{ order.ma_don_hang }}</h2>
              <span :class="['badge text-xs font-bold', statusClasses[order.trang_thai]]">{{ statusLabels[order.trang_thai] }}</span>
            </div>
            <p class="text-sm text-gray-500">Đặt ngày {{ formatDate(order.ngay_tao) }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">Thành tiền</p>
            <p class="text-2xl font-black text-red-600">{{ formatPrice(order.thanh_tien) }}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left: Order Items & Shipping -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Order Items -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-50">
              <h3 class="font-bold text-gray-900">Sản phẩm đã đặt</h3>
            </div>
            <div class="divide-y divide-gray-50">
              <div v-for="item in order.chi_tiet_don_hangs" :key="item.id" class="px-6 py-4 flex items-center gap-4">
                <div class="w-16 h-16 rounded-xl bg-gray-100 overflow-hidden shrink-0 border border-gray-50">
                  <img v-if="item.anh_san_pham" :src="item.anh_san_pham" class="w-full h-full object-cover" />
                  <div v-else class="w-full h-full flex items-center justify-center text-2xl text-gray-300">👟</div>
                </div>
                <div class="flex-1 min-w-0">
                  <RouterLink :to="`/products/${item.id_san_pham}`" class="font-semibold text-sm text-gray-900 hover:text-red-600 transition-colors line-clamp-1">{{ item.ten_san_pham }}</RouterLink>
                  <p class="text-xs text-gray-500 mt-1">Size: {{ item.kich_thuoc }} · SL: {{ item.so_luong }}</p>
                  <p class="text-xs text-gray-400">{{ formatPrice(item.don_gia) }}/SP</p>
                </div>
                <p class="font-bold text-gray-900 shrink-0">{{ formatPrice(item.thanh_tien) }}</p>
              </div>
            </div>
            <!-- Price Summary -->
            <div class="px-6 py-4 bg-gray-50/50 border-t border-gray-50 space-y-2">
              <div class="flex justify-between text-sm"><span class="text-gray-500">Tạm tính</span><span class="text-gray-900">{{ formatPrice(order.tong_tien) }}</span></div>
              <div v-if="order.tien_giam_gia" class="flex justify-between text-sm"><span class="text-gray-500">Giảm giá</span><span class="text-green-600">-{{ formatPrice(order.tien_giam_gia) }}</span></div>
              <div class="flex justify-between text-sm"><span class="text-gray-500">Phí vận chuyển</span><span class="text-gray-900">{{ order.phi_van_chuyen ? formatPrice(order.phi_van_chuyen) : 'Miễn phí' }}</span></div>
              <div class="flex justify-between text-base font-bold pt-2 border-t border-gray-200"><span>Tổng cộng</span><span class="text-red-600">{{ formatPrice(order.thanh_tien) }}</span></div>
            </div>
          </div>

          <!-- Shipping Info -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <h3 class="font-bold text-gray-900 mb-4">Thông tin giao hàng</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
              <div>
                <p class="text-gray-400 text-xs mb-1">Người nhận</p>
                <p class="font-semibold text-gray-900">{{ order.ten_nguoi_nhan }}</p>
              </div>
              <div>
                <p class="text-gray-400 text-xs mb-1">Số điện thoại</p>
                <p class="font-semibold text-gray-900">{{ order.sdt_nguoi_nhan }}</p>
              </div>
              <div class="sm:col-span-2">
                <p class="text-gray-400 text-xs mb-1">Địa chỉ nhận hàng</p>
                <p class="font-semibold text-gray-900">{{ order.dia_chi_nhan }}</p>
              </div>
              <div>
                <p class="text-gray-400 text-xs mb-1">Phương thức thanh toán</p>
                <p class="font-semibold text-gray-900">{{ paymentMethods[order.phuong_thuc_thanh_toan] || order.phuong_thuc_thanh_toan }}</p>
              </div>
              <div>
                <p class="text-gray-400 text-xs mb-1">Trạng thái thanh toán</p>
                <span :class="['inline-flex text-xs font-bold px-2 py-0.5 rounded-full', order.trang_thai_thanh_toan === 'da_thanh_toan' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700']">
                  {{ order.trang_thai_thanh_toan === 'da_thanh_toan' ? 'Đã thanh toán' : 'Chưa thanh toán' }}
                </span>
              </div>
              <div v-if="order.ghi_chu" class="sm:col-span-2">
                <p class="text-gray-400 text-xs mb-1">Ghi chú</p>
                <p class="font-semibold text-gray-900">{{ order.ghi_chu }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Order History Timeline -->
        <div class="space-y-6">
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <h3 class="font-bold text-gray-900 mb-6">Lịch sử đơn hàng</h3>
            <div v-if="order.lich_su_tac_dong && order.lich_su_tac_dong.length" class="relative">
              <div class="absolute left-4 top-2 bottom-2 w-0.5 bg-gray-100"></div>
              <div v-for="(log, index) in order.lich_su_tac_dong" :key="log.id" class="relative pl-10 pb-8 last:pb-0">
                <div :class="['absolute left-2.5 w-3 h-3 rounded-full border-2 border-white ring-2 mt-1.5', getLogColor(log.hanh_dong)]"></div>
                <div>
                  <p class="text-sm font-semibold text-gray-900">{{ getActionLabel(log.hanh_dong) }}</p>
                  <p class="text-xs text-gray-500 mt-0.5">{{ log.mo_ta }}</p>
                  <p class="text-xs text-gray-400 mt-1">{{ formatDateTime(log.ngay_tao) }}</p>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8">
              <p class="text-sm text-gray-400">Chưa có lịch sử đơn hàng</p>
            </div>
          </div>

          <!-- Cancel Button -->
          <div v-if="order.trang_thai === 'cho_xu_ly'" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <button @click="cancelOrder" class="w-full py-3 border-2 border-red-200 text-red-600 rounded-xl text-sm font-bold hover:bg-red-50 transition-colors flex items-center justify-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              Hủy đơn hàng
            </button>
          </div>
        </div>
      </div>
    </template>

    <div v-else class="text-center py-20 bg-white rounded-2xl border border-gray-100">
      <p class="text-gray-500">Không tìm thấy đơn hàng</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

const { success, error: showError } = useToast()
const route = useRoute()
const router = useRouter()

const order = ref(null)
const loading = ref(true)

const statusLabels = { cho_xu_ly: 'Chờ xử lý', da_xac_nhan: 'Đã xác nhận', dang_giao: 'Đang giao', da_giao: 'Đã giao', da_huy: 'Đã hủy' }
const statusClasses = { cho_xu_ly: 'bg-yellow-100 text-yellow-700', da_xac_nhan: 'bg-blue-100 text-blue-700', dang_giao: 'bg-indigo-100 text-indigo-700', da_giao: 'bg-green-100 text-green-700', da_huy: 'bg-red-100 text-red-700' }
const paymentMethods = { 
  cod: 'Thanh toán khi nhận hàng (COD)', 
  bank_transfer: 'Chuyển khoản ngân hàng', 
  momo: 'Ví MoMo', 
  zalopay: 'Ví ZaloPay',
  tien_mat: 'Tiền mặt', 
  the_tin_dung: 'Thẻ tín dụng' 
}

const actionLabels = {
  ORDER_CREATE: 'Đặt hàng',
  ORDER_STATUS_UPDATE: 'Cập nhật trạng thái',
  ORDER_CANCEL: 'Hủy đơn hàng',
}

function getActionLabel(action) {
  return actionLabels[action] || action
}

function getLogColor(action) {
  const colors = {
    ORDER_CREATE: 'ring-green-500 bg-green-500',
    ORDER_STATUS_UPDATE: 'ring-blue-500 bg-blue-500',
    ORDER_CANCEL: 'ring-red-500 bg-red-500',
  }
  return colors[action] || 'ring-gray-400 bg-gray-400'
}

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }
function formatDate(d) { return new Date(d).toLocaleDateString('vi-VN', { year: 'numeric', month: 'long', day: 'numeric' }) }
function formatDateTime(d) { return new Date(d).toLocaleString('vi-VN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }

async function fetchData() {
  loading.value = true
  try {
    const orderRes = await api.get(`/orders/${route.params.id}`)
    order.value = orderRes.data
  } catch (e) {
    console.error('Error fetching order detail:', e)
  } finally {
    loading.value = false
  }
}

async function cancelOrder() {
  if (!confirm('Bạn có chắc muốn hủy đơn hàng này?')) return
  try {
    await api.put(`/orders/${route.params.id}/cancel`)
    success('Đã hủy đơn hàng')
    fetchData()
  } catch (e) {
    showError(e.response?.data?.detail || 'Lỗi hủy đơn')
  }
}

onMounted(fetchData)
</script>
