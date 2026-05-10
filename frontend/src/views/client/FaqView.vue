<template>
  <div class="faq-page">
    <!-- Hero Section tối giản nhưng ấn tượng -->
    <div class="hero-section">
      <div class="hero-bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex items-center gap-2 text-sm mb-4 text-white/70" data-aos="fade-right" data-aos-duration="400">
          <RouterLink to="/" class="hover:text-white transition-colors">Trang chủ</RouterLink>
          <span>/</span>
          <span class="text-[#e8191a] font-medium">Câu hỏi thường gặp</span>
        </div>
        <div class="max-w-2xl">
          <h1 class="text-4xl md:text-5xl font-black text-white leading-tight" data-aos="fade-up" data-aos-duration="600">
            Trung tâm <span class="text-gradient">hỗ trợ</span>
          </h1>
          <p class="mt-4 text-white/80 text-lg" data-aos="fade-up" data-aos-delay="100" data-aos-duration="600">Câu trả lời cho mọi thắc mắc — nhanh chóng, chi tiết và dễ hiểu</p>
        </div>
      </div>
    </div>

    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
      <!-- Danh mục nổi bật + bộ lọc -->
      <div class="mb-10" data-aos="fade-up" data-aos-duration="600">
        <div class="flex flex-wrap items-center gap-3 mb-2">
          <span class="text-sm font-semibold text-gray-500 tracking-wide">CHỦ ĐỀ</span>
          <div class="h-px flex-1 bg-gradient-to-r from-gray-200 to-transparent"></div>
        </div>
        <div class="flex flex-wrap gap-2.5 mt-3 category-tabs">
          <button
            v-for="(cat, idx) in categories"
            :key="cat"
            @click="activeCategory = cat"
            class="category-btn group relative px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300"
            :class="activeCategory === cat ? 'active' : 'inactive'"
            data-aos="zoom-in" :data-aos-delay="idx * 50"
          >
            <span>{{ cat }}</span>
            <span class="count-badge" :class="activeCategory === cat ? 'bg-white/20' : 'bg-gray-100'">
              {{ getCategoryCount(cat) }}
            </span>
            <span v-if="activeCategory === cat" class="active-indicator"></span>
          </button>
        </div>
      </div>

      <!-- Danh sách FAQ dạng accordion -->
      <div class="space-y-4">
        <div
          v-for="(faq, i) in filteredFaqs"
          :key="faq.q"
          class="faq-card group rounded-2xl bg-white transition-all duration-300"
          :class="openItem === i ? 'card-open shadow-xl shadow-red-500/5' : 'card-closed shadow-sm hover:shadow-md'"
          data-aos="fade-up" :data-aos-delay="i * 30" data-aos-once="true"
        >
          <button
            @click="toggleItem(i)"
            class="w-full flex items-center justify-between px-6 py-5 text-left transition-colors"
          >
            <div class="flex items-start gap-4 pr-4">
              <div class="flex-shrink-0 mt-0.5">
                <div class="w-6 h-6 rounded-full bg-red-50 flex items-center justify-center text-[#e8191a] text-xs font-bold transition-all duration-200 group-hover:bg-red-100">
                  <svg v-if="openItem !== i" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
                  </svg>
                  <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M20 12H4"/>
                  </svg>
                </div>
              </div>
              <span class="text-gray-800 font-semibold text-base md:text-lg leading-tight transition-colors group-hover:text-[#e8191a]">
                {{ faq.q }}
              </span>
            </div>
            <svg
              class="w-5 h-5 flex-shrink-0 text-gray-400 transition-all duration-300 ml-4"
              :class="openItem === i ? 'rotate-180 text-[#e8191a]' : 'group-hover:text-gray-600'"
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          <div
            v-if="openItem === i"
            class="px-6 pb-6 transition-all duration-300 animate-fadeIn"
          >
            <div class="h-px bg-gradient-to-r from-red-100 via-gray-200 to-transparent mb-5"></div>
            <div class="pl-10 text-gray-600 leading-relaxed text-base answer-content" v-html="faq.a"></div>
          </div>
        </div>
      </div>

      <!-- Empty state nếu không có kết quả -->
      <div v-if="filteredFaqs.length === 0" class="text-center py-16 bg-white rounded-2xl shadow-sm border border-gray-100 mt-8" data-aos="zoom-in">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-xl font-bold text-gray-800">Không tìm thấy câu hỏi</h3>
        <p class="text-gray-500 mt-1">Hãy thử chọn chủ đề khác hoặc liên hệ trực tiếp với chúng tôi</p>
      </div>

      <!-- Khu vực hỗ trợ trực tiếp - nổi bật hơn -->
      <div class="mt-16 relative" data-aos="fade-up" data-aos-duration="800">
        <div class="absolute inset-0 bg-gradient-to-r from-red-50 to-orange-50 rounded-3xl blur-2xl opacity-60"></div>
        <div class="relative bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
          <div class="absolute top-0 right-0 w-64 h-64 bg-red-500/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
          <div class="px-6 py-10 md:p-12 text-center relative z-10">
            <div class="inline-flex items-center justify-center w-16 h-16 bg-red-50 rounded-full text-3xl mb-5 shadow-inner" data-aos="zoom-in" data-aos-delay="200">
              💬
            </div>
            <h3 class="text-2xl md:text-3xl font-black text-gray-900 mb-3" data-aos="fade-up" data-aos-delay="300">Vẫn còn băn khoăn?</h3>
            <p class="text-gray-500 max-w-md mx-auto mb-8" data-aos="fade-up" data-aos-delay="400">
              Đội ngũ chuyên viên của chúng tôi luôn sẵn sàng giải đáp mọi thắc mắc của bạn trong vòng 2 giờ.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center" data-aos="fade-up" data-aos-delay="500">
              <RouterLink to="/lien-he" class="support-btn-primary inline-flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                </svg>
                Gửi câu hỏi ngay
              </RouterLink>
              <a href="tel:0123456789" class="support-btn-outline inline-flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                </svg>
                Gọi hotline 0123 456 789
              </a>
            </div>
            <p class="text-xs text-gray-400 mt-6" data-aos="fade-up" data-aos-delay="600">Thời gian hỗ trợ: 8h00 - 21h00 tất cả các ngày</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { RouterLink } from 'vue-router'
