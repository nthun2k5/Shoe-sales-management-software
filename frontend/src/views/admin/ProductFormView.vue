<template>
  <div class="max-w-3xl mx-auto animate-fade-in">
    <div class="bg-white rounded-xl p-8 border border-gray-100 shadow-sm">
      <h2 class="text-xl font-bold text-gray-900 mb-6">{{ isEdit ? 'Chỉnh sửa sản phẩm' : 'Thêm sản phẩm mới' }}</h2>
      <form @submit.prevent="handleSubmit" class="space-y-5">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div><label class="block text-sm font-semibold text-gray-700 mb-1">Tên sản phẩm *</label><input v-model="form.ten" class="input-field" required /></div>
          <div><label class="block text-sm font-semibold text-gray-700 mb-1">Giá (₫) *</label><input v-model="formattedGia" type="text" class="input-field" required /></div>
          <div><label class="block text-sm font-semibold text-gray-700 mb-1">Giá khuyến mãi (₫)</label><input v-model="formattedGiaKM" type="text" class="input-field" /></div>
          <div><label class="block text-sm font-semibold text-gray-700 mb-1">Số lượng tồn kho</label><input v-model="formattedTonKho" type="text" class="input-field" /></div>
          <div><label class="block text-sm font-semibold text-gray-700 mb-1">SKU</label><input v-model="form.ma_sku" class="input-field" /></div>
          <div><label class="block text-sm font-semibold text-gray-700 mb-1">Danh mục</label>
            <select v-model="form.id_danh_muc" class="select-modern">
              <option :value="null">-- Chọn --</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.ten }}</option>
            </select>
          </div>
          <div><label class="block text-sm font-semibold text-gray-700 mb-1">Thương hiệu</label><input v-model="form.thuong_hieu" class="input-field" /></div>
        </div>
        <div><label class="block text-sm font-semibold text-gray-700 mb-1">Mô tả ngắn</label><input v-model="form.mo_ta_ngan" class="input-field" /></div>
        <div><label class="block text-sm font-semibold text-gray-700 mb-1">Các kích thước hỗ trợ (VD: 36, 37, 38)</label><input v-model="form.cac_kich_thuoc" class="input-field" placeholder="Cách nhau bằng dấu phẩy" /></div>
        <div><label class="block text-sm font-semibold text-gray-700 mb-1">Mô tả chi tiết</label><textarea v-model="form.mo_ta" class="input-field" rows="4"></textarea></div>

        <div class="flex items-center gap-6">
          <label class="flex items-center gap-2 cursor-pointer"><input type="checkbox" v-model="form.dang_hoat_dong" class="w-4 h-4 rounded border-gray-300 text-primary-600" /><span class="text-sm font-medium text-gray-700">Đang bán</span></label>
          <label class="flex items-center gap-2 cursor-pointer"><input type="checkbox" v-model="form.la_noi_bat" class="w-4 h-4 rounded border-gray-300 text-primary-600" /><span class="text-sm font-medium text-gray-700">Nổi bật</span></label>
        </div>

        <!-- Images -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Hình ảnh sản phẩm</label>
          <div class="grid grid-cols-4 gap-3 mb-3">
            <div v-for="(img, idx) in previewImages" :key="idx" class="relative aspect-square bg-gray-100 rounded-lg overflow-hidden group">
              <img :src="img" class="w-full h-full object-cover" />
              <button @click="removeImage(idx)" type="button" class="absolute top-1 right-1 w-6 h-6 bg-red-500 text-white rounded-full text-xs opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">×</button>
            </div>
          </div>
          <label class="flex items-center justify-center w-full h-24 border-2 border-dashed border-gray-300 rounded-xl hover:border-primary-400 cursor-pointer transition-colors">
            <input type="file" accept="image/*" multiple @change="handleImageUpload" class="hidden" />
            <div class="text-center">
              <svg class="w-8 h-8 text-gray-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              <p class="text-xs text-gray-500 mt-1">Kéo thả hoặc click để upload</p>
            </div>
          </label>
        </div>

        <div v-if="errorMsg" class="text-red-500 text-sm bg-red-50 p-3 rounded-lg">{{ errorMsg }}</div>

        <div class="flex items-center gap-3 pt-4">
          <button type="submit" :disabled="saving" class="btn-primary py-3 px-8">
            <span v-if="saving" class="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></span>
            <span v-else>{{ isEdit ? 'Cập nhật' : 'Thêm sản phẩm' }}</span>
          </button>
          <RouterLink to="/admin/products" class="btn-outline py-3 px-6">Hủy</RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const router = useRouter()
