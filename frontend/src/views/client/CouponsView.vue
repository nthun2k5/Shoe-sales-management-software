<template>
  <div class="space-y-6 animate-fade-in">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xl font-bold text-gray-900">Mã giảm giá</h2>
        <p class="text-sm text-gray-500 mt-1">Sao chép mã để sử dụng khi thanh toán</p>
      </div>
      <button @click="fetchCoupons" class="w-10 h-10 rounded-xl border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition-colors" title="Làm mới">
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.953 8.953 0 004.278 9m10.034-5a8.954 8.954 0 00-2.036-1.37m-4.965 9.197A8.972 8.972 0 0012 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8a8.947 8.947 0 01-2.357.563M12 21v-8.517M15.657 5.343l-1.414 1.414"/></svg>
      </button>
    </div>

    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="skeleton h-32 w-full rounded-xl"></div>
    </div>

    <div v-else-if="availableCoupons.length === 0" class="text-center py-20 bg-white rounded-2xl border border-gray-100 shadow-sm">
      <div class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
        <svg class="w-10 h-10 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/></svg>
      </div>
      <h3 class="text-lg font-bold text-gray-900 mb-1">Chưa có mã giảm giá</h3>
      <p class="text-gray-500 text-sm">Hãy quay lại sau để nhận mã mới</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="c in availableCoupons" :key="c.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden group hover:shadow-md hover:border-red-100 transition-all">
        <!-- Coupon Header -->
        <div class="relative bg-linear-to-r from-red-500 to-red-600 p-5 text-white">
          <div class="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -translate-y-8 translate-x-8"></div>
          <div class="absolute bottom-0 left-0 w-16 h-16 bg-white/5 rounded-full translate-y-6 -translate-x-4"></div>
          <div class="relative z-10">
            <p class="text-xs text-red-100 font-medium">GIẢM GIÁ</p>
            <p class="text-2xl font-black mt-1">
              {{ c.loai_giam_gia === 'phan_tram' ? c.gia_tri_giam + '%' : formatPrice(c.gia_tri_giam) }}
            </p>
            <p class="text-xs text-red-200 mt-1 font-mono font-bold">{{ c.ma }}</p>
          </div>
        </div>
        <!-- Coupon Body -->
        <div class="p-5 space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-500">Đơn tối thiểu</span>
            <span class="font-semibold text-gray-900">{{ c.gia_tri_don_toi_thieu > 0 ? formatPrice(c.gia_tri_don_toi_thieu) : 'Không yêu cầu' }}</span>
          </div>
          <div v-if="c.ngay_ket_thuc" class="flex items-center justify-between text-xs">
            <span class="text-gray-500">Hết hạn</span>
            <span class="font-semibold text-gray-900">{{ formatDate(c.ngay_ket_thuc) }}</span>
          </div>
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-500">Còn lại</span>
            <span class="font-semibold text-gray-900">{{ c.so_lan_su_dung_toi_da > 0 ? (c.so_lan_su_dung_toi_da - c.so_lan_da_su_dung) + ' lượt' : 'Vô hạn' }}</span>
          </div>
          <button @click="copyCode(c.ma)" class="w-full mt-2 py-2.5 bg-red-50 text-red-600 rounded-xl text-sm font-bold hover:bg-red-100 transition-colors flex items-center justify-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-2M8 5a2 2 0 100-4 0 2 2 0 000 4zm0 0c.552 0 1.076.17 1.502.474L12 8.414l2.498-2.94A3.978 3.978 0 0116 5c.78 0 1.514.26 2.121.879L20 8l-2 2H8.414L6.586 8z"/></svg>
            {{ copiedCode === c.ma ? 'Đã sao chép!' : 'Sao chép mã' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Used Coupons Section -->
    <div v-if="usedCoupons.length > 0" class="mt-8">
      <h3 class="text-lg font-bold text-gray-900 mb-4">Mã đã sử dụng</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="c in usedCoupons" :key="c.id"
          class="bg-gray-50 rounded-2xl border border-gray-100 overflow-hidden opacity-60">
          <div class="bg-gray-200 p-5">
            <p class="text-xs text-gray-500 font-medium">ĐÃ SỬ DỤNG</p>
            <p class="text-2xl font-black text-gray-400 mt-1">
              {{ c.loai_giam_gia === 'phan_tram' ? c.gia_tri_giam + '%' : formatPrice(c.gia_tri_giam) }}
            </p>
            <p class="text-xs text-gray-400 mt-1 font-mono font-bold">{{ c.ma }}</p>
          </div>
          <div class="p-5 space-y-3">
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-400">Đơn tối thiểu</span>
              <span class="text-gray-400">{{ c.gia_tri_don_toi_thieu > 0 ? formatPrice(c.gia_tri_don_toi_thieu) : 'Không yêu cầu' }}</span>
            </div>
            <div class="text-center text-xs text-gray-400 py-2">Bạn đã sử dụng mã này</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

const { success } = useToast()
const availableCoupons = ref([])
const usedCoupons = ref([])
const loading = ref(true)
const copiedCode = ref(null)

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }
function formatDate(d) { return new Date(d).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' }) }

async function fetchCoupons() {
  loading.value = true
  try {
    const res = await api.get('/coupons/available')
    availableCoupons.value = res.data.filter(c => !c._used)
    usedCoupons.value = res.data.filter(c => c._used)
  } catch {}
  finally { loading.value = false }
}

async function copyCode(code) {
  try {
    await navigator.clipboard.writeText(code)
    copiedCode.value = code
    success('Đã sao chép mã: ' + code)
    setTimeout(() => { copiedCode.value = null }, 2000)
  } catch {
    // Fallback for older browsers
    const input = document.createElement('input')
    input.value = code
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
    copiedCode.value = code
    success('Đã sao chép mã: ' + code)
    setTimeout(() => { copiedCode.value = null }, 2000)
  }
}

onMounted(fetchCoupons)
</script>
