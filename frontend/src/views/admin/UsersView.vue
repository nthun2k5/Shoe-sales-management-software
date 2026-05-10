<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4 flex-1">
        <div class="relative max-w-xs w-full">
          <input v-model="search" @input="fetchUsers" class="input-field pl-10" placeholder="Tìm người dùng..." />
          <svg class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
        <button @click="handleExport" class="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 rounded-lg text-sm font-medium hover:bg-green-100 transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          Xuất Excel
        </button>
      </div>
      <button @click="openCreateModal" class="btn-primary w-10 h-10 rounded-xl flex items-center justify-center" title="Thêm người dùng">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
      </button>
    </div>

    <!-- Users Table -->
    <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-6 py-4 font-semibold text-gray-600">Người dùng</th>
            <th class="text-left px-4 py-4 font-semibold text-gray-600">Email</th>
            <th class="text-left px-4 py-4 font-semibold text-gray-600">Điện thoại</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Vai trò</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Trạng thái</th>
            <th class="text-right px-6 py-4 font-semibold text-gray-600">Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id" class="border-b border-gray-50 hover:bg-gray-50/50">
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-linear-to-r from-red-500 to-red-600 flex items-center justify-center text-white text-sm font-bold shrink-0">
                  {{ u.ho_ten?.charAt(0) }}
                </div>
                <div>
                  <p class="font-medium text-gray-900">{{ u.ho_ten }}</p>
                  <p v-if="u.dia_chi" class="text-xs text-gray-400 truncate max-w-[200px]">{{ u.dia_chi }}</p>
                </div>
              </div>
            </td>
            <td class="px-4 py-4 text-gray-600">{{ u.email }}</td>
            <td class="px-4 py-4 text-gray-600">{{ u.so_dien_thoai || '—' }}</td>
            <td class="px-4 py-4 text-center">
              <span :class="['badge', u.vai_tro === 'quan_tri' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700']">
                {{ u.vai_tro === 'quan_tri' ? 'Quản trị' : 'Khách' }}
              </span>
            </td>
            <td class="px-4 py-4 text-center">
              <span :class="['badge', u.dang_hoat_dong ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']">
                {{ u.dang_hoat_dong ? 'Hoạt động' : 'Bị khóa' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end gap-1">
                <button @click="openEditModal(u)" class="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors flex items-center justify-center" title="Sửa">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.586a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                </button>
                <button v-if="u.vai_tro !== 'quan_tri'" @click="toggleActive(u.id)"
                  :class="['w-8 h-8 rounded-lg transition-colors flex items-center justify-center',
                    u.dang_hoat_dong ? 'bg-red-50 text-red-600 hover:bg-red-100' : 'bg-green-50 text-green-600 hover:bg-green-100']"
                  :title="u.dang_hoat_dong ? 'Khóa' : 'Mở khóa'">
                  <svg v-if="u.dang_hoat_dong" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"/></svg>
                </button>
                <button @click="confirmDelete(u)" class="w-8 h-8 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 transition-colors flex items-center justify-center" title="Xóa">
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
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md z-10 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-1">{{ isEditing ? 'Sửa người dùng' : 'Thêm người dùng mới' }}</h3>
          <p class="text-sm text-gray-500 mb-6">{{ isEditing ? `Cập nhật thông tin cho ${modalForm.ho_ten}` : 'Nhập thông tin người dùng mới' }}</p>

          <form @submit.prevent="submitForm" class="space-y-4">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Họ tên *</label>
              <input v-model="modalForm.ho_ten" type="text" required class="input-field" placeholder="Nguyễn Văn A" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Email *</label>
              <input v-model="modalForm.email" type="email" required class="input-field" placeholder="email@example.com" :disabled="isEditing" />
            </div>
            <div v-if="!isEditing" class="relative">
              <label class="block text-xs font-medium text-gray-500 mb-1">Mật khẩu *</label>
              <input v-model="modalForm.mat_khau" :type="showPassword ? 'text' : 'password'" required class="input-field pr-10" placeholder="Nhập mật khẩu" />
              <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-8 text-gray-400 hover:text-gray-600 transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path v-if="showPassword" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L6.59 6.59m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
              </button>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Số điện thoại</label>
              <input v-model="modalForm.so_dien_thoai" type="tel" class="input-field" placeholder="0123456789" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Địa chỉ</label>
              <textarea v-model="modalForm.dia_chi" rows="2" class="input-field" placeholder="Nhập địa chỉ..."></textarea>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Vai trò</label>
              <select v-model="modalForm.vai_tro" class="select-modern">
                <option value="khach">Khách hàng</option>
                <option value="quan_tri">Quản trị viên</option>
              </select>
            </div>

            <div class="flex gap-3 pt-4">
              <button type="button" @click="showModal = false" class="flex-1 py-3 border border-gray-200 rounded-xl text-sm font-medium hover:bg-gray-50 transition-colors">Hủy</button>
              <button type="submit" :disabled="formLoading" class="flex-1 py-3 bg-red-600 text-white rounded-xl text-sm font-bold hover:bg-red-700 transition-colors disabled:opacity-50">
                {{ formLoading ? 'Đang xử lý...' : (isEditing ? 'Cập nhật' : 'Tạo mới') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
      <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showDeleteModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-sm z-10 p-6 text-center">
          <div class="w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 mb-1">Xóa người dùng</h3>
          <p class="text-sm text-gray-500 mb-6">Bạn có chắc muốn xóa người dùng <span class="font-semibold text-gray-900">{{ deletingUser?.ho_ten }}</span>? Hành động này không thể hoàn tác.</p>
          <div class="flex gap-3">
            <button @click="showDeleteModal = false" class="flex-1 py-3 border border-gray-200 rounded-xl text-sm font-medium hover:bg-gray-50 transition-colors">Hủy</button>
            <button @click="deleteUser" :disabled="deleteLoading" class="flex-1 py-3 bg-red-600 text-white rounded-xl text-sm font-bold hover:bg-red-700 transition-colors disabled:opacity-50">
              {{ deleteLoading ? 'Đang xóa...' : 'Xóa' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'
import { exportToExcel } from '@/utils/excel'

const { success, error: showError } = useToast()
const users = ref([])
const search = ref('')

function handleExport() {
  const data = users.value.map(u => ({
    'ID': u.id,
    'Họ tên': u.ho_ten,
    'Email': u.email,
    'Số điện thoại': u.so_dien_thoai || '',
    'Địa chỉ': u.dia_chi || '',
    'Vai trò': u.vai_tro === 'quan_tri' ? 'Quản trị viên' : 'Khách hàng',
    'Trạng thái': u.dang_hoat_dong ? 'Hoạt động' : 'Bị khóa',
    'Ngày tham gia': new Date(u.ngay_tao).toLocaleDateString('vi-VN')
  }))
  exportToExcel(data, 'Danh_sach_nguoi_dung', 'Nguoi_dung')
}
const showModal = ref(false)
const showDeleteModal = ref(false)
const isEditing = ref(false)
const formLoading = ref(false)
const deleteLoading = ref(false)
const deletingUser = ref(null)
const showPassword = ref(false)

const modalForm = reactive({
  id: null,
  email: '',
  ho_ten: '',
  mat_khau: '',
  so_dien_thoai: '',
  dia_chi: '',
  vai_tro: 'khach',
})

async function fetchUsers() {
  try {
    const params = {}
    if (search.value) params.search = search.value
    const res = await api.get('/users', { params })
    users.value = res.data
  } catch {}
}

function openCreateModal() {
  isEditing.value = false
  modalForm.id = null
  modalForm.email = ''
  modalForm.ho_ten = ''
  modalForm.mat_khau = ''
  modalForm.so_dien_thoai = ''
  modalForm.dia_chi = ''
  modalForm.vai_tro = 'khach'
  showPassword.value = false
  showModal.value = true
}

function openEditModal(user) {
  isEditing.value = true
  modalForm.id = user.id
  modalForm.email = user.email
  modalForm.ho_ten = user.ho_ten
  modalForm.mat_khau = ''
  modalForm.so_dien_thoai = user.so_dien_thoai || ''
  modalForm.dia_chi = user.dia_chi || ''
  modalForm.vai_tro = user.vai_tro
  showModal.value = true
}

async function submitForm() {
  formLoading.value = true
  try {
    if (isEditing.value) {
      const data = {
        ho_ten: modalForm.ho_ten,
        so_dien_thoai: modalForm.so_dien_thoai || null,
        dia_chi: modalForm.dia_chi || null,
        vai_tro: modalForm.vai_tro,
      }
      await api.put(`/users/${modalForm.id}`, data)
      success('Đã cập nhật người dùng')
    } else {
      await api.post('/users', modalForm)
      success('Đã tạo người dùng mới')
    }
    showModal.value = false
    fetchUsers()
  } catch (e) {
    showError(e.response?.data?.detail || 'Có lỗi xảy ra')
  } finally {
    formLoading.value = false
  }
}

function confirmDelete(user) {
  deletingUser.value = user
  showDeleteModal.value = true
}

async function deleteUser() {
  deleteLoading.value = true
  try {
    await api.delete(`/users/${deletingUser.value.id}`)
    success('Đã xóa người dùng')
    showDeleteModal.value = false
    fetchUsers()
  } catch (e) {
    showError(e.response?.data?.detail || 'Có lỗi xảy ra')
  } finally {
    deleteLoading.value = false
  }
}

async function toggleActive(id) {
  try {
    await api.put(`/users/${id}/toggle-active`)
    success('Đã cập nhật trạng thái')
    fetchUsers()
  } catch (e) {
    showError(e.response?.data?.detail || 'Có lỗi xảy ra')
  }
}

onMounted(fetchUsers)
</script>
