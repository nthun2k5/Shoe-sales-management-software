<template>
  <div class="min-h-screen flex items-center justify-center p-4" style="background:linear-gradient(135deg,#f5f5f5,#fff1f1)">
    <div class="w-full max-w-md animate-fade-in">
      <div class="text-center mb-8">
        <RouterLink to="/" class="inline-flex items-center gap-3 group">
          <div class="relative w-12 h-12 flex items-center justify-center shrink-0">
            <div class="absolute inset-0 bg-red-600 rounded-xl rotate-6 group-hover:rotate-12 transition-transform duration-500"></div>
            <div class="absolute inset-0 bg-black rounded-xl -rotate-3 group-hover:rotate-0 transition-transform duration-500"></div>
            <svg class="relative w-7 h-7 text-white transform -rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </div>
          <div class="flex flex-col text-left leading-none">
            <span class="font-black text-xl tracking-tighter text-gray-900">
              GIÀY<span style="color:#e8191a">ĐẸP</span>
            </span>
            <span class="text-[10px] font-black uppercase tracking-[0.3em] text-gray-400 mt-1">Premium Store</span>
          </div>
        </RouterLink>
        <h1 class="text-2xl font-black text-gray-900 mt-6">Tạo tài khoản</h1>
        <p class="text-gray-500 mt-1 text-sm">Tham gia Giày Đẹp Store ngay hôm nay</p>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Họ và tên *</label>
            <input v-model="form.full_name" type="text" required class="input-field" placeholder="Nguyễn Văn A" />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Email *</label>
            <input v-model="form.email" type="email" required class="input-field" placeholder="email@example.com" />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Số điện thoại</label>
            <input v-model="form.phone" type="tel" class="input-field" placeholder="0912 345 678" />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Mật khẩu *</label>
            <div class="relative">
              <input v-model="form.password" :type="showPw ? 'text' : 'password'" required
                class="input-field pr-10" placeholder="Tối thiểu 6 ký tự" minlength="6" />
              <button type="button" @click="showPw = !showPw"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                <svg v-if="!showPw" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
              </button>
            </div>
          </div>

          <div v-if="errorMsg" class="flex items-center gap-2 text-red-600 text-sm bg-red-50 px-4 py-3 rounded-lg border border-red-100">
            <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            {{ errorMsg }}
          </div>

          <button type="submit" :disabled="loading"
            class="w-full py-3 text-sm font-bold text-white rounded transition-all flex items-center justify-center gap-2 disabled:opacity-70"
            style="background:#e8191a"
            @mouseenter="e=>!loading&&(e.target.style.background='#c9111b')"
            @mouseleave="e=>e.target.style.background='#e8191a'">
            <span v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            {{ loading ? 'Đang tạo tài khoản...' : 'Đăng ký ngay' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-500">
            Đã có tài khoản?
            <RouterLink to="/login" class="font-bold hover:underline" style="color:#e8191a">Đăng nhập</RouterLink>
          </p>
        </div>
      </div>

      <p class="text-center text-xs text-gray-400 mt-6">
        Bằng cách đăng ký, bạn đồng ý với
        <RouterLink to="/dieu-khoan" class="underline hover:text-gray-600">Điều khoản sử dụng</RouterLink>
        và
        <RouterLink to="/chinh-sach-bao-mat" class="underline hover:text-gray-600">Chính sách bảo mật</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const form = reactive({ full_name: '', email: '', phone: '', password: '' })
const loading = ref(false)
const errorMsg = ref('')
const showPw = ref(false)

async function handleRegister() {
  loading.value = true
  errorMsg.value = ''
  try {
    await authStore.register(form)
    router.push('/')
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Đăng ký thất bại. Vui lòng thử lại.'
  } finally {
    loading.value = false
  }
}
</script>
