<template>
  <div class="contact-page">
    <!-- Hero Section với hiệu ứng nền chuyển động -->
    <div class="hero-section">
      <div class="hero-bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex items-center gap-2 text-sm mb-4 text-white/70" data-aos="fade-right" data-aos-duration="400">
          <RouterLink to="/" class="hover:text-white transition-colors">Trang chủ</RouterLink>
          <span>/</span>
          <span class="text-[#e8191a] font-medium">Liên hệ</span>
        </div>
        <div class="max-w-2xl">
          <h1 class="text-4xl md:text-5xl font-black text-white leading-tight" data-aos="fade-up" data-aos-duration="600">
            Liên hệ <span class="text-gradient">hỗ trợ</span>
          </h1>
          <p class="mt-4 text-white/80 text-lg" data-aos="fade-up" data-aos-delay="100" data-aos-duration="600">Đội ngũ của chúng tôi luôn sẵn sàng giải đáp mọi thắc mắc — nhanh chóng, tận tâm.</p>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Thông tin liên hệ dạng thẻ nổi -->
        <div class="space-y-5">
          <div class="flex items-center gap-2 mb-2" data-aos="fade-right">
            <span class="text-xs font-semibold text-gray-400 tracking-wider">THÔNG TIN</span>
            <div class="h-px flex-1 bg-gradient-to-r from-gray-200 to-transparent"></div>
          </div>
          <div
            v-for="(item, idx) in contactInfos"
            :key="item.title"
            class="contact-card group bg-white rounded-2xl p-5 shadow-sm border border-gray-100 transition-all duration-300 hover:shadow-xl hover:border-red-100"
            :style="{ transitionDelay: `${idx * 50}ms` }"
            data-aos="fade-right" :data-aos-delay="idx * 50"
          >
            <div class="flex gap-4">
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-red-50 to-orange-50 flex items-center justify-center text-2xl shrink-0 group-hover:scale-110 transition-transform duration-300">
                {{ item.icon }}
              </div>
              <div>
                <h3 class="font-bold text-gray-800 mb-1">{{ item.title }}</h3>
                <p class="text-sm text-gray-600 leading-relaxed">{{ item.value }}</p>
                <p v-if="item.sub" class="text-xs text-gray-400 mt-1">{{ item.sub }}</p>
              </div>
            </div>
          </div>

          <!-- Bản đồ tương tác đẹp hơn -->
          <div class="mt-5 bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100 transition-all hover:shadow-md" data-aos="zoom-in" data-aos-duration="800">
            <div class="relative h-52 bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
              <div class="text-center relative z-10">
                <div class="text-5xl mb-2 drop-shadow-md">📍</div>
                <p class="text-sm font-medium text-gray-700">123 Đường Giày Đẹp, Q.1, TP.HCM</p>
                <p class="text-xs text-gray-400 mt-1">Xem trên Google Maps →</p>
              </div>
              <div class="absolute inset-0 opacity-10 bg-repeat map-pattern"></div>
            </div>
          </div>
        </div>

        <!-- Form liên hệ thiết kế mới -->
        <div class="lg:col-span-2" data-aos="fade-left" data-aos-duration="600">
          <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
            <div class="bg-gradient-to-r from-gray-50 to-white px-6 py-5 border-b border-gray-100">
              <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
                <span class="w-1 h-6 bg-[#e8191a] rounded-full"></span>
                Gửi tin nhắn cho chúng tôi
              </h2>
              <p class="text-xs text-gray-400 mt-1">Phản hồi trong vòng 2 giờ làm việc</p>
            </div>

            <div class="p-6 md:p-8">
              <div v-if="submitted" class="text-center py-8 animate-fadeIn">
                <div class="w-20 h-20 rounded-full bg-green-50 flex items-center justify-center mx-auto mb-5">
                  <svg class="w-10 h-10 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                </div>
                <h3 class="font-bold text-gray-800 text-xl mb-2">Gửi thành công!</h3>
                <p class="text-gray-500 text-sm max-w-sm mx-auto">Cảm ơn bạn đã liên hệ. Chúng tôi sẽ phản hồi sớm nhất có thể.</p>
                <button @click="resetForm" class="mt-6 btn-primary text-sm py-2.5 px-6">Gửi tin nhắn mới</button>
              </div>

              <form v-else @submit.prevent="handleSubmit" class="space-y-5">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <div class="input-group">
                    <label class="form-label">Họ và tên <span class="text-red-500">*</span></label>
                    <input v-model="form.name" type="text" required placeholder="Nguyễn Văn A" class="form-input" />
                  </div>
                  <div class="input-group">
                    <label class="form-label">Email <span class="text-red-500">*</span></label>
                    <input v-model="form.email" type="email" required placeholder="hello@example.com" class="form-input" />
                  </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <div class="input-group">
                    <label class="form-label">Số điện thoại</label>
                    <input v-model="form.phone" type="tel" placeholder="0123 456 789" class="form-input" />
                  </div>
                  <div class="input-group">
                    <label class="form-label">Chủ đề <span class="text-red-500">*</span></label>
                    <select v-model="form.subject" required class="form-select">
                      <option value="" disabled>-- Chọn chủ đề --</option>
                      <option value="order">📦 Đơn hàng / Vận chuyển</option>
                      <option value="return">🔄 Đổi trả sản phẩm</option>
                      <option value="product">👟 Tư vấn sản phẩm</option>
                      <option value="payment">💳 Thanh toán</option>
                      <option value="other">💬 Khác</option>
                    </select>
                  </div>
                </div>
                <div class="input-group">
                  <label class="form-label">Nội dung <span class="text-red-500">*</span></label>
                  <textarea v-model="form.message" required rows="5" placeholder="Nhập nội dung chi tiết để chúng tôi hỗ trợ tốt hơn..." class="form-input resize-none"></textarea>
                </div>
                <button type="submit" :disabled="sending" class="btn-primary w-full justify-center gap-2 py-3 text-base font-semibold">
                  <svg v-if="sending" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span v-else>Gửi tin nhắn</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Câu hỏi thường gặp nhanh - dạng grid đẹp -->
      <div class="mt-16">
        <div class="flex items-center gap-2 mb-5 justify-center">
          <span class="text-xs font-semibold text-gray-400 tracking-wider">GIẢI ĐÁP NHANH</span>
          <div class="h-px w-8 bg-gradient-to-r from-gray-300 to-transparent"></div>
          <span class="text-xs text-gray-400">Câu hỏi thường gặp</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <RouterLink
            v-for="q in quickFaqs"
            :key="q.label"
            :to="q.to"
            class="quick-faq-card group bg-white rounded-xl p-5 border border-gray-100 hover:border-red-200 hover:shadow-lg transition-all duration-300 flex items-center gap-4"
          >
            <div class="w-12 h-12 rounded-xl bg-red-50 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-200">
              {{ q.icon }}
            </div>
            <div class="flex-1">
              <h4 class="font-bold text-gray-800 group-hover:text-red-600 transition-colors">{{ q.label }}</h4>
              <p class="text-xs text-gray-400">{{ q.sub }}</p>
            </div>
            <svg class="w-5 h-5 text-gray-300 group-hover:text-red-400 transition-all group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { RouterLink } from 'vue-router'

