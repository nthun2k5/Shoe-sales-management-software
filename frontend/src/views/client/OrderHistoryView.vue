<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Compact Single-Row Filter -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4">
      <div class="flex flex-wrap items-center gap-3">
        <!-- Search Order ID -->
        <div class="relative flex-1 min-w-[200px] group">
          <input
            v-model="orderIdSearch"
            @input="fetchOrders"
            type="text"
            placeholder="Mã đơn hàng..."
            class="w-full bg-gray-50 border border-gray-100 focus:border-red-500/30 focus:bg-white rounded-xl py-2.5 pl-9 pr-3 text-sm font-medium transition-all outline-none"
          />
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 group-focus-within:text-red-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>

        <!-- Status Combobox -->
        <div class="relative min-w-[180px]">
          <select v-model="statusFilter" @change="fetchOrders" 
            class="w-full appearance-none bg-gray-50 border border-gray-100 focus:border-red-500/30 focus:bg-white rounded-xl py-2.5 pl-4 pr-10 text-sm font-bold text-gray-700 outline-none cursor-pointer transition-all">
            <option value="">Trạng thái: Tất cả</option>
            <option v-for="(label, key) in statusLabels" :key="key" :value="key">{{ label }}</option>
          </select>
          <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-width="3"/></svg>
        </div>

        <!-- Date Range (Compact Premium) -->
        <div class="flex items-center gap-3 bg-white border border-gray-100 rounded-xl px-4 py-2 shadow-xs group focus-within:border-red-200 transition-all">
          <div class="flex items-center gap-2">
            <span class="text-[10px] font-black text-gray-400 uppercase tracking-wider">Từ</span>
            <input type="date" v-model="fromDate" @change="fetchOrders" class="bg-transparent text-xs font-black text-gray-700 outline-none w-28 cursor-pointer" />
          </div>
          <div class="w-px h-4 bg-gray-100"></div>
          <div class="flex items-center gap-2">
            <span class="text-[10px] font-black text-gray-400 uppercase tracking-wider">Đến</span>
            <input type="date" v-model="toDate" @change="fetchOrders" class="bg-transparent text-xs font-black text-gray-700 outline-none w-28 cursor-pointer" />
          </div>
        </div>

        <!-- Reset Button -->
        <button @click="resetFilters" class="p-2.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all" title="Làm mới bộ lọc">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        </button>
      </div>
    </div>

    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="skeleton h-40 w-full rounded-xl"></div>
    </div>

    <div v-else-if="orders.length === 0" class="text-center py-20 bg-white rounded-2xl border border-gray-100 shadow-sm">
      <div class="w-20 h-20 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-4">
        <svg class="w-10 h-10 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
      </div>
      <h3 class="text-lg font-bold text-gray-900 mb-1">Chưa có đơn hàng nào</h3>
      <p class="text-gray-500 text-sm mb-6">Hãy bắt đầu mua sắm ngay!</p>
      <RouterLink to="/products" class="btn-primary px-8 py-3 text-sm">Khám phá sản phẩm</RouterLink>
    </div>

    <div v-else class="space-y-4">
      <div v-for="order in orders" :key="order.id" @click="$router.push(`/account/orders/${order.id}`)"
        class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-red-100 transition-all cursor-pointer group">
        <!-- Order Header -->
        <div class="flex items-center justify-between px-6 py-4 bg-gray-50/50 border-b border-gray-100">
          <div class="flex items-center gap-4">
            <span class="font-mono font-bold text-red-600 text-sm group-hover:text-red-700 transition-colors">{{ order.ma_don_hang }}</span>
            <span class="text-xs text-gray-400">{{ new Date(order.ngay_tao).toLocaleDateString('vi-VN', { year: 'numeric', month: 'long', day: 'numeric' }) }}</span>
          </div>
          <div class="flex items-center gap-3">
            <span :class="['badge text-xs font-bold', statusClasses[order.trang_thai]]">{{ statusLabels[order.trang_thai] }}</span>
            <svg class="w-4 h-4 text-gray-300 group-hover:text-red-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </div>
        </div>

        <!-- Order Items -->
        <div class="divide-y divide-gray-50">
          <div v-for="item in order.chi_tiet_don_hangs" :key="item.id" class="px-6 py-4 flex items-center gap-4" @click.stop>
            <div class="w-16 h-16 rounded-xl bg-gray-100 overflow-hidden shrink-0 border border-gray-50">
              <img v-if="item.anh_san_pham" :src="item.anh_san_pham" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center text-2xl text-gray-300">👟</div>
            </div>
            <div class="flex-1 min-w-0">
              <RouterLink :to="`/products/${item.id_san_pham}`" class="font-semibold text-gray-900 text-sm hover:text-red-600 transition-colors line-clamp-1">{{ item.ten_san_pham }}</RouterLink>
              <p class="text-xs text-gray-500 mt-1">Size: {{ item.kich_thuoc }} · x{{ item.so_luong }} · {{ formatPrice(item.don_gia) }}/SP</p>
            </div>
            <div class="text-right shrink-0">
              <p class="font-bold text-gray-900">{{ formatPrice(item.thanh_tien) }}</p>
              <button v-if="order.trang_thai === 'da_giao'" @click.stop="openReviewModal(item, order)"
                class="text-xs text-red-600 hover:underline font-medium mt-1">
                ⭐ Đánh giá
              </button>
            </div>
          </div>
        </div>

        <!-- Order Footer -->
        <div class="px-6 py-4 bg-gray-50/30 border-t border-gray-100 flex items-center justify-between">
          <div class="flex items-center gap-3" @click.stop>
            <button v-if="order.trang_thai === 'cho_xu_ly'" @click="cancelOrder(order.id)"
              class="text-xs text-red-500 hover:text-red-700 font-medium flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              Hủy đơn
            </button>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">Tổng cộng</p>
            <p class="text-xl font-black text-red-600">{{ formatPrice(order.thanh_tien) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Review Modal: Minimalist Luxury -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showReviewModal" class="fixed inset-0 z-100 flex items-center justify-center p-4">
          <!-- Deep Backdrop -->
          <div class="absolute inset-0 bg-black/40 backdrop-blur-xl transition-opacity" @click="showReviewModal = false"></div>
          
          <!-- Modal Panel -->
          <div class="relative bg-white rounded-[2.5rem] w-full max-w-lg shadow-2xl border border-white/20 overflow-hidden transform transition-all">
            <!-- Header -->
            <div class="px-8 pt-10 pb-6">
              <h3 class="text-2xl font-light text-gray-900 tracking-tight">Đánh giá <span class="font-black text-red-600">sản phẩm</span></h3>
              <p class="text-sm text-gray-500 font-medium mt-1 line-clamp-1">{{ reviewingItem?.ten_san_pham }}</p>
            </div>

            <div class="px-8 pb-10 space-y-10">
              <!-- Star Rating Premium -->
              <div class="space-y-4">
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Chất lượng sản phẩm</label>
                <div class="flex items-center gap-3">
                  <button v-for="i in 5" :key="i" @click="reviewForm.diem_danh_gia = i"
                    :class="['text-4xl transition-all duration-300 transform', i <= reviewForm.diem_danh_gia ? 'text-amber-400 scale-110 drop-shadow-sm' : 'text-gray-100 hover:scale-105']">
                    ★
                  </button>
                  <span class="ml-4 px-3 py-1 bg-gray-50 text-gray-400 text-[10px] font-black uppercase tracking-widest rounded-lg transition-all" :class="{'bg-red-50 text-red-600': reviewForm.diem_danh_gia > 0}">
                    {{ ['', 'Rất tệ', 'Tệ', 'Bình thường', 'Tốt', 'Xuất sắc'][reviewForm.diem_danh_gia] }}
                  </span>
                </div>
              </div>

              <!-- Comment Underline Style -->
              <div class="group border-b border-gray-100 focus-within:border-red-500 transition-colors py-1">
                <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-3">Chia sẻ trải nghiệm</label>
                <textarea v-model="reviewForm.binh_luan" rows="3" class="w-full bg-transparent text-gray-900 font-medium outline-none text-base resize-none"
                  placeholder="Sản phẩm rất đẹp, đi êm chân..."></textarea>
              </div>

              <div class="flex gap-4 pt-4">
                <button @click="showReviewModal = false" class="flex-1 py-4 text-xs font-black uppercase tracking-widest text-gray-400 hover:text-gray-900 transition-all">Hủy bỏ</button>
                <button @click="submitReview" :disabled="reviewLoading"
                  class="flex-1 py-4 bg-gray-900 text-white rounded-full text-xs font-black uppercase tracking-widest hover:bg-black transition-all shadow-xl shadow-black/20 disabled:opacity-50">
                  {{ reviewLoading ? 'Đang gửi...' : 'Gửi đánh giá' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

const { success, error: showError } = useToast()
const orders = ref([])
const loading = ref(true)
const statusFilter = ref('')
const fromDate = ref('')
const toDate = ref('')
const orderIdSearch = ref('')

const statusLabels = { 
  cho_xu_ly: 'Chờ xử lý', 
  da_xac_nhan: 'Đã xác nhận', 
  dang_giao: 'Đang giao', 
  da_giao: 'Đã giao', 
  da_huy: 'Đã hủy' 
}
const statusClasses = { cho_xu_ly: 'bg-yellow-100 text-yellow-700', da_xac_nhan: 'bg-blue-100 text-blue-700', dang_giao: 'bg-indigo-100 text-indigo-700', da_giao: 'bg-green-100 text-green-700', da_huy: 'bg-red-100 text-red-700' }

// Review
const showReviewModal = ref(false)
const reviewingItem = ref(null)
const reviewLoading = ref(false)
const reviewForm = reactive({ diem_danh_gia: 5, binh_luan: '' })

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }

async function fetchOrders() {
  loading.value = true
  try {
    const res = await api.get('/orders/my')
    let items = res.data.items || []
    
    // Order ID Search
    if (orderIdSearch.value) {
      const search = orderIdSearch.value.toLowerCase()
      items = items.filter(o => o.ma_don_hang.toLowerCase().includes(search))
    }

    // Status Filter
    if (statusFilter.value) items = items.filter(o => o.trang_thai === statusFilter.value)
    
    // Date Filters
    if (fromDate.value) {
      const start = new Date(fromDate.value)
      start.setHours(0, 0, 0, 0)
      items = items.filter(o => new Date(o.ngay_tao) >= start)
    }
    if (toDate.value) {
      const end = new Date(toDate.value)
      end.setHours(23, 59, 59, 999)
      items = items.filter(o => new Date(o.ngay_tao) <= end)
    }
    
    orders.value = items
  } catch {} finally { loading.value = false }
}

function resetFilters() {
  statusFilter.value = ''
  fromDate.value = ''
  toDate.value = ''
  orderIdSearch.value = ''
  fetchOrders()
}

async function cancelOrder(id) {
  const ghi_chu = prompt('Vui lòng nhập lý do hủy đơn hàng (không bắt buộc):')
  if (ghi_chu === null) return // User cancelled prompt
  
  try { 
    await api.put(`/orders/${id}/cancel`, { ghi_chu: ghi_chu.trim() || 'Hủy mua từ khách hàng' }); 
    success('Đã hủy đơn hàng'); 
    fetchOrders() 
  }
  catch (e) { showError(e.response?.data?.detail || 'Lỗi hủy đơn') }
}

function openReviewModal(item, order) {
  reviewingItem.value = item
  reviewForm.diem_danh_gia = 5
  reviewForm.binh_luan = ''
  showReviewModal.value = true
}

async function submitReview() {
  reviewLoading.value = true
  try {
    await api.post('/reviews', { id_san_pham: reviewingItem.value.id_san_pham, diem_danh_gia: reviewForm.diem_danh_gia, binh_luan: reviewForm.binh_luan })
    success('Cảm ơn bạn đã đánh giá!')
    showReviewModal.value = false
  } catch (e) {
    showError(e.response?.data?.detail || 'Lỗi gửi đánh giá')
  } finally { reviewLoading.value = false }
}

onMounted(fetchOrders)
</script>
