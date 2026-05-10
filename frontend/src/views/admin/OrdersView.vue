<template>
  <div class="space-y-6 animate-fade-in">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4 flex-1">
        <div class="relative max-w-xs w-full">
          <input v-model="search" @input="fetchOrders" class="input-field pl-10" placeholder="Tìm mã đơn hàng..." />
          <svg class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
        <select v-model="statusFilter" @change="fetchOrders" class="select-modern max-w-[200px]">
          <option :value="null">Tất cả trạng thái</option>
          <option v-for="(label, key) in statusLabels" :key="key" :value="key">{{ label }}</option>
        </select>
        <button @click="handleExport" class="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 rounded-lg text-sm font-medium hover:bg-green-100 transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          Xuất Excel
        </button>
      </div>
      <div class="flex items-center gap-2 text-xs text-gray-400 bg-white px-4 py-2 rounded-lg border border-gray-100">
        <span class="w-2 h-2 rounded-full bg-green-500"></span>
        Hệ thống trực tuyến
      </div>
    </div>

    <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-6 py-4 font-semibold text-gray-600">Mã đơn</th>
            <th class="text-left px-4 py-4 font-semibold text-gray-600">Khách hàng</th>
            <th class="text-right px-4 py-4 font-semibold text-gray-600">Tổng tiền</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Thanh toán</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Trạng thái</th>
            <th class="text-left px-4 py-4 font-semibold text-gray-600">Ngày đặt</th>
            <th class="text-right px-6 py-4 font-semibold text-gray-600">Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="o in orders" :key="o.id" class="border-b border-gray-50 hover:bg-gray-50 transition-colors cursor-pointer" @click="viewDetail(o)">
            <td class="px-6 py-4 font-mono font-semibold text-red-600 underline">{{ o.ma_don_hang }}</td>
            <td class="px-4 py-4">{{ o.ten_nguoi_dung || o.ten_nguoi_nhan || '—' }}</td>
            <td class="px-4 py-4 text-right font-semibold text-gray-900">{{ formatPrice(o.thanh_tien) }}</td>
            <td class="px-4 py-4 text-center">
              <span :class="['px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider', 
                o.trang_thai_thanh_toan === 'da_thanh_toan' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700']">
                {{ o.trang_thai_thanh_toan === 'da_thanh_toan' ? 'Đã TT' : 'Chưa TT' }}
              </span>
            </td>
            <td class="px-4 py-4 text-center">
              <span :class="['px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider', statusColors[o.trang_thai]]">
                {{ statusLabels[o.trang_thai] }}
              </span>
            </td>
            <td class="px-4 py-4 text-gray-500 text-xs">{{ formatDate(o.ngay_tao) }}</td>
            <td class="px-6 py-4 text-right" @click.stop>
              <select @change="updateStatus(o.id, $event.target.value)" :value="o.trang_thai" class="select-modern text-xs py-1 px-2 w-auto bg-gray-50 border-gray-200">
                <option v-for="(label, key) in statusLabels" :key="key" :value="key">{{ label }}</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Detail Modal -->
    <Teleport to="body">
      <div v-if="selectedOrder" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" @click.self="selectedOrder = null">
        <div class="bg-white rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl animate-scale-up overflow-hidden">
          <div class="px-6 py-4 border-b flex items-center justify-between bg-gray-50/50">
            <div>
              <h2 class="text-xl font-black text-gray-900">Chi tiết đơn hàng</h2>
              <p class="text-xs text-gray-500 font-mono mt-0.5">ID: #{{ selectedOrder.ma_don_hang }}</p>
            </div>
            <div class="flex items-center gap-3">
              <button @click="handlePrint" class="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-xl text-sm font-bold hover:bg-black transition-all shadow-lg shadow-gray-200">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
                In hóa đơn
              </button>
              <button @click="selectedOrder = null" class="p-2 text-gray-400 hover:text-red-600 transition-colors"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-width="2.5"/></svg></button>
            </div>
          </div>
          
          <div class="flex-1 overflow-y-auto p-6 custom-scrollbar" id="printable-invoice">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <!-- Customer Info -->
              <div class="space-y-6">
                <div>
                  <h3 class="text-sm font-black uppercase tracking-wider text-gray-400 mb-4">Thông tin giao hàng</h3>
                  <div class="bg-gray-50 rounded-xl p-4 space-y-3 border border-gray-100">
                    <div class="flex justify-between text-sm"><span class="text-gray-500">Người nhận:</span> <span class="font-bold text-gray-900">{{ selectedOrder.ten_nguoi_nhan }}</span></div>
                    <div class="flex justify-between text-sm"><span class="text-gray-500">Số điện thoại:</span> <span class="font-bold text-gray-900">{{ selectedOrder.sdt_nguoi_nhan }}</span></div>
                    <div class="flex justify-between text-sm"><span class="text-gray-500">Địa chỉ:</span> <span class="font-bold text-gray-900 text-right">{{ selectedOrder.dia_chi_nhan }}</span></div>
                    <div class="flex justify-between text-sm pt-2 border-t border-gray-200"><span class="text-gray-500">Thanh toán:</span> <span class="font-bold text-red-600 uppercase">{{ paymentMethodLabels[selectedOrder.phuong_thuc_thanh_toan] || selectedOrder.phuong_thuc_thanh_toan }}</span></div>
                  </div>
                </div>

                <div>
                  <h3 class="text-sm font-black uppercase tracking-wider text-gray-400 mb-4">Lịch sử tác động</h3>
                  <div class="space-y-3">
                    <div v-if="selectedOrder.lich_su_tac_dong && selectedOrder.lich_su_tac_dong.length === 0" class="text-center py-6 text-gray-400 bg-gray-50 rounded-xl border border-dashed italic text-sm">Chưa có lịch sử tác động</div>
                    <div v-for="log in selectedOrder.lich_su_tac_dong" :key="log.id" class="flex gap-3 relative pb-4 last:pb-0">
                      <div class="absolute left-2 top-6 bottom-0 w-0.5 bg-gray-100 last:hidden"></div>
                      <div class="w-4 h-4 rounded-full bg-red-100 border-2 border-red-500 shrink-0 mt-1 z-10"></div>
                      <div>
                        <p class="text-sm text-gray-800 font-medium">{{ log.mo_ta }} <span v-if="log.nguoi_dung" class="text-xs text-gray-500 italic">({{ log.nguoi_dung }})</span></p>
                        <p class="text-[10px] text-gray-400 mt-1">{{ formatDateFull(log.ngay_tao) }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Order Items -->
              <div>
                <h3 class="text-sm font-black uppercase tracking-wider text-gray-400 mb-4">Sản phẩm đã đặt</h3>
                <div class="space-y-4">
                  <div v-for="item in selectedOrder.chi_tiet_don_hangs" :key="item.id" class="flex gap-4 p-3 bg-white border border-gray-100 rounded-xl hover:shadow-sm transition-shadow">
                    <div class="w-16 h-16 bg-gray-50 rounded-lg overflow-hidden shrink-0 border border-gray-100">
                      <img v-if="item.anh_san_pham" :src="item.anh_san_pham" class="w-full h-full object-cover" />
                      <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <h4 class="text-sm font-bold text-gray-900 truncate">{{ item.ten_san_pham }}</h4>
                      <p class="text-xs text-gray-500 mt-0.5">Số lượng: {{ item.so_luong }} × {{ formatPrice(item.don_gia) }}</p>
                      <p class="text-sm font-black text-red-600 mt-1">{{ formatPrice(item.thanh_tien) }}</p>
                    </div>
                  </div>
                </div>

                <div class="mt-8 bg-gray-900 text-white p-6 rounded-2xl shadow-xl shadow-gray-200">
                  <div class="flex justify-between text-gray-400 text-sm mb-2"><span>Tạm tính:</span> <span>{{ formatPrice(selectedOrder.tong_tien) }}</span></div>
                  <div class="flex justify-between text-gray-400 text-sm mb-2"><span>Giảm giá:</span> <span>-{{ formatPrice(selectedOrder.tien_giam_gia) }}</span></div>
                  <div class="flex justify-between text-gray-400 text-sm mb-4 pb-4 border-b border-white/10"><span>Vận chuyển:</span> <span>+{{ formatPrice(selectedOrder.phi_van_chuyen) }}</span></div>
                  <div class="flex justify-between items-end">
                    <span class="text-sm font-bold uppercase tracking-widest text-gray-400">Tổng cộng:</span>
                    <span class="text-2xl font-black text-white">{{ formatPrice(selectedOrder.thanh_tien) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'
import { exportToExcel } from '@/utils/excel'

const { success, error: showError } = useToast()
const orders = ref([])
const search = ref('')
const statusFilter = ref(null)
const selectedOrder = ref(null)

function handleExport() {
  const data = orders.value.map(o => ({
    'Mã đơn hàng': o.ma_don_hang,
    'Khách hàng': o.ten_nguoi_dung || o.ten_nguoi_nhan || 'N/A',
    'Số điện thoại': o.sdt_nguoi_nhan,
    'Tổng tiền': o.tong_tien,
    'Giảm giá': o.tien_giam_gia,
    'Phí ship': o.phi_van_chuyen,
    'Thanh tiền': o.thanh_tien,
    'PT Thanh toán': paymentMethodLabels[o.phuong_thuc_thanh_toan] || o.phuong_thuc_thanh_toan,
    'TT Thanh toán': o.trang_thai_thanh_toan === 'da_thanh_toan' ? 'Đã TT' : 'Chưa TT',
    'Trạng thái': statusLabels[o.trang_thai],
    'Ngày đặt': new Date(o.ngay_tao).toLocaleDateString('vi-VN')
  }))
  exportToExcel(data, 'Danh_sach_don_hang', 'Don_hang')
}

function handlePrint() {
  const content = document.getElementById('printable-invoice').innerHTML
  const printWindow = window.open('', '', 'height=600,width=800')
  printWindow.document.write('<html><head><title>Hóa đơn ' + selectedOrder.value.ma_don_hang + '</title>')
  printWindow.document.write('<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">')
  printWindow.document.write('</head><body class="p-10">')
  printWindow.document.write('<div class="max-w-2xl mx-auto border p-8">')
  printWindow.document.write('<div class="flex justify-between mb-8 border-b pb-4"><div><h1 class="text-2xl font-bold">GIÀY ĐẸP STORE</h1><p>Địa chỉ: 123 Đường ABC, Hà Nội</p><p>SĐT: 0123 456 789</p></div><div class="text-right"><h2 class="text-xl font-bold text-red-600">HÓA ĐƠN BÁN HÀNG</h2><p>Mã: ' + selectedOrder.value.ma_don_hang + '</p><p>Ngày: ' + new Date(selectedOrder.value.ngay_tao).toLocaleDateString("vi-VN") + '</p></div></div>')
  printWindow.document.write(content)
  printWindow.document.write('<div class="mt-10 pt-10 border-t flex justify-between px-10"><div><p class="font-bold mb-10">Người mua hàng</p><p>(Ký tên)</p></div><div class="text-center"><p class="font-bold mb-10">Người bán hàng</p><p>(Ký tên)</p></div></div>')
  printWindow.document.write('</div>')
  printWindow.document.write('</body></html>')
  printWindow.document.close()
  setTimeout(() => {
    printWindow.print()
  }, 500)
}

const statusLabels = { 
  cho_xu_ly: 'Chờ xử lý', 
  da_xac_nhan: 'Đã xác nhận', 
  dang_giao: 'Đang giao', 
  da_giao: 'Đã giao', 
  da_huy: 'Đã hủy' 
}

const statusColors = {
  cho_xu_ly: 'bg-blue-100 text-blue-700',
  da_xac_nhan: 'bg-indigo-100 text-indigo-700',
  dang_giao: 'bg-amber-100 text-amber-700',
  da_giao: 'bg-green-100 text-green-700',
  da_huy: 'bg-red-100 text-red-700'
}

const paymentMethodLabels = {
  cod: 'COD',
  bank_transfer: 'Chuyển khoản',
  momo: 'MoMo',
  zalopay: 'ZaloPay',
  tien_mat: 'Tiền mặt'
}

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }
function formatDate(d) { return new Date(d).toLocaleDateString('vi-VN') }
function formatDateFull(d) { return new Intl.DateTimeFormat('vi-VN', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(d)) }

async function fetchOrders() {
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (statusFilter.value) params.trang_thai = statusFilter.value
    const res = await api.get('/orders', { params })
    orders.value = res.data.items
  } catch (e) { console.error(e) }
}

async function viewDetail(order) {
  try {
    const res = await api.get(`/orders/${order.id}`)
    selectedOrder.value = res.data
  } catch (e) {
    console.error('Failed to fetch order detail', e)
  }
}

async function updateStatus(id, trang_thai) {
  try {
    await api.put(`/orders/${id}/status`, { trang_thai })
    success('Đã cập nhật trạng thái')
    fetchOrders()
    if (selectedOrder.value && selectedOrder.value.id === id) {
      viewDetail({ id })
    }
  } catch (e) {
    showError(e.response?.data?.detail || 'Lỗi cập nhật')
  }
}

onMounted(fetchOrders)
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f9fafb; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #d1d5db; }

@keyframes scale-up {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-scale-up { animation: scale-up 0.3s ease-out forwards; }
</style>