import AOS from 'aos'

const openItem = ref(-1)
const activeCategory = ref('Tất cả')

const toggleItem = (i) => {
  openItem.value = openItem.value === i ? -1 : i
  nextTick(() => {
    AOS.refresh()
  })
}

const categories = ['Tất cả', 'Đặt hàng', 'Vận chuyển', 'Đổi trả', 'Thanh toán', 'Sản phẩm']

const faqs = [
  { category: 'Đặt hàng', q: 'Làm thế nào để đặt hàng?', a: 'Bạn chọn sản phẩm, thêm vào giỏ hàng, sau đó tiến hành thanh toán. Hệ thống sẽ gửi email xác nhận đơn hàng sau khi đặt thành công.' },
  { category: 'Đặt hàng', q: 'Tôi có thể thay đổi hoặc hủy đơn hàng không?', a: 'Bạn có thể hủy đơn hàng trong vòng <strong>2 giờ</strong> sau khi đặt, trước khi đơn được xác nhận. Sau đó vui lòng liên hệ hotline để được hỗ trợ.' },
  { category: 'Đặt hàng', q: 'Tôi cần đăng ký tài khoản để mua hàng không?', a: 'Có, bạn cần đăng ký tài khoản để đặt hàng và theo dõi trạng thái đơn hàng. Việc đăng ký hoàn toàn miễn phí và chỉ mất 1 phút.' },
  { category: 'Vận chuyển', q: 'Thời gian giao hàng là bao lâu?', a: 'Nội thành TP.HCM, Hà Nội: <strong>1-2 ngày</strong>.<br>Các tỉnh thành khác: <strong>3-5 ngày làm việc</strong>.<br>Vùng sâu, vùng xa: <strong>5-7 ngày làm việc</strong>.' },
  { category: 'Vận chuyển', q: 'Phí vận chuyển được tính như thế nào?', a: 'Miễn phí vận chuyển cho đơn hàng từ <strong>500.000 đồng</strong>. Đơn dưới 500.000đ phí ship từ 25.000 - 40.000đ tùy khu vực.' },
  { category: 'Vận chuyển', q: 'Tôi có thể theo dõi đơn hàng không?', a: 'Có. Sau khi đơn hàng được gửi đi, chúng tôi sẽ gửi email kèm mã vận đơn. Bạn có thể theo dõi tại mục <strong>Đơn hàng của tôi</strong> trong tài khoản.' },
  { category: 'Đổi trả', q: 'Chính sách đổi trả như thế nào?', a: 'Chúng tôi chấp nhận đổi trả trong vòng <strong>30 ngày</strong> kể từ ngày nhận hàng. Sản phẩm phải còn nguyên vẹn, chưa sử dụng, còn nguyên hộp và nhãn mác. Xem chi tiết tại <a href="/chinh-sach-doi-tra" style="color:#e8191a;font-weight:600">Chính sách đổi trả</a>.' },
  { category: 'Đổi trả', q: 'Mất bao lâu để hoàn tiền?', a: 'Sau khi chúng tôi nhận và kiểm tra hàng hoàn, tiền sẽ được hoàn trong <strong>3-7 ngày làm việc</strong> tùy phương thức thanh toán.' },
  { category: 'Thanh toán', q: 'Có những hình thức thanh toán nào?', a: 'Chúng tôi chấp nhận: <strong>COD (tiền mặt khi nhận hàng)</strong>, Momo, ZaloPay, VNPay, thẻ ATM, thẻ tín dụng Visa/Mastercard.' },
  { category: 'Thanh toán', q: 'Thanh toán online có an toàn không?', a: 'Hoàn toàn an toàn. Mọi giao dịch đều được mã hóa SSL 256-bit. Chúng tôi không lưu trữ thông tin thẻ của bạn.' },
  { category: 'Sản phẩm', q: 'Hàng có chính hãng không?', a: 'Tất cả sản phẩm tại Giày Đẹp Store đều là <strong>hàng chính hãng 100%</strong>, nhập khẩu trực tiếp từ nhà phân phối ủy quyền.' },
  { category: 'Sản phẩm', q: 'Làm thế nào để chọn đúng size?', a: 'Tham khảo <a href="/bang-size-giay" style="color:#e8191a;font-weight:600">Bảng size giày</a> của chúng tôi. Nếu cần tư vấn thêm, liên hệ hotline <strong>0123 456 789</strong>.' },
]

