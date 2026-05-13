<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="stat in stats" :key="stat.label" class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">{{ stat.label }}</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">{{ stat.value }}</p>
          </div>
          <div :class="['w-12 h-12 rounded-xl flex items-center justify-center text-white text-xl', stat.bg]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path :d="stat.icon" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Revenue Chart -->
      <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
        <h3 class="font-bold text-gray-900 mb-4">Doanh thu 7 ngày gần nhất</h3>
        <div class="h-64">
          <canvas ref="revenueChartRef"></canvas>
        </div>
      </div>

      <!-- Order Status -->
      <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
        <h3 class="font-bold text-gray-900 mb-4">Trạng thái đơn hàng</h3>
        <div class="h-64">
          <canvas ref="statusChartRef"></canvas>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Top Products -->
      <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
        <h3 class="font-bold text-gray-900 mb-4">Top sản phẩm bán chạy</h3>
        <div class="space-y-3">
          <div v-for="(p, i) in data.top_san_phams" :key="p.id" class="flex items-center gap-3">
            <span :class="['w-8 h-8 rounded-lg flex items-center justify-center text-white text-sm font-bold', i === 0 ? 'bg-yellow-500' : i === 1 ? 'bg-gray-400' : 'bg-amber-600']">{{ i + 1 }}</span>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 line-clamp-1">{{ p.ten }}</p>
              <p class="text-xs text-gray-500">{{ formatPrice(p.gia) }}</p>
            </div>
            <span class="text-sm font-bold text-primary-600">{{ p.tong_da_ban }} đã bán</span>
          </div>
          <p v-if="!data.top_san_phams?.length" class="text-gray-500 text-sm">Chưa có dữ liệu</p>
        </div>
      </div>

      <!-- Recent Orders -->
      <div class="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
        <h3 class="font-bold text-gray-900 mb-4">Đơn hàng mới</h3>
        <div class="space-y-3">
          <div v-for="o in data.don_hang_gan_day" :key="o.id" class="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
            <div>
              <p class="text-sm font-medium text-gray-900">{{ o.ma_don_hang }}</p>
              <p class="text-xs text-gray-500">{{ o.ho_ten }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-bold text-gray-900">{{ formatPrice(o.thanh_tien) }}</p>
              <span :class="['badge text-xs', `badge-${o.trang_thai}`]">{{ statusLabels[o.trang_thai] }}</span>
            </div>
          </div>
          <p v-if="!data.don_hang_gan_day?.length" class="text-gray-500 text-sm">Chưa có đơn hàng</p>
        </div>
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
const revenueChartRef = ref(null)
const statusChartRef = ref(null)
const statusLabels = { 
  cho_xu_ly: 'Chờ xử lý', 
  da_xac_nhan: 'Đã xác nhận', 
  dang_giao: 'Đang giao', 
  da_giao: 'Đã giao', 
  da_huy: 'Đã hủy' 
}

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }

const stats = computed(() => [
  { label: 'Doanh thu tháng', value: formatPrice(data.value.doanh_thu_thang || 0), icon: 'M12 8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 10c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7zm0-12c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5z', bg: 'bg-indigo-500' },
  { label: 'Đơn chờ xử lý', value: data.value.don_cho_xu_ly || 0, icon: 'M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z', bg: 'bg-yellow-500' },
  { label: 'Tổng sản phẩm', value: data.value.tong_san_pham || 0, icon: 'M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z', bg: 'bg-green-500' },
  { label: 'Khách hàng', value: data.value.tong_nguoi_dung || 0, icon: 'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z', bg: 'bg-blue-500' },
])

onMounted(async () => {
  try {
    const res = await api.get('/dashboard/admin')
    data.value = res.data

    await nextTick()

    // Revenue chart
    if (revenueChartRef.value && data.value.bieu_do_doanh_thu) {
      new Chart(revenueChartRef.value, {
        type: 'line',
        data: {
          labels: data.value.bieu_do_doanh_thu.map(d => {
            const date = new Date(d.date)
            return date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' })
          }),
          datasets: [{
            label: 'Doanh thu',
            data: data.value.bieu_do_doanh_thu.map(d => d.doanh_thu),
            borderColor: '#6366f1',
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#6366f1',
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: (value) => new Intl.NumberFormat('vi-VN', { notation: 'compact', compactDisplay: 'short' }).format(value)
              }
            }
          }
        }
      })
    }

    // Status chart
    if (statusChartRef.value && data.value.phan_bo_trang_thai) {
      const os = data.value.phan_bo_trang_thai
      const labels = Object.keys(os).map(k => statusLabels[k] || k)
      const values = Object.values(os)
      new Chart(statusChartRef.value, {
        type: 'doughnut',
        data: {
          labels,
          datasets: [{
            data: values,
            backgroundColor: ['#f59e0b', '#3b82f6', '#6366f1', '#22c55e', '#ef4444'],
            borderWidth: 2,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { padding: 15, usePointStyle: true, pointStyleWidth: 10 }
            }
          }
        }
      })
    }
  } catch (e) {
    console.error('Dashboard error:', e)
  }
})
</script>
