<template>
  <div class="animate-fade-in">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-24 pt-10">
      <!-- Premium Hero -->
      <div class="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-gray-900 to-black px-6 sm:px-10 py-10">
        <div
          class="absolute inset-0 opacity-20"
          style="background-image: radial-gradient(circle at 20% 10%, #e8191a 0%, transparent 45%), radial-gradient(circle at 80% 30%, rgba(255,64,64,.8) 0%, transparent 55%);"
        />
        <div class="relative z-10 flex flex-col md:flex-row md:items-center md:justify-between gap-8">
          <div class="flex items-center gap-6">
            <div class="relative group">
              <button
                type="button"
                class="w-20 h-20 sm:w-24 sm:h-24 rounded-2xl bg-white/5 backdrop-blur border border-white/10 flex items-center justify-center text-white text-3xl font-light shadow-2xl overflow-hidden relative hover:opacity-95"
                @click="triggerAvatarPicker"
                :disabled="avatarUploading"
              >
                <img
                  v-if="authStore.user?.anh_dai_dien"
                  :src="avatarSrc"
                  alt="Avatar"
                  class="absolute inset-0 w-full h-full object-cover"
                  @error="onAvatarImgError"
                />

                <span v-else class="relative z-10">{{ getInitials(authStore.user?.ho_ten) }}</span>
                <div class="absolute inset-0 bg-red-600 opacity-0 group-hover:opacity-25 transition-opacity duration-500" />
              </button>

              <div class="absolute -bottom-2 -right-2 w-9 h-9 rounded-2xl bg-white shadow-xl flex items-center justify-center border border-gray-100">
                <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                    stroke-width="2"
                  />
                  <path d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" stroke-width="2" />
                </svg>
              </div>

              <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleAvatarSelected"
              />
            </div>

            <div>
              <div class="flex items-center gap-3">
                <h1 class="text-3xl font-light text-white tracking-tight">{{ authStore.user?.ho_ten || 'Tài khoản' }}</h1>
                <span class="px-3 py-1 bg-white/10 border border-white/15 text-white text-[10px] font-bold uppercase tracking-widest rounded-full">
                  Verified
                </span>
              </div>
              <p class="text-white/70 font-medium text-sm tracking-wide mt-2">{{ authStore.user?.email }}</p>
              <div class="flex flex-wrap items-center gap-3 mt-4">
                <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-white/80 text-[11px] font-bold uppercase tracking-wider">
                  <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  Tài khoản đang hoạt động
                </span>
                <span class="inline-flex items-center px-3 py-1.5 rounded-full bg-red-500/15 border border-red-500/25 text-red-100 text-[11px] font-bold uppercase tracking-wider">
                  {{ authStore.isAdmin ? 'Admin' : 'Premium Member' }}
                </span>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <button
              @click="updateProfile"
              :disabled="loading"
              class="btn-primary inline-flex items-center justify-center disabled:opacity-60 disabled:cursor-not-allowed"
            >
              <span v-if="!loading">Lưu hồ sơ</span>
              <span v-else class="inline-flex items-center gap-2">
                <span class="spinner" style="width:14px;height:14px;border-width:2px" />
                Đang lưu...
              </span>
            </button>
          </div>
        </div>
      </div>


      <!-- Layout: Cards -->
      <div class="mt-10 grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
        <!-- Left cards -->
        <aside class="space-y-6">
          <div class="glass-card rounded-3xl p-6 sm:p-8 border border-gray-100/60">
            <h3 class="text-[10px] font-bold text-gray-500 uppercase tracking-[0.3em] mb-6">Trạng thái tài khoản</h3>
            <div class="space-y-5">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600 font-medium">Hạng thành viên</span>
                <span class="text-sm font-bold text-gray-900">{{ authStore.isAdmin ? 'Admin' : 'Premium Member' }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600 font-medium">Ngày tham gia</span>
                <span class="text-sm font-bold text-gray-900">May 2026</span>
              </div>
              <div class="pt-4 border-t border-gray-100 flex items-center gap-4">
                <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                <span class="text-xs text-gray-500 font-medium uppercase tracking-widest">Tài khoản đang hoạt động</span>
              </div>
            </div>
          </div>

          <div class="rounded-3xl overflow-hidden border border-red-200/50 shadow-xl shadow-red-200/30 bg-gradient-to-br from-red-700 via-red-600 to-red-500 text-white relative">
            <div class="absolute -right-10 -bottom-10 w-52 h-52 bg-white/10 rounded-full blur-2xl" />
            <div class="relative p-6 sm:p-8">
              <div class="flex items-start justify-between gap-4">
                <div>
                  <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/15 text-white/90 text-[11px] font-bold uppercase tracking-widest">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3 3-7z" />
                    </svg>
                    Ưu đãi đặc quyền
                  </div>
                  <h4 class="font-bold text-lg mt-4">Cập nhật để nhận deal mới</h4>
                  <p class="text-white/80 text-xs leading-relaxed mt-2">Nhận thông báo về các bộ sưu tập giới hạn và voucher dành riêng cho Premium.</p>
                </div>
                <div class="hidden sm:block w-10 h-10 rounded-2xl bg-white/10 border border-white/15 flex items-center justify-center">
                  <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2l8 4v6c0 5-3 9-8 10-5-1-8-5-8-10V6l8-4z" />
                  </svg>
                </div>
              </div>
              <button class="mt-6 btn-outline" type="button">Xem chi tiết</button>
            </div>
          </div>
        </aside>

        <!-- Main content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Personal info -->
          <section class="glass-card rounded-3xl p-6 sm:p-8 border border-gray-100/60">
            <header class="flex items-center gap-3 mb-6">
              <span class="text-2xl">👤</span>
              <div>
                <h2 class="text-xl font-bold text-gray-900 tracking-tight">Thông tin cá nhân</h2>
                <p class="text-sm text-gray-500 mt-1">Đảm bảo thông tin đúng để nhận hàng nhanh hơn.</p>
              </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Họ và tên</label>
                <input v-model="profileForm.ho_ten" class="input-field" placeholder="Nguyễn Văn A" />
              </div>

              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Số điện thoại</label>
                <input v-model="profileForm.so_dien_thoai" class="input-field" placeholder="032xxxxxxx" />
              </div>

              <div class="md:col-span-2">
                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Địa chỉ giao hàng mặc định</label>
                <input v-model="profileForm.dia_chi" class="input-field" placeholder="Số nhà, tên đường..." />
              </div>
            </div>
          </section>

          <!-- Security -->
          <section class="glass-card rounded-3xl p-6 sm:p-8 border border-gray-100/60">
            <header class="flex items-center gap-3 mb-6">
              <span class="text-2xl">🔒</span>
              <div>
                <h2 class="text-xl font-bold text-gray-900 tracking-tight">Bảo mật tài khoản</h2>
                <p class="text-sm text-gray-500 mt-1">Cập nhật mật khẩu để tăng cường an toàn.</p>
              </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Mật khẩu hiện tại</label>
                <input v-model="pwForm.mat_khau_hien_tai" type="password" class="input-field" placeholder="••••••••" />
              </div>

              <div>
                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Mật khẩu mới</label>
                <input v-model="pwForm.mat_khau_moi" type="password" class="input-field" placeholder="••••••••" />
              </div>

              <div class="md:col-span-2 pt-2">
                <button
                  @click="changePassword"
                  :disabled="!pwForm.mat_khau_hien_tai || !pwForm.mat_khau_moi"
                  class="btn-outline inline-flex items-center justify-center disabled:opacity-60 disabled:cursor-not-allowed"
                  type="button"
                >
                  Cập nhật mật khẩu
                </button>
              </div>
            </div>
          </section>

          <!-- Danger zone -->
          <section class="rounded-3xl p-6 sm:p-8 border border-red-100/60 bg-red-50/40">
            <header class="flex items-center gap-3 mb-4">
              <span class="text-2xl">⚠️</span>
              <div>
                <h4 class="text-red-700 font-bold text-sm uppercase tracking-wider">Vùng nguy hiểm</h4>
                <p class="text-red-800/70 text-xs mt-1">Xóa tài khoản sẽ loại bỏ toàn bộ lịch sử đơn hàng và thông tin cá nhân. Thao tác này không thể hoàn tác.</p>
              </div>
            </header>

            <button
              class="mt-6 text-[10px] font-black uppercase tracking-widest text-red-700 hover:text-red-800 underline underline-offset-4"
              type="button"
            >
              Yêu cầu xóa tài khoản
            </button>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { reactive, onMounted, ref, computed } from 'vue'

import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const authStore = useAuthStore()
const { success, error: showError } = useToast()
const loading = ref(false)
const avatarUploading = ref(false)
const avatarInput = ref(null)

const avatarSrc = computed(() => {
  const v = authStore.user?.anh_dai_dien
  if (!v) return ''
  if (typeof v === 'string' && v.startsWith('data:')) return v
  // backend đang lưu base64 thuần
  return `data:image/*;base64,${v}`
})


const profileForm = reactive({
  ho_ten: '',
  so_dien_thoai: '',
  dia_chi: ''
})

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const pwForm = reactive({
  mat_khau_hien_tai: '',
  mat_khau_moi: ''
})

onMounted(() => {
  profileForm.ho_ten = authStore.user?.ho_ten || ''
  profileForm.so_dien_thoai = authStore.user?.so_dien_thoai || ''
  profileForm.dia_chi = authStore.user?.dia_chi || ''
})

function triggerAvatarPicker() {
  avatarInput.value?.click()
}

function onAvatarImgError() {
  // img lỗi thì chỉ bỏ hiển thị, không block upload
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = (e) => reject(e)
    reader.readAsDataURL(file)
  })
}

