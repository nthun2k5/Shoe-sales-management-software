<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Nhật ký hoạt động</h2>
        <p class="text-sm text-gray-500">Theo dõi các thay đổi và hành động trên hệ thống</p>
      </div>
      <div class="flex items-center gap-2">
        <button @click="fetchLogs" class="p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors" title="Làm mới">
          <svg class="w-5 h-5" :class="{'animate-spin': loading}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-wrap gap-4">
      <div class="relative flex-1 min-w-[200px]">
        <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </span>
        <input v-model="searchQuery" type="text" placeholder="Tìm kiếm hành động, mô tả..." class="w-full pl-10 pr-4 py-2 bg-gray-50 border-none rounded-lg focus:ring-2 focus:ring-primary-500 text-sm">
      </div>
      <select v-model="actionFilter" class="select-modern w-auto text-sm py-2 px-4 bg-gray-50">
        <option value="">Tất cả hành động</option>
        <option value="CREATE">Thêm mới</option>
        <option value="UPDATE">Cập nhật</option>
        <option value="DELETE">Xóa</option>
        <option value="LOGIN">Đăng nhập</option>
      </select>
    </div>

    <!-- Logs Table -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100">
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Thời gian</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Người dùng</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Hành động</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Mô tả</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">IP Address</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="loading" v-for="i in 5" :key="i" class="animate-pulse">
              <td v-for="j in 5" :key="j" class="px-6 py-4"><div class="h-4 bg-gray-100 rounded w-full"></div></td>
            </tr>
            <tr v-else-if="filteredLogs.length === 0">
              <td colspan="5" class="px-6 py-10 text-center text-gray-500">Không tìm thấy nhật ký nào</td>
            </tr>
            <tr v-for="log in filteredLogs" :key="log.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 text-sm text-gray-600 whitespace-nowrap">
                {{ formatDate(log.ngay_tao) }}
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <div class="w-7 h-7 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center text-xs font-bold">
                    {{ (log.ten_nguoi_dung || 'System').charAt(0) }}
                  </div>
                  <span class="text-sm font-medium text-gray-700">{{ log.ten_nguoi_dung || 'Hệ thống' }}</span>
                </div>
              </td>
              <td class="px-6 py-4">
                <span :class="getActionClass(log.hanh_dong)" class="px-2 py-1 rounded-md text-xs font-bold uppercase tracking-wider">
                  {{ log.hanh_dong }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">
                {{ log.mo_ta }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 font-mono">
                {{ log.ip_address || '---' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination Placeholder -->
      <div class="px-6 py-4 border-t border-gray-100 bg-gray-50 flex items-center justify-between">
        <p class="text-sm text-gray-500">Hiển thị {{ filteredLogs.length }} kết quả</p>
        <div class="flex gap-2">
          <button disabled class="px-3 py-1 bg-white border border-gray-200 rounded text-gray-400 cursor-not-allowed text-sm">Trước</button>
          <button disabled class="px-3 py-1 bg-white border border-gray-200 rounded text-gray-400 cursor-not-allowed text-sm">Sau</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'

const logs = ref([])
const loading = ref(true)
const searchQuery = ref('')
const actionFilter = ref('')

const fetchLogs = async () => {
  loading.value = true
  try {
    const response = await api.get('/logs/')
    logs.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy nhật ký:', error)
  } finally {
    loading.value = false
  }
}

const filteredLogs = computed(() => {
  return logs.value.filter(log => {
    const matchesSearch = !searchQuery.value || 
      log.hanh_dong.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (log.mo_ta && log.mo_ta.toLowerCase().includes(searchQuery.value.toLowerCase()))
    const matchesAction = !actionFilter.value || log.hanh_dong === actionFilter.value
    return matchesSearch && matchesAction
  })
})

const formatDate = (dateString) => {
  if (!dateString) return '---'
  return new Date(dateString).toLocaleString('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const getActionClass = (action) => {
  switch (action) {
    case 'CREATE': return 'bg-green-100 text-green-700'
    case 'UPDATE': return 'bg-blue-100 text-blue-700'
    case 'DELETE': return 'bg-red-100 text-red-700'
    case 'LOGIN': return 'bg-purple-100 text-purple-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}

onMounted(fetchLogs)
</script>
