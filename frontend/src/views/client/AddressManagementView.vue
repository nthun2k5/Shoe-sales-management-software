<template>
  <div class="space-y-6">
    <!-- Header và nút thêm giữ nguyên -->
    <div class="flex items-center justify-between" data-aos="fade-down">
      <div>
        <h2 class="text-xl font-bold text-gray-900">Địa chỉ nhận hàng</h2>
        <p class="text-sm text-gray-500 mt-1">Quản lý các địa chỉ giao hàng của bạn</p>
      </div>
      <button @click="openAdd" class="flex items-center gap-2 px-4 py-2.5 bg-red-600 text-white rounded-xl text-sm font-bold hover:bg-red-700 transition-all shadow-lg shadow-red-500/20">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Thêm địa chỉ mới
      </button>
    </div>

    <!-- Address List (giữ nguyên) -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="i in 2" :key="i" class="bg-white rounded-2xl p-6 animate-pulse border border-gray-100">
        <div class="h-5 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div class="h-4 bg-gray-100 rounded w-2/3 mb-2"></div>
        <div class="h-4 bg-gray-100 rounded w-1/2"></div>
      </div>
    </div>

    <div v-else-if="addresses.length === 0" class="bg-white rounded-2xl p-12 text-center border border-gray-100 shadow-sm" data-aos="zoom-in">
      <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-10 h-10 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
      </div>
      <p class="text-gray-500 font-medium">Bạn chưa có địa chỉ nhận hàng nào</p>
      <button @click="openAdd" class="mt-4 text-red-600 font-bold hover:underline">Thêm địa chỉ đầu tiên</button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-5">
      <!-- ... card địa chỉ ... (giữ nguyên nội dung cũ nhưng có thể tối ưu nhẹ) -->
      <div v-for="(addr, idx) in addresses" :key="addr.id" 
        class="bg-white rounded-3xl p-6 border transition-all relative group overflow-hidden"
        :class="addr.la_mac_dinh ? 'border-red-200 shadow-xl shadow-red-500/5' : 'border-gray-100 hover:border-red-100 hover:shadow-lg hover:shadow-gray-200/50'"
        data-aos="fade-up" :data-aos-delay="idx * 50">
        
        <div v-if="addr.la_mac_dinh" class="absolute top-0 right-0">
          <div class="bg-red-600 text-white text-[9px] font-black px-4 py-1.5 rounded-bl-2xl uppercase tracking-widest shadow-sm">
            Mặc định
          </div>
        </div>

        <div class="flex flex-col h-full">
          <div class="flex items-center gap-4 mb-6">
            <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 transition-transform group-hover:scale-110 duration-500', addr.la_mac_dinh ? 'bg-red-50 text-red-600' : 'bg-gray-50 text-gray-400']">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            </div>
            <div class="min-w-0">
              <h3 class="font-black text-gray-900 text-base mb-0.5 truncate uppercase tracking-tight">{{ addr.ten_nguoi_nhan }}</h3>
              <p class="text-sm font-bold text-red-600/70 tracking-wider">{{ addr.so_dien_thoai }}</p>
            </div>
          </div>

          <div class="flex-1">
            <div class="flex gap-2 text-gray-400 mb-1">
              <svg class="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              <span class="text-[10px] font-black uppercase tracking-widest">Địa chỉ giao hàng</span>
            </div>
            <p class="text-sm text-gray-600 leading-relaxed font-medium pl-6">{{ addr.dia_chi }}</p>
          </div>
          
          <div class="mt-8 pt-5 border-t border-gray-50 flex items-center justify-between">
            <div class="flex items-center gap-4">
              <button @click="openEdit(addr)" class="text-[10px] font-black text-gray-400 hover:text-gray-900 transition-colors uppercase tracking-[0.2em] flex items-center gap-1.5 group/btn">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
                Sửa
              </button>
              <button @click="deleteAddress(addr)" class="text-[10px] font-black text-gray-400 hover:text-red-600 transition-colors uppercase tracking-[0.2em] flex items-center gap-1.5 group/btn">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                Xóa
              </button>
            </div>
            <button v-if="!addr.la_mac_dinh" @click="setDefault(addr)" 
              class="text-[10px] font-black text-blue-600 hover:text-blue-700 transition-colors uppercase tracking-[0.2em] bg-blue-50 px-3 py-1.5 rounded-lg">
              Đặt mặc định
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL THÊM/SỬA - THIẾT KẾ LẠI HOÀN TOÀN -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showModal" class="fixed inset-0 z-100 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/60 backdrop-blur-md transition-opacity" @click="closeModal"></div>
          
          <div class="relative bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden transform transition-all duration-300 scale-100">
            <!-- Header với gradient -->
            <div class="relative bg-gradient-to-r from-gray-50 to-white px-6 pt-6 pb-4 border-b border-gray-100">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-2xl font-black tracking-tight">
                    <span class="text-gray-800">{{ editingAddr ? 'Cập nhật' : 'Thêm mới' }}</span>
                    <span class="text-red-600 ml-1">địa chỉ</span>
                  </h3>
                  <p class="text-xs text-gray-400 font-medium mt-1">Vui lòng nhập thông tin chính xác để giao hàng nhanh chóng</p>
                </div>
                <button @click="closeModal" class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors text-gray-400">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-width="2"/></svg>
                </button>
              </div>
            </div>

            <form @submit.prevent="saveAddress" class="p-6 space-y-6">
              <!-- Họ tên và SĐT trên cùng 1 hàng (grid) -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                <div class="relative">
                  <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1.5 ml-1">Họ tên người nhận</label>
                  <div class="relative">
                    <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                    </span>
                    <input v-model="form.ten_nguoi_nhan" type="text" required
                      class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-red-400 focus:ring-4 focus:ring-red-50 transition-all outline-none text-gray-800 font-medium"
                      placeholder="Nguyễn Văn A" />
                  </div>
                  <p v-if="errors.ten_nguoi_nhan" class="mt-1.5 text-xs text-red-600 font-semibold flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    {{ errors.ten_nguoi_nhan }}
                  </p>
                </div>

                <div class="relative">
                  <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1.5 ml-1">Số điện thoại</label>
                  <div class="relative">
                    <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                    </span>
                    <input v-model="form.so_dien_thoai" type="tel" required
                      class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-red-400 focus:ring-4 focus:ring-red-50 transition-all outline-none text-gray-800 font-medium"
                      placeholder="0912 345 678" />
                  </div>
                  <p v-if="errors.so_dien_thoai" class="mt-1.5 text-xs text-red-600 font-semibold flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    {{ errors.so_dien_thoai }}
                  </p>
                </div>
              </div>

              <!-- Địa chỉ chi tiết (có icon) -->
              <div class="relative">
                <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1.5 ml-1">Địa chỉ chi tiết</label>
                <div class="relative">
                  <span class="absolute left-4 top-4 text-gray-400">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  </span>
                  <textarea v-model="form.dia_chi" rows="3" required
                    class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-red-400 focus:ring-4 focus:ring-red-50 transition-all outline-none text-gray-800 font-medium resize-none"
                    placeholder="Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành phố"></textarea>
                </div>
                <p v-if="errors.dia_chi" class="mt-1.5 text-xs text-red-600 font-semibold flex items-center gap-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  {{ errors.dia_chi }}
                </p>
              </div>

              <!-- Checkbox mặc định được thiết kế lại -->
              <div class="flex items-center justify-between pt-2 pb-1">
                <div class="flex items-center gap-3">
                  <div class="relative">
                    <input type="checkbox" v-model="form.la_mac_dinh" id="default_address_checkbox" class="sr-only peer" />
                    <div class="w-10 h-5 bg-gray-200 rounded-full peer peer-checked:bg-red-600 peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all cursor-pointer"></div>
                  </div>
                  <label for="default_address_checkbox" class="text-sm font-bold text-gray-700 cursor-pointer select-none">
                    Đặt làm địa chỉ mặc định
                  </label>
                </div>
                <span class="text-[10px] text-gray-400 italic">Ưu tiên sử dụng khi thanh toán</span>
              </div>

              <!-- Hành động -->
              <div class="flex gap-3 pt-4">
                <button type="button" @click="closeModal"
                  class="flex-1 py-3.5 rounded-xl border border-gray-200 text-gray-600 font-bold text-sm hover:bg-gray-50 transition-all">
                  Hủy bỏ
                </button>
                <button type="submit" :disabled="saving"
                  class="flex-1 py-3.5 rounded-xl bg-gradient-to-r from-red-600 to-red-700 text-white font-bold text-sm shadow-lg shadow-red-500/20 hover:from-red-700 hover:to-red-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
                  {{ saving ? 'Đang lưu...' : (editingAddr ? 'Cập nhật' : 'Thêm mới') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
// Phần script giữ nguyên hoàn toàn (tôi vẫn giữ nguyên logic cũ)
import { computed, onMounted, reactive, ref } from 'vue'
import { useToast } from '@/composables/useToast'
import api from '@/services/api'

const { success, error: showError } = useToast()

const addresses = ref([])
const loading = ref(true)
const saving = ref(false)
const showModal = ref(false)
const editingAddr = ref(null)

const form = reactive({
  ten_nguoi_nhan: '',
  so_dien_thoai: '',
  dia_chi: '',
  la_mac_dinh: false
})

const errors = reactive({
  ten_nguoi_nhan: '',
  so_dien_thoai: '',
  dia_chi: ''
})

const isPhoneValid = computed(() => {
  const phone = (form.so_dien_thoai ?? '').trim()
  if (!phone) return false
  const normalized = phone.replace(/\s+/g, '')
  return /^\d{10,11}$/.test(normalized)
})

function resetForm() {
  form.ten_nguoi_nhan = ''
  form.so_dien_thoai = ''
  form.dia_chi = ''
  form.la_mac_dinh = addresses.value.length === 0

  errors.ten_nguoi_nhan = ''
  errors.so_dien_thoai = ''
  errors.dia_chi = ''
}

function validateForm() {
  errors.ten_nguoi_nhan = ''
  errors.so_dien_thoai = ''
  errors.dia_chi = ''

  const ten = (form.ten_nguoi_nhan ?? '').trim()
  const phoneRaw = (form.so_dien_thoai ?? '').trim()
  const phone = phoneRaw.replace(/\s+/g, '')
  const addr = (form.dia_chi ?? '').trim()

  if (!ten) {
    errors.ten_nguoi_nhan = 'Vui lòng nhập họ tên người nhận'
  }

  if (!phoneRaw) {
    errors.so_dien_thoai = 'Vui lòng nhập số điện thoại'
  } else if (!/^\d{10,11}$/.test(phone)) {
    errors.so_dien_thoai = 'Số điện thoại không hợp lệ (10-11 chữ số)'
  }

  if (!addr) {
    errors.dia_chi = 'Vui lòng nhập địa chỉ chi tiết'
  }

  return !errors.ten_nguoi_nhan && !errors.so_dien_thoai && !errors.dia_chi
}

function normalizePayload(payload) {
  const ten_nguoi_nhan = (payload.ten_nguoi_nhan ?? '').trim()
  const so_dien_thoai = (payload.so_dien_thoai ?? '').trim().replace(/\s+/g, '')
  const dia_chi = (payload.dia_chi ?? '').trim()
  return {
    ...payload,
    ten_nguoi_nhan,
    so_dien_thoai,
    dia_chi,
  }
}

async function fetchAddresses() {
  loading.value = true
  try {
    const res = await api.get('/addresses')
    addresses.value = res.data
  } catch (e) {
    showError('Không thể tải danh sách địa chỉ')
  } finally {
    loading.value = false
  }
}

function openAdd() {
  editingAddr.value = null
  resetForm()
  showModal.value = true
}

function openEdit(addr) {
  editingAddr.value = addr
  errors.ten_nguoi_nhan = ''
  errors.so_dien_thoai = ''
  errors.dia_chi = ''

  form.ten_nguoi_nhan = addr.ten_nguoi_nhan
  form.so_dien_thoai = addr.so_dien_thoai
  form.dia_chi = addr.dia_chi
  form.la_mac_dinh = addr.la_mac_dinh

  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function saveAddress() {
  if (saving.value) return
  if (!validateForm()) return

  saving.value = true
  try {
    const payload = normalizePayload({ ...form })

    if (editingAddr.value) {
      await api.put(`/addresses/${editingAddr.value.id}`, payload)
      success('Đã cập nhật địa chỉ')
    } else {
      await api.post('/addresses', payload)
      success('Đã thêm địa chỉ mới')
    }

    closeModal()
    fetchAddresses()
  } catch (e) {
    showError('Lỗi khi lưu địa chỉ')
  } finally {
    saving.value = false
  }
}

async function setDefault(addr) {
  try {
    await api.post(`/addresses/${addr.id}/set-default`)
    success('Đã thiết lập địa chỉ mặc định')
    fetchAddresses()
  } catch (e) {
    showError('Lỗi khi thiết lập mặc định')
  }
}

async function deleteAddress(addr) {
  if (!confirm('Bạn có chắc chắn muốn xóa địa chỉ này?')) return
  try {
    await api.delete(`/addresses/${addr.id}`)
    success('Đã xóa địa chỉ')
    fetchAddresses()
  } catch (e) {
    showError('Lỗi khi xóa địa chỉ')
  }
}

onMounted(fetchAddresses)
</script>

<style scoped>
/* Giữ lại style cho modal fade và các hiệu ứng */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .relative.bg-white,
.modal-fade-leave-to .relative.bg-white {
  transform: scale(0.96) translateY(10px);
}
</style>