const filteredFaqs = computed(() => {
  if (activeCategory.value === 'Tất cả') return faqs
  return faqs.filter(f => f.category === activeCategory.value)
})

const getCategoryCount = (category) => {
  if (category === 'Tất cả') return faqs.length
  return faqs.filter(f => f.category === category).length
}
</script>

<style scoped>
.faq-page {
  background: linear-gradient(180deg, #f9fafc 0%, #ffffff 100%);
}

/* Hero Section với hiệu ứng nền độc đáo */
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

/* Category Buttons */
.category-tabs {
  perspective: 500px;
}

.category-btn {
  backdrop-filter: blur(4px);
  transition: all 0.2s ease;
  overflow: hidden;
  border: 1px solid transparent;
}

.category-btn.active {
  background: #e8191a;
  color: white;
  box-shadow: 0 8px 20px -8px rgba(232, 25, 26, 0.4);
  transform: translateY(-2px);
  border-color: rgba(255,255,255,0.2);
}

.category-btn.inactive {
  background: white;
  color: #4b5563;
  border-color: #e5e7eb;
}

.category-btn.inactive:hover {
  border-color: #e8191a;
  color: #e8191a;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px -4px rgba(0,0,0,0.05);
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 24px;
  padding: 0 6px;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 600;
  margin-left: 8px;
  transition: all 0.2s;
}

.active-indicator {
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 3px;
  background: white;
  border-radius: 3px;
  box-shadow: 0 0 6px rgba(232,25,26,0.6);
}

/* FAQ Card */
.faq-card {
  border: 1px solid #f0f0f0;
  transition: all 0.25s cubic-bezier(0.2, 0, 0, 1);
  position: relative;
}

.faq-card.card-open {
  border-color: rgba(232, 25, 26, 0.2);
  background: white;
  transform: translateY(-2px);
}

.faq-card.card-closed:hover {
  border-color: #e2e8f0;
}

/* Answer Content */
.answer-content :deep(strong) {
  color: #e8191a;
  font-weight: 700;
}

.answer-content :deep(a) {
  color: #e8191a;
  text-decoration: none;
  border-bottom: 1px dashed #e8191a;
  transition: all 0.2s;
}

.answer-content :deep(a:hover) {
  border-bottom-style: solid;
  opacity: 0.8;
}

/* Animation fadeIn */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeInUp 0.3s ease-out forwards;
}

/* Support Buttons */
.support-btn-primary {
  background: #e8191a;
  color: white;
  font-weight: 700;
  padding: 0.85rem 1.8rem;
  border-radius: 60px;
  transition: all 0.3s;
  box-shadow: 0 8px 20px -6px rgba(232, 25, 26, 0.4);
  border: none;
  font-size: 0.95rem;
}

.support-btn-primary:hover {
  background: #c41516;
  transform: translateY(-2px);
  box-shadow: 0 15px 25px -10px rgba(232, 25, 26, 0.5);
}

.support-btn-outline {
  background: transparent;
  color: #1f2937;
  font-weight: 700;
  padding: 0.85rem 1.8rem;
  border-radius: 60px;
  transition: all 0.3s;
  border: 1px solid #e5e7eb;
  backdrop-filter: blur(4px);
}

.support-btn-outline:hover {
  border-color: #e8191a;
  background: rgba(232, 25, 26, 0.03);
  transform: translateY(-2px);
  color: #e8191a;
}

/* Responsive */
@media (max-width: 640px) {
  .hero-section {
    padding: 2.5rem 0 3rem;
  }
  
  .faq-card button {
    padding: 1rem 1.25rem;
  }
  
  .support-btn-primary, .support-btn-outline {
    padding: 0.7rem 1.5rem;
    font-size: 0.9rem;
  }
  
  .category-btn {
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
  }
  
  .count-badge {
    min-width: 22px;
    height: 20px;
    font-size: 10px;
  }
}
</style>