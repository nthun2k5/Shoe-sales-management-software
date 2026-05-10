<template>
  <div class="space-y-6 animate-fade-in">
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-gray-900">Danh mục sản phẩm</h2>
      <button @click="openNew" class="btn-primary">+ Thêm danh mục</button>
    </div>

    <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-6 py-4 font-semibold text-gray-600">Tên</th>
            <th class="text-left px-4 py-4 font-semibold text-gray-600">Slug</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Sản phẩm</th>
            <th class="text-center px-4 py-4 font-semibold text-gray-600">Trạng thái</th>
            <th class="text-right px-6 py-4 font-semibold text-gray-600">Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in categories" :key="cat.id" class="border-b border-gray-50 hover:bg-gray-50">
            <td class="px-6 py-4 font-medium text-gray-900">{{ cat.ten }}</td>
            <td class="px-4 py-4 text-gray-500">{{ cat.slug }}</td>
            <td class="px-4 py-4 text-center">{{ cat.so_luong_san_pham }}</td>
            <td class="px-4 py-4 text-center"><span :class="['badge', cat.dang_hoat_dong ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500']">{{ cat.dang_hoat_dong ? 'Hoạt động' : 'Ẩn' }}</span></td>
            <td class="px-6 py-4 text-right">
              <button @click="editCat(cat)" class="p-2 text-blue-500 hover:bg-blue-50 rounded-lg"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg></button>
              <button @click="deleteCat(cat.id, cat.name)" class="p-2 text-red-500 hover:bg-red-50 rounded-lg"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form -->
    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="showForm = false">
      <div class="bg-white rounded-xl p-8 w-full max-w-md animate-scale-in">
        <h3 class="text-lg font-bold mb-4">{{ editingId ? 'Sửa danh mục' : 'Thêm danh mục' }}</h3>
        <form @submit.prevent="saveCat" class="space-y-4">
          <div><label class="block text-sm font-semibold text-gray-700 mb-1">Tên danh mục</label><input v-model="formData.name" class="input-field" required /></div>
          <div><label class="block text-sm font-semibold text-gray-700 mb-1">Mô tả</label><textarea v-model="formData.description" class="input-field" rows="2"></textarea></div>
          <label class="flex items-center gap-2"><input type="checkbox" v-model="formData.dang_hoat_dong" class="w-4 h-4" /><span class="text-sm">Hoạt động</span></label>
          <div class="flex gap-3 pt-2">
            <button type="submit" class="btn-primary flex-1">Lưu</button>
            <button type="button" @click="showForm = false" class="btn-outline flex-1">Hủy</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

const { success, error: showError } = useToast()
const categories = ref([])
const showForm = ref(false)
const editingId = ref(null)
const formData = reactive({ name: '', description: '', parent_id: null, is_active: true })

async function fetchCategories() {
  try { const res = await api.get('/categories/all'); categories.value = res.data } catch {}
}

function openNew() {
  editingId.value = null
  Object.assign(formData, { ten: '', mo_ta: '', id_cha: null, dang_hoat_dong: true })
  showForm.value = true
}

function editCat(cat) {
  editingId.value = cat.id
  Object.assign(formData, { ten: cat.ten, mo_ta: cat.mo_ta, id_cha: cat.id_cha, dang_hoat_dong: cat.dang_hoat_dong })
  showForm.value = true
}

async function saveCat() {
  try {
    if (editingId.value) { await api.put(`/categories/${editingId.value}`, formData); success('Đã cập nhật') }
    else { await api.post('/categories', formData); success('Đã thêm danh mục') }
    showForm.value = false
    fetchCategories()
  } catch (e) { showError(e.response?.data?.detail || 'Lỗi') }
}

async function deleteCat(id, name) {
  if (!confirm(`Xóa danh mục "${name}"?`)) return
  try { await api.delete(`/categories/${id}`); success('Đã xóa'); fetchCategories() }
  catch (e) { showError(e.response?.data?.detail || 'Lỗi') }
}

onMounted(fetchCategories)
</script>