const submitted = ref(false)
const sending = ref(false)

const form = reactive({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const contactInfos = [
  { icon: '📍', title: 'Địa chỉ', value: '123 Đường Giày Đẹp, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh', sub: 'Mở cửa: 8:00 - 21:00 hàng ngày' },
  { icon: '📞', title: 'Hotline', value: '0123 456 789', sub: 'Hỗ trợ 24/7, miễn phí cước gọi' },
  { icon: '✉️', title: 'Email', value: 'support@giaydep.store', sub: 'Phản hồi trong vòng 2-4 giờ' },
  { icon: '💬', title: 'Zalo / Facebook', value: 'Giày Đẹp Store', sub: 'Nhắn tin trực tiếp để được hỗ trợ nhanh nhất' },
]

const quickFaqs = [
  { icon: '📦', label: 'Chính sách đổi trả', sub: 'Đổi trả trong 30 ngày', to: '/chinh-sach-doi-tra' },
  { icon: '📏', label: 'Bảng size giày', sub: 'Tìm size phù hợp', to: '/bang-size-giay' },
  { icon: '❓', label: 'Câu hỏi thường gặp', sub: 'Giải đáp nhanh', to: '/faq' },
]

async function handleSubmit() {
  sending.value = true
  // Giả lập gửi API
  await new Promise(resolve => setTimeout(resolve, 1200))
  sending.value = false
  submitted.value = true
}

function resetForm() {
  submitted.value = false
  Object.assign(form, { name: '', email: '', phone: '', subject: '', message: '' })
}
</script>

<style scoped>
@reference "../../assets/main.css";

.contact-page {
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}

/* Hero Section giống FAQ */
.hero-section {
  position: relative;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
  padding: 4rem 0 5rem 0;
  overflow: hidden;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.hero-bg-shapes {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 0;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.shape-1 {
  width: 40vw;
  height: 40vw;
  background: radial-gradient(circle, #e8191a, transparent);
  top: -20%;
  right: -10%;
  animation: float 20s infinite ease-in-out;
}

.shape-2 {
  width: 30vw;
  height: 30vw;
  background: radial-gradient(circle, #ff4d4d, transparent);
  bottom: -30%;
  left: -10%;
  animation: float 25s infinite reverse;
}

.shape-3 {
  width: 20vw;
  height: 20vw;
  background: radial-gradient(circle, #ff7b7b, transparent);
  top: 40%;
  left: 30%;
  animation: pulse 18s infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  50% { transform: translateY(-30px) translateX(20px); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.1); }
}

.text-gradient {
  background: linear-gradient(135deg, #fff, #ffb3b3);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

/* Contact Cards */
.contact-card {
  transition: all 0.25s ease;
}

.contact-card:hover {
  transform: translateY(-3px);
}

/* Form elements */
.form-label {
  @apply block text-sm font-semibold text-gray-700 mb-1.5;
}

.form-input, .form-select {
  @apply w-full px-4 py-2.5 rounded-xl border border-gray-200 bg-gray-50/50 focus:bg-white focus:ring-2 focus:ring-red-200 focus:border-red-400 transition-all duration-200 text-gray-800 text-sm;
}

.form-input:focus, .form-select:focus {
  outline: none;
}

.form-select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-position: right 0.75rem center;
  background-repeat: no-repeat;
  background-size: 1.25rem;
  appearance: none;
  padding-right: 2.5rem;
}

/* Button */
.btn-primary {
  display: inline-flex;
  align-items: center;
  background: #e8191a;
  color: white;
  font-weight: 700;
  padding: 0.75rem 1.8rem;
  border-radius: 60px;
  transition: all 0.3s;
  box-shadow: 0 8px 20px -6px rgba(232, 25, 26, 0.4);
  border: none;
}

.btn-primary:hover:not(:disabled) {
  background: #c41516;
  transform: translateY(-2px);
  box-shadow: 0 15px 25px -10px rgba(232, 25, 26, 0.5);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Quick FAQ Card */
.quick-faq-card {
  transition: all 0.2s cubic-bezier(0.2, 0, 0, 1);
}

.quick-faq-card:hover {
  transform: translateY(-4px);
}

/* Animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fadeIn {
  animation: fadeIn 0.4s ease-out forwards;
}

.map-pattern {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23e8191a'%3E%3Cpath d='M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z'/%3E%3C/svg%3E");
  background-size: 24px;
}

/* Responsive */
@media (max-width: 640px) {
  .hero-section {
    padding: 2.5rem 0 3rem;
  }
  
  .contact-card {
    padding: 1rem;
  }
  
  .btn-primary {
    padding: 0.7rem 1.5rem;
  }
  
  .quick-faq-card {
    padding: 1rem;
  }
}
</style>