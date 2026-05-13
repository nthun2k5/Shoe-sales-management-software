<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Period Selector -->
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-900">Báo cáo & Thống kê</h2>
      <select v-model="period" @change="fetchData" class="select-modern w-auto text-sm py-2">
        <option value="7">7 ngày qua</option>
        <option value="30">30 ngày qua</option>
        <option value="90">3 tháng qua</option>
      </select>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="kpi in kpis" :key="kpi.label" class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center', kpi.bg]">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path :d="kpi.icon" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <span :class="['text-xs font-bold px-2 py-1 rounded-full', kpi.trend > 0 ? 'text-green-700 bg-green-50' : 'text-red-700 bg-red-50']">
            {{ kpi.trend > 0 ? '+' : '' }}{{ kpi.trend }}%
          </span>
        </div>
        <p class="text-2xl font-black text-gray-900">{{ kpi.value }}</p>
        <p class="text-xs text-gray-500 mt-1">{{ kpi.label }}</p>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
        <h3 class="font-bold text-gray-900 mb-4">Biểu đồ doanh thu</h3>
        <div class="h-72"><canvas ref="revenueRef"></canvas></div>
      </div>
      <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
        <h3 class="font-bold text-gray-900 mb-4">Phân bố trạng thái</h3>
        <div class="h-72"><canvas ref="statusRef"></canvas></div>
      </div>
    </div>

    <!-- Tables Row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Top Products -->
      <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
        <h3 class="font-bold text-gray-900 mb-4">🏆 Top sản phẩm bán chạy</h3>
        <div class="space-y-3">
          <div v-for="(p, i) in data.top_san_phams" :key="p.id" class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
            <span :class="['w-7 h-7 rounded-lg flex items-center justify-center text-white text-xs font-bold', i === 0 ? 'bg-yellow-500' : i === 1 ? 'bg-gray-400' : i === 2 ? 'bg-amber-700' : 'bg-gray-300']">{{ i + 1 }}</span>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-900 line-clamp-1">{{ p.ten }}</p>
              <p class="text-xs text-gray-400">{{ formatPrice(p.gia) }}</p>
            </div>
            <span class="text-sm font-bold text-red-600">{{ p.tong_da_ban }} bán</span>
          </div>
          <p v-if="!data.top_san_phams?.length" class="text-sm text-gray-400 text-center py-4">Chưa có dữ liệu</p>
        </div>
      </div>

      <!-- Category Revenue -->
      <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
        <h3 class="font-bold text-gray-900 mb-4">📊 Tổng quan nhanh</h3>
        <div class="space-y-4">
          <div class="p-4 rounded-xl bg-linear-to-r from-indigo-500 to-purple-600 text-white">
            <p class="text-xs opacity-80">Tổng doanh thu</p>
            <p class="text-2xl font-black mt-1">{{ formatPrice(data.tong_doanh_thu || 0) }}</p>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div class="p-3 rounded-lg bg-green-50 border border-green-100">
              <p class="text-xs text-green-600 font-medium">Doanh thu tháng này</p>
              <p class="text-lg font-bold text-green-700">{{ formatPrice(data.doanh_thu_thang || 0) }}</p>
            </div>
            <div class="p-3 rounded-lg bg-blue-50 border border-blue-100">
              <p class="text-xs text-blue-600 font-medium">Đơn tháng này</p>
              <p class="text-lg font-bold text-blue-700">{{ data.don_thang_nay || 0 }}</p>
            </div>
            <div class="p-3 rounded-lg bg-yellow-50 border border-yellow-100">
              <p class="text-xs text-yellow-600 font-medium">Tồn kho cần nhập</p>
              <p class="text-lg font-bold text-yellow-700">{{ data.het_hang || 0 }} SP</p>
            </div>
            <div class="p-3 rounded-lg bg-red-50 border border-red-100">
              <p class="text-xs text-red-600 font-medium">Đơn chờ xử lý</p>
              <p class="text-lg font-bold text-red-700">{{ data.don_cho_xu_ly || 0 }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Orders -->
    <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-bold text-gray-900">Đơn hàng mới nhất</h3>
        <RouterLink to="/admin/orders" class="text-sm text-red-600 font-medium hover:underline">Xem tất cả →</RouterLink>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead><tr class="border-b border-gray-100">
            <th class="text-left py-3 px-2 text-gray-500 font-medium">Mã đơn</th>
            <th class="text-left py-3 px-2 text-gray-500 font-medium">Khách hàng</th>
            <th class="text-right py-3 px-2 text-gray-500 font-medium">Tổng tiền</th>
            <th class="text-center py-3 px-2 text-gray-500 font-medium">Trạng thái</th>
            <th class="text-right py-3 px-2 text-gray-500 font-medium">Ngày</th>
          </tr></thead>
          <tbody>
            <tr v-for="o in data.don_hang_gan_day" :key="o.id" class="border-b border-gray-50 hover:bg-gray-50/50">
              <td class="py-3 px-2 font-mono font-semibold text-red-600">{{ o.ma_don_hang }}</td>
              <td class="py-3 px-2">{{ o.ho_ten }}</td>
              <td class="py-3 px-2 text-right font-semibold">{{ formatPrice(o.thanh_tien) }}</td>
              <td class="py-3 px-2 text-center"><span :class="['badge text-xs', `badge-${o.trang_thai}`]">{{ statusLabels[o.trang_thai] }}</span></td>
              <td class="py-3 px-2 text-right text-gray-400 text-xs">{{ new Date(o.ngay_tao).toLocaleDateString('vi-VN') }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="!data.don_hang_gan_day?.length" class="text-center py-8 text-gray-400 text-sm">Chưa có đơn hàng</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import api from '@/services/api'

Chart.register(...registerables)

const data = ref({})
const period = ref('7')
const revenueRef = ref(null)
const statusRef = ref(null)
const statusLabels = { 
  cho_xu_ly: 'Chờ xử lý', 
  da_xac_nhan: 'Đã xác nhận', 
  dang_giao: 'Đang giao', 
  da_giao: 'Đã giao', 
  da_huy: 'Đã hủy' 
}
let revenueChart = null
let statusChart = null

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }

const kpis = computed(() => [
  { label: 'Doanh thu tháng', value: formatPrice(data.value.doanh_thu_thang || 0), icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z', bg: 'bg-indigo-500', trend: 12 },
  { label: 'Đơn chờ xử lý', value: data.value.don_cho_xu_ly || 0, icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z', bg: 'bg-yellow-500', trend: -(data.value.don_cho_xu_ly || 0) },
  { label: 'Tổng sản phẩm', value: data.value.tong_san_pham || 0, icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4', bg: 'bg-green-500', trend: 5 },
  { label: 'Khách hàng', value: data.value.tong_nguoi_dung || 0, icon: 'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2', bg: 'bg-blue-500', trend: 8 },
])

async function fetchData() {
  try {
    const res = await api.get('/dashboard/admin')
    data.value = res.data
    await nextTick()
    renderCharts()
  } catch (e) { console.error(e) }
}

function renderCharts() {
  if (revenueChart) revenueChart.destroy()
  if (statusChart) statusChart.destroy()

  if (revenueRef.value && data.value.bieu_do_doanh_thu) {
    revenueChart = new Chart(revenueRef.value, {
      type: 'bar',
      data: {
        labels: data.value.bieu_do_doanh_thu.map(d => { const date = new Date(d.date); return date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' }) }),
        datasets: [{
          label: 'Doanh thu', data: data.value.bieu_do_doanh_thu.map(d => d.doanh_thu),
          backgroundColor: 'rgba(99,102,241,0.8)', borderRadius: 8, barThickness: 28,
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { callback: v => new Intl.NumberFormat('vi-VN', { notation: 'compact' }).format(v) } } } }
    })
  }

  if (statusRef.value && data.value.phan_bo_trang_thai) {
    const os = data.value.phan_bo_trang_thai
    statusChart = new Chart(statusRef.value, {
      type: 'doughnut',
      data: {
        labels: Object.keys(os).map(k => statusLabels[k] || k),
        datasets: [{ data: Object.values(os), backgroundColor: ['#f59e0b', '#3b82f6', '#6366f1', '#22c55e', '#ef4444'], borderWidth: 3, borderColor: '#fff' }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: '65%', plugins: { legend: { position: 'bottom', labels: { padding: 12, usePointStyle: true } } } }
    })
  }
}

onMounted(fetchData)
</script>
