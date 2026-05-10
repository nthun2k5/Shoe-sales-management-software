<template>
  <div class="space-y-8 animate-fade-in pb-20">
    <div>
      <h2 class="text-2xl font-bold text-gray-900">Tài khoản nhận thanh toán</h2>
      <p class="text-sm text-gray-500 mt-1">Cấu hình thông tin nhận tiền duy nhất cho từng phương thức</p>
    </div>

    <!-- Configuration Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Bank Transfer Card -->
      <div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500 flex flex-col h-full relative overflow-hidden group">
        <div class="absolute top-0 right-0 w-32 h-32 bg-blue-500/5 rounded-full -mr-16 -mt-16 blur-2xl group-hover:bg-blue-500/10 transition-all"></div>
        
        <div class="flex items-center gap-4 mb-6">
          <div class="w-14 h-14 rounded-2xl bg-blue-50 flex items-center justify-center text-blue-600 shadow-sm">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/></svg>
          </div>
          <div>
            <h3 class="font-bold text-gray-900">Chuyển khoản</h3>
            <p class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Ngân hàng / VietQR</p>
          </div>
        </div>

        <div v-if="bankAccount" class="flex-1 space-y-4">
          <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100">
            <p class="text-[10px] text-gray-400 uppercase font-bold mb-1">Số tài khoản</p>
            <p class="text-lg font-bold text-primary-600 tracking-wider">{{ bankAccount.so_tai_khoan }}</p>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <p class="text-[10px] text-gray-400 uppercase font-bold">Ngân hàng</p>
              <p class="text-xs font-bold text-gray-700">{{ bankAccount.ten_ngan_hang }} ({{ bankAccount.ma_ngan_hang }})</p>
            </div>
            <div>
              <p class="text-[10px] text-gray-400 uppercase font-bold">Chủ tài khoản</p>
              <p class="text-xs font-bold text-gray-700 uppercase">{{ bankAccount.chu_tai_khoan }}</p>
            </div>
          </div>
        </div>
        <div v-else class="flex-1 flex flex-col items-center justify-center py-10 text-gray-300">
          <svg class="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
          <p class="text-xs font-bold uppercase">Chưa cấu hình</p>
        </div>

        <div class="mt-8 pt-6 border-t border-gray-50 flex items-center gap-3">
          <button @click="openEdit('ngan_hang')" 
            class="flex-1 py-3 bg-gray-900 text-white rounded-xl text-xs font-bold hover:bg-black transition-all shadow-lg shadow-gray-200">
            {{ bankAccount ? 'CẬP NHẬT' : 'THIẾT LẬP' }}
          </button>
          <button v-if="bankAccount" @click="toggleAccount(bankAccount)"
            :class="['w-12 h-11 rounded-xl flex items-center justify-center transition-all', bankAccount.dang_su_dung ? 'bg-green-50 text-green-600' : 'bg-gray-100 text-gray-400']">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          </button>
        </div>
      </div>

      <!-- MoMo Card -->
      <div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500 flex flex-col h-full relative overflow-hidden group">
        <div class="absolute top-0 right-0 w-32 h-32 bg-pink-500/5 rounded-full -mr-16 -mt-16 blur-2xl group-hover:bg-pink-500/10 transition-all"></div>
        
        <div class="flex items-center gap-4 mb-6">
          <div class="w-14 h-14 rounded-2xl bg-pink-50 flex items-center justify-center text-pink-600 shadow-sm">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
          </div>
          <div>
            <h3 class="font-bold text-gray-900">Ví MoMo</h3>
            <p class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Mobile Wallet</p>
          </div>
        </div>

        <div v-if="momoAccount" class="flex-1 space-y-4">
          <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100">
            <p class="text-[10px] text-gray-400 uppercase font-bold mb-1">Số điện thoại</p>
            <p class="text-lg font-bold text-pink-600 tracking-wider">{{ momoAccount.so_dien_thoai }}</p>
          </div>
          <div>
            <p class="text-[10px] text-gray-400 uppercase font-bold">Chủ tài khoản</p>
            <p class="text-xs font-bold text-gray-700 uppercase">{{ momoAccount.chu_tai_khoan || 'Chưa cập nhật' }}</p>
          </div>
        </div>
        <div v-else class="flex-1 flex flex-col items-center justify-center py-10 text-gray-300">
          <svg class="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
          <p class="text-xs font-bold uppercase">Chưa cấu hình</p>
        </div>

        <div class="mt-8 pt-6 border-t border-gray-50 flex items-center gap-3">
          <button @click="openEdit('vi_momo')" 
            class="flex-1 py-3 bg-gray-900 text-white rounded-xl text-xs font-bold hover:bg-black transition-all shadow-lg shadow-gray-200">
            {{ momoAccount ? 'CẬP NHẬT' : 'THIẾT LẬP' }}
          </button>
          <button v-if="momoAccount" @click="toggleAccount(momoAccount)"
            :class="['w-12 h-11 rounded-xl flex items-center justify-center transition-all', momoAccount.dang_su_dung ? 'bg-green-50 text-green-600' : 'bg-gray-100 text-gray-400']">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          </button>
        </div>
      </div>

      <!-- ZaloPay Card -->
      <div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500 flex flex-col h-full relative overflow-hidden group">
        <div class="absolute top-0 right-0 w-32 h-32 bg-green-500/5 rounded-full -mr-16 -mt-16 blur-2xl group-hover:bg-green-500/10 transition-all"></div>
        
        <div class="flex items-center gap-4 mb-6">
          <div class="w-14 h-14 rounded-2xl bg-green-50 flex items-center justify-center text-green-600 shadow-sm">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div>
            <h3 class="font-bold text-gray-900">Ví ZaloPay</h3>
            <p class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Mobile Wallet</p>
          </div>
        </div>

        <div v-if="zalopayAccount" class="flex-1 space-y-4">
          <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100">
            <p class="text-[10px] text-gray-400 uppercase font-bold mb-1">Số điện thoại</p>
            <p class="text-lg font-bold text-green-600 tracking-wider">{{ zalopayAccount.so_dien_thoai }}</p>
          </div>
          <div>
            <p class="text-[10px] text-gray-400 uppercase font-bold">Chủ tài khoản</p>
            <p class="text-xs font-bold text-gray-700 uppercase">{{ zalopayAccount.chu_tai_khoan || 'Chưa cập nhật' }}</p>
          </div>
        </div>
        <div v-else class="flex-1 flex flex-col items-center justify-center py-10 text-gray-300">
          <svg class="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
          <p class="text-xs font-bold uppercase">Chưa cấu hình</p>
        </div>

        <div class="mt-8 pt-6 border-t border-gray-50 flex items-center gap-3">
          <button @click="openEdit('vi_zalopay')" 
            class="flex-1 py-3 bg-gray-900 text-white rounded-xl text-xs font-bold hover:bg-black transition-all shadow-lg shadow-gray-200">
            {{ zalopayAccount ? 'CẬP NHẬT' : 'THIẾT LẬP' }}
          </button>
          <button v-if="zalopayAccount" @click="toggleAccount(zalopayAccount)"
            :class="['w-12 h-11 rounded-xl flex items-center justify-center transition-all', zalopayAccount.dang_su_dung ? 'bg-green-50 text-green-600' : 'bg-gray-100 text-gray-400']">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          </button>
        </div>
      </div>

      <!-- COD Card -->
      <div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500 flex flex-col h-full relative overflow-hidden group">
        <div class="absolute top-0 right-0 w-32 h-32 bg-gray-500/5 rounded-full -mr-16 -mt-16 blur-2xl group-hover:bg-gray-500/10 transition-all"></div>
        
        <div class="flex items-center gap-4 mb-6">
          <div class="w-14 h-14 rounded-2xl bg-gray-50 flex items-center justify-center text-gray-600 shadow-sm">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
          </div>
          <div>
            <h3 class="font-bold text-gray-900">Thanh toán COD</h3>
            <p class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Cash on Delivery</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center justify-center py-6 text-center">
          <div :class="['px-4 py-2 rounded-full text-[10px] font-bold uppercase mb-2', codAccount?.dang_su_dung ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400']">
            {{ codAccount?.dang_su_dung ? 'ĐANG HOẠT ĐỘNG' : 'ĐANG TẮT' }}
          </div>
          <p class="text-xs text-gray-500 max-w-[200px]">
            Cho phép khách hàng thanh toán bằng tiền mặt khi nhận hàng.
          </p>
        </div>

        <div class="mt-8 pt-6 border-t border-gray-50 flex items-center gap-3">
          <button @click="toggleCOD" 
            :class="['flex-1 py-3 rounded-xl text-xs font-bold transition-all shadow-lg', 
              codAccount?.dang_su_dung ? 'bg-red-50 text-red-600 hover:bg-red-100 shadow-red-100' : 'bg-green-600 text-white hover:bg-green-700 shadow-green-100']">
            {{ codAccount?.dang_su_dung ? 'TẮT PHƯƠNG THỨC' : 'KÍCH HOẠT COD' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" @click.self="closeModal">
        <div class="bg-white rounded-3xl w-full max-w-md shadow-2xl overflow-hidden animate-scale-up">
          <div class="p-6 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-gray-900">{{ editingTypeLabel }}</h3>
              <p class="text-[10px] text-gray-500 uppercase font-bold mt-0.5">Cấu hình thông tin nhận tiền</p>
            </div>
            <button @click="closeModal" class="p-2 text-gray-400 hover:text-gray-900 hover:bg-white rounded-full transition-all">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>
          
          <form @submit.prevent="saveAccount" class="p-6 space-y-6">
            <!-- Bank fields -->
            <template v-if="currentEditingType === 'ngan_hang'">
              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase mb-2">Tên ngân hàng *</label>
                <input v-model="form.ten_ngan_hang" class="modern-input" placeholder="Ví dụ: Vietcombank" required />
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-[10px] font-bold text-gray-400 uppercase mb-2">Mã VietQR *</label>
                  <input v-model="form.ma_ngan_hang" class="modern-input font-mono" placeholder="VCB" required />
                </div>
                <div>
                  <label class="block text-[10px] font-bold text-gray-400 uppercase mb-2">Chi nhánh</label>
                  <input v-model="form.chi_nhanh" class="modern-input" placeholder="Hồ Chí Minh" />
                </div>
              </div>
              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase mb-2">Số tài khoản *</label>
                <input v-model="form.so_tai_khoan" class="modern-input text-lg font-bold tracking-wider" placeholder="1234567890" required />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase mb-2">Chủ tài khoản *</label>
                <input v-model="form.chu_tai_khoan" class="modern-input uppercase" placeholder="NGUYEN VAN A" required />
              </div>
            </template>

            <!-- Wallet fields -->
            <template v-else>
              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase mb-2">Số điện thoại đăng ký *</label>
                <input v-model="form.so_dien_thoai" class="modern-input text-lg font-bold tracking-wider" placeholder="0901234567" required />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase mb-2">Họ tên chủ ví *</label>
                <input v-model="form.chu_tai_khoan" class="modern-input uppercase" placeholder="NGUYEN VAN A" required />
              </div>
            </template>

            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-100">
              <div>
                <p class="text-sm font-bold text-gray-900">Kích hoạt phương thức</p>
                <p class="text-[10px] text-gray-500 uppercase font-bold mt-0.5">Cho phép khách hàng sử dụng</p>
              </div>
              <button type="button" @click="form.dang_su_dung = !form.dang_su_dung"
                :class="['relative w-12 h-7 rounded-full transition-all duration-300', form.dang_su_dung ? 'bg-green-500' : 'bg-gray-200']">
                <span :class="['absolute top-1 left-1 w-5 h-5 bg-white rounded-full shadow-md transition-transform duration-300', form.dang_su_dung ? 'translate-x-5' : 'translate-x-0']"></span>
              </button>
            </div>

            <div class="flex gap-3 pt-2">
              <button type="button" @click="closeModal" class="flex-1 px-6 py-3 border border-gray-200 rounded-xl text-xs font-bold text-gray-700 hover:bg-gray-50 transition-all">HỦY</button>
              <button type="submit" :disabled="saving" class="flex-1 px-6 py-3 bg-primary-600 text-white rounded-xl text-xs font-bold hover:bg-primary-700 transition-all shadow-xl shadow-primary-500/20 disabled:opacity-50">
                {{ saving ? 'ĐANG LƯU...' : 'LƯU CẤU HÌNH' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import api from '@/services/api'
import apiPublic from '@/services/apiPublic'

const { success, error: showError } = useToast()

const accounts = ref([])
const loading = ref(true)
const saving = ref(false)
const showModal = ref(false)
const currentEditingType = ref('')

const bankAccount = computed(() => accounts.value.find(a => a.loai === 'ngan_hang'))
const momoAccount = computed(() => accounts.value.find(a => a.loai === 'vi_dien_tu' && a.ten_ngan_hang?.toLowerCase().includes('momo')))
const zalopayAccount = computed(() => accounts.value.find(a => a.loai === 'vi_dien_tu' && a.ten_ngan_hang?.toLowerCase().includes('zalopay')))
const codAccount = computed(() => accounts.value.find(a => a.loai === 'cod'))

const editingTypeLabel = computed(() => {
  if (currentEditingType.value === 'ngan_hang') return 'Tài khoản Ngân hàng'
  if (currentEditingType.value === 'vi_momo') return 'Ví MoMo'
  if (currentEditingType.value === 'vi_zalopay') return 'Ví ZaloPay'
  return ''
})

const form = reactive({
  loai: 'ngan_hang',
  ten_ngan_hang: '',
  ma_ngan_hang: '',
  chu_tai_khoan: '',
  so_tai_khoan: '',
  so_dien_thoai: '',
  chi_nhanh: '',
  dang_su_dung: true,
})

async function fetchAccounts() {
  loading.value = true
  try {
    const res = await api.get('/banks')
    accounts.value = res.data
  } catch (e) {
    showError('Không thể tải danh sách tài khoản')
  } finally {
    loading.value = false
  }
}

function openEdit(type) {
  currentEditingType.value = type
  let acc = null
  
  if (type === 'ngan_hang') {
    acc = bankAccount.value
    form.loai = 'ngan_hang'
  } else if (type === 'vi_momo') {
    acc = momoAccount.value
    form.loai = 'vi_dien_tu'
    form.ten_ngan_hang = 'MoMo'
  } else if (type === 'vi_zalopay') {
    acc = zalopayAccount.value
    form.loai = 'vi_dien_tu'
    form.ten_ngan_hang = 'ZaloPay'
  }

  if (acc) {
    form.ten_ngan_hang = acc.ten_ngan_hang
    form.ma_ngan_hang = acc.ma_ngan_hang || ''
    form.chu_tai_khoan = acc.chu_tai_khoan || ''
    form.so_tai_khoan = acc.so_tai_khoan || ''
    form.so_dien_thoai = acc.so_dien_thoai || ''
    form.chi_nhanh = acc.chi_nhanh || ''
    form.dang_su_dung = acc.dang_su_dung
  } else {
    // Reset for new
    if (type === 'ngan_hang') {
      form.ten_ngan_hang = ''
      form.ma_ngan_hang = ''
    }
    form.chu_tai_khoan = ''
    form.so_tai_khoan = ''
    form.so_dien_thoai = ''
    form.chi_nhanh = ''
    form.dang_su_dung = true
  }
  
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function saveAccount() {
  saving.value = true
  try {
    const payload = { ...form }
    let existing = null
    
    if (currentEditingType.value === 'ngan_hang') existing = bankAccount.value
    else if (currentEditingType.value === 'vi_momo') existing = momoAccount.value
    else if (currentEditingType.value === 'vi_zalopay') existing = zalopayAccount.value

    if (existing) {
      await api.put(`/banks/${existing.id}`, payload)
      success('Đã cập nhật thông tin')
    } else {
      await api.post('/banks', payload)
      success('Đã lưu thông tin mới')
    }
    closeModal()
    await fetchAccounts()
  } catch (e) {
    showError(e.response?.data?.detail || 'Lỗi khi lưu')
  } finally {
    saving.value = false
  }
}

async function toggleAccount(acc) {
  try {
    await api.put(`/banks/${acc.id}`, { dang_su_dung: !acc.dang_su_dung })
    acc.dang_su_dung = !acc.dang_su_dung
    success(acc.dang_su_dung ? 'Đã bật' : 'Đã tắt')
  } catch (e) {
    showError('Cập nhật thất bại')
  }
}

async function toggleCOD() {
  try {
    if (codAccount.value) {
      await api.put(`/banks/${codAccount.value.id}`, { dang_su_dung: !codAccount.value.dang_su_dung })
      await fetchAccounts()
      success(codAccount.value.dang_su_dung ? 'Đã bật COD' : 'Đã tắt COD')
    } else {
      await api.post('/banks', {
        loai: 'cod',
        ten_ngan_hang: 'COD',
        dang_su_dung: true
      })
      await fetchAccounts()
      success('Đã kích hoạt COD')
    }
  } catch (e) {
    showError('Cập nhật COD thất bại')
  }
}

onMounted(fetchAccounts)
</script>

<style scoped>
.modern-input {
  width: 100%;
  background-color: #f9fafb;
  border: 1px solid #f3f4f6;
  border-radius: 1rem;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: #111827;
  transition: all 0.2s;
  outline: none;
  font-weight: 500;
}

.modern-input:focus {
  background-color: white;
  border-color: #ef4444;
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.05);
}

.modern-input::placeholder {
  color: #d1d5db;
}

.animate-scale-up {
  animation: scale-up 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes scale-up {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
</style>