async function handleAvatarSelected(e) {
  const file = e.target?.files?.[0]
  if (!file) return

  // backend đang nhận base64 thuần (không nhất thiết prefix data:)
  // FileReader trả về dạng data:image/...;base64,XXXX
  try {
    avatarUploading.value = true
    const dataUrl = await fileToBase64(file)
    const base64 = typeof dataUrl === 'string' ? dataUrl.split(',')[1] : null
    if (!base64) throw new Error('Không đọc được dữ liệu ảnh')

    const res = await api.put('/users/me/avatar', { avatar: base64 })
    // backend trả về user (có anh_dai_dien) => update store để ảnh đổi ngay
    authStore.updateUser(res.data)

    // đảm bảo avatarInput được reset để lần chọn lại ảnh cùng file vẫn trigger change

    success('Cập nhật avatar thành công')
  } catch (err) {
    showError(err?.response?.data?.detail || err?.message || 'Lỗi cập nhật avatar')
  } finally {
    avatarUploading.value = false
    if (avatarInput.value) avatarInput.value.value = ''
  }
}

async function updateProfile() {

  loading.value = true
  try {
    const res = await api.put('/users/me', profileForm)
    authStore.updateUser(res.data)
    success('Hồ sơ của bạn đã được cập nhật')
  } catch (e) {
    showError(e.response?.data?.detail || 'Lỗi cập nhật hồ sơ')
  } finally {
    loading.value = false
  }
}

async function changePassword() {
  if (!pwForm.mat_khau_hien_tai || !pwForm.mat_khau_moi) {
    showError('Vui lòng điền đủ thông tin mật khẩu')
    return
  }
  try {
    await api.put('/users/me/password', pwForm)
    success('Mật khẩu đã được thay đổi')
    pwForm.mat_khau_hien_tai = ''
    pwForm.mat_khau_moi = ''
  } catch (e) {
    showError(e.response?.data?.detail || 'Lỗi đổi mật khẩu')
  }
}
</script>

<style scoped>
@reference "../../assets/main.css";

.animate-fade-in {
  animation: fadeIn 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

input:focus + label,
input:not(:placeholder-shown) + label {
  color: #e8191a;
}
</style>