const { success, error: showError } = useToast()

const isEdit = computed(() => !!route.params.id)
const categories = ref([])
const previewImages = ref([])
const imageFiles = ref([])
const saving = ref(false)
const errorMsg = ref('')

const form = reactive({
  ten: '', mo_ta: '', mo_ta_ngan: '',
  gia: 0, gia_khuyen_mai: null, so_luong_ton: 0,
  ma_sku: '', id_danh_muc: null, thuong_hieu: '',
  dang_hoat_dong: true, la_noi_bat: false, cac_kich_thuoc: ''
})

const formattedGia = computed({
  get: () => form.gia ? new Intl.NumberFormat('vi-VN').format(form.gia) : '',
  set: (val) => { form.gia = Number(val.toString().replace(/[^\d]/g, '')) || 0 }
})

const formattedGiaKM = computed({
  get: () => form.gia_khuyen_mai ? new Intl.NumberFormat('vi-VN').format(form.gia_khuyen_mai) : '',
  set: (val) => { form.gia_khuyen_mai = val ? (Number(val.toString().replace(/[^\d]/g, '')) || null) : null }
})

const formattedTonKho = computed({
  get: () => form.so_luong_ton ? new Intl.NumberFormat('vi-VN').format(form.so_luong_ton) : '0',
  set: (val) => { form.so_luong_ton = Number(val.toString().replace(/[^\d]/g, '')) || 0 }
})

function handleImageUpload(e) {
  const files = Array.from(e.target.files)
  files.forEach(file => {
    const reader = new FileReader()
    reader.onload = (ev) => {
      previewImages.value.push(ev.target.result)
      imageFiles.value.push(ev.target.result)
    }
    reader.readAsDataURL(file)
  })
}

function removeImage(idx) {
  previewImages.value.splice(idx, 1)
  imageFiles.value.splice(idx, 1)
}

async function handleSubmit() {
  saving.value = true
  errorMsg.value = ''
  try {
    if (isEdit.value) {
      await api.put(`/products/${route.params.id}`, form)
      for (const imgData of imageFiles.value) {
        await api.post(`/products/${route.params.id}/images`, { du_lieu_anh: imgData, la_anh_chinh: false, thu_tu_sap_xep: 0 })
      }
      success('Cập nhật thành công')
    } else {
      const payload = { ...form, anh_san_phams: imageFiles.value.map((d, i) => ({ du_lieu_anh: d, la_anh_chinh: i === 0, thu_tu_sap_xep: i })) }
      await api.post('/products', payload)
      success('Thêm sản phẩm thành công')
    }
    router.push('/admin/products')
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Có lỗi xảy ra'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try { const res = await api.get('/categories/all'); categories.value = res.data } catch {}
  if (isEdit.value) {
    try {
      const res = await api.get(`/products/${route.params.id}`)
      Object.assign(form, { ten: res.data.ten, mo_ta: res.data.mo_ta, mo_ta_ngan: res.data.mo_ta_ngan, gia: res.data.gia, gia_khuyen_mai: res.data.gia_khuyen_mai, so_luong_ton: res.data.so_luong_ton, ma_sku: res.data.ma_sku, id_danh_muc: res.data.id_danh_muc, thuong_hieu: res.data.thuong_hieu, dang_hoat_dong: res.data.dang_hoat_dong, la_noi_bat: res.data.la_noi_bat, cac_kich_thuoc: res.data.cac_kich_thuoc || '' })
      previewImages.value = (res.data.anh_san_phams || []).map(i => i.du_lieu_anh)
    } catch {}
  }
})
</script>
