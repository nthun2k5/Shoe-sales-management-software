<template>
  <div class="policy-page">
    <!-- Hero Section với hiệu ứng động -->
    <div class="hero-section">
      <div class="hero-bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex items-center gap-2 text-sm mb-4 text-white/70" data-aos="fade-right" data-aos-duration="400">
          <RouterLink to="/" class="hover:text-white transition-colors">Trang chủ</RouterLink>
          <span>/</span>
          <span class="text-[#e8191a] font-medium">Chính sách đổi trả</span>
        </div>
        <div class="max-w-2xl">
          <h1 class="text-4xl md:text-5xl font-black text-white leading-tight" data-aos="fade-up" data-aos-duration="600">
            Chính sách <span class="text-gradient">đổi trả</span>
          </h1>
          <p class="mt-4 text-white/80 text-lg" data-aos="fade-up" data-aos-delay="100" data-aos-duration="600">Minh bạch, nhanh chóng và đặt quyền lợi khách hàng lên hàng đầu</p>
          <p class="mt-2 text-white/50 text-sm" data-aos="fade-up" data-aos-delay="200" data-aos-duration="600">Cập nhật lần cuối: 01/01/2026</p>
        </div>
      </div>
    </div>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
      <!-- Quick summary boxes - 3D nhẹ hơn -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-12">
        <div
          v-for="(item, idx) in summaries"
          :key="item.title"
          class="summary-card bg-white rounded-2xl p-6 text-center shadow-sm border border-gray-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
          :style="{ transitionDelay: `${idx * 50}ms` }"
          data-aos="zoom-in" :data-aos-delay="idx * 100"
        >
          <div class="summary-icon w-14 h-14 rounded-xl bg-gradient-to-br from-red-50 to-orange-50 flex items-center justify-center text-3xl mx-auto mb-4">
            {{ item.icon }}
          </div>
          <h3 class="font-bold text-gray-800 text-lg mb-1">{{ item.title }}</h3>
          <p class="text-sm text-gray-500">{{ item.desc }}</p>
        </div>
      </div>

      <!-- Policy accordion -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden" data-aos="fade-up" data-aos-duration="600">
        <div class="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-b border-gray-100">
          <h2 class="text-lg font-bold text-gray-800 flex items-center gap-2">
            <span class="w-1 h-5 bg-[#e8191a] rounded-full"></span>
            Chi tiết chính sách
          </h2>
        </div>

        <div v-for="(section, i) in sections" :key="i" class="policy-section" data-aos="fade-up" :data-aos-delay="i * 50">
          <button
            @click="open === i ? open = -1 : open = i"
            class="policy-trigger w-full flex items-center justify-between px-6 py-5 text-left transition-all duration-200 border-b border-gray-100"
            :class="open === i ? 'bg-red-50/30' : 'hover:bg-gray-50'"
          >
            <div class="flex items-center gap-4">
              <div class="policy-number w-8 h-8 rounded-full bg-[#e8191a] text-white text-sm font-bold flex items-center justify-center shrink-0 shadow-sm">
                {{ i + 1 }}
              </div>
              <span class="font-semibold text-gray-800 text-base md:text-lg" :class="open === i ? 'text-[#e8191a]' : ''">
                {{ section.title }}
              </span>
            </div>
            <svg
              class="w-5 h-5 text-gray-400 transition-all duration-300"
              :class="open === i ? 'rotate-180 text-[#e8191a]' : ''"
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          <div
            v-if="open === i"
            class="policy-content px-6 py-6 bg-gray-50/50 border-b border-gray-100 transition-all animate-fadeIn"
          >
            <div class="text-gray-700 leading-relaxed text-sm md:text-base" v-html="section.content"></div>
          </div>
        </div>
      </div>

      <!-- CTA nổi bật với gradient chuyển động -->
      <div class="mt-12 relative" data-aos="fade-up" data-aos-duration="800">
        <div class="absolute inset-0 bg-gradient-to-r from-red-600 to-orange-500 rounded-2xl blur-2xl opacity-30"></div>
        <div class="relative bg-gradient-to-r from-[#e8191a] to-[#b31617] rounded-2xl p-8 md:p-10 text-center shadow-xl overflow-hidden">
          <div class="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
          <div class="absolute bottom-0 left-0 w-40 h-40 bg-white/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/3"></div>
          <h3 class="text-2xl md:text-3xl font-black text-white mb-2 relative z-10" data-aos="fade-up" data-aos-delay="200">Cần hỗ trợ đổi trả?</h3>
          <p class="text-white/90 text-sm md:text-base mb-6 relative z-10" data-aos="fade-up" data-aos-delay="300">Liên hệ ngay với đội ngũ chăm sóc khách hàng — giải quyết nhanh chóng trong vòng 2 giờ</p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center relative z-10" data-aos="fade-up" data-aos-delay="400">
            <RouterLink to="/lien-he" class="cta-primary inline-flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
              </svg>
              Liên hệ ngay
            </RouterLink>
            <a href="tel:0123456789" class="cta-secondary inline-flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
              </svg>
              📞 0123 456 789
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const open = ref(0)

const summaries = [
  { icon: '📅', title: '30 ngày đổi trả', desc: 'Kể từ ngày nhận hàng' },
  { icon: '✅', title: 'Miễn phí đổi trả', desc: 'Lỗi do nhà sản xuất' },
  { icon: '⚡', title: 'Xử lý nhanh', desc: 'Trong vòng 3-5 ngày làm việc' },
]

const sections = [
  {
    title: 'Điều kiện đổi trả',
    content: `
      <ul class="list-disc pl-5 space-y-2">
        <li>Sản phẩm còn nguyên vẹn, chưa qua sử dụng</li>
        <li>Còn đầy đủ hộp, túi, nhãn mác gốc</li>
        <li>Trong vòng <strong class="text-[#e8191a]">30 ngày</strong> kể từ ngày nhận hàng</li>
        <li>Có hóa đơn mua hàng hoặc mã đơn hàng</li>
        <li>Sản phẩm không thuộc danh mục hàng giảm giá đặc biệt (>50%)</li>
      </ul>
    `
  },
  {
    title: 'Trường hợp được đổi trả miễn phí',
    content: `
      <ul class="list-disc pl-5 space-y-2">
        <li>Hàng bị lỗi kỹ thuật từ nhà sản xuất (đứt chỉ, bong đế, bong keo...)</li>
        <li>Hàng giao sai mẫu, sai size, sai màu so với đơn đặt</li>
        <li>Hàng bị hư hỏng trong quá trình vận chuyển</li>
        <li>Hàng không đúng mô tả trên website</li>
      </ul>
    `
  },
  {
    title: 'Quy trình đổi trả',
    content: `
      <ol class="list-decimal pl-5 space-y-2">
        <li><strong>Bước 1:</strong> Liên hệ hotline <strong class="text-[#e8191a]">0123 456 789</strong> hoặc email <strong>support@giaydep.store</strong> trong vòng 30 ngày</li>
        <li><strong>Bước 2:</strong> Cung cấp mã đơn hàng và mô tả/hình ảnh lý do đổi trả</li>
        <li><strong>Bước 3:</strong> Nhận phiếu đổi trả và gửi hàng về địa chỉ kho của chúng tôi</li>
        <li><strong>Bước 4:</strong> Chúng tôi kiểm tra và xử lý trong 3-5 ngày làm việc</li>
        <li><strong>Bước 5:</strong> Nhận hàng đổi hoặc hoàn tiền vào tài khoản</li>
      </ol>
    `
  },
  {
    title: 'Chính sách hoàn tiền',
    content: `
      <ul class="list-disc pl-5 space-y-2">
        <li>Hoàn tiền 100% nếu lỗi từ nhà sản xuất hoặc giao nhầm</li>
        <li>Hoàn tiền 80% nếu khách hàng đổi ý (trừ phí vận chuyển chiều về)</li>
        <li>Thời gian hoàn tiền: <strong>3-7 ngày làm việc</strong> tùy ngân hàng</li>
        <li>Hình thức hoàn: chuyển khoản ngân hàng, Momo, hoặc voucher mua hàng</li>
      </ul>
    `
  },
  {
    title: 'Trường hợp không áp dụng',
    content: `
      <ul class="list-disc pl-5 space-y-2">
        <li>Sản phẩm đã qua sử dụng, có vết bẩn, trầy xước</li>
        <li>Mất hộp, nhãn mác gốc</li>
        <li>Sau 30 ngày kể từ ngày nhận hàng</li>
        <li>Sản phẩm thuộc chương trình khuyến mãi đặc biệt có ghi rõ "Không đổi trả"</li>
        <li>Sản phẩm bị hư hỏng do tác động ngoại lực, ngâm nước</li>
      </ul>
    `
  },
]
</script>

<style scoped>
.policy-page {
  background: linear-gradient(180deg, #f9fafc 0%, #ffffff 100%);
}

/* Hero Section với hiệu ứng nền chuyển động */
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

/* Summary Cards */
.summary-card {
  transition: all 0.25s cubic-bezier(0.2, 0, 0, 1);
}

.summary-icon {
  transition: transform 0.2s ease;
}

.summary-card:hover .summary-icon {
  transform: scale(1.05);
}

/* Policy Accordion */
.policy-trigger {
  cursor: pointer;
  position: relative;
  z-index: 1;
}

.policy-number {
  transition: all 0.2s ease;
}

.policy-trigger:hover .policy-number {
  transform: scale(1.05);
}

.policy-content {
  animation: fadeInDown 0.25s ease-out forwards;
}

/* CTA Buttons */
.cta-primary {
  background: white;
  color: #e8191a;
  font-weight: 700;
  padding: 0.8rem 1.8rem;
  border-radius: 60px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  font-size: 0.95rem;
}

.cta-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(0,0,0,0.2);
  background: #fef2f2;
}

.cta-secondary {
  background: transparent;
  color: white;
  font-weight: 700;
  padding: 0.8rem 1.8rem;
  border-radius: 60px;
  transition: all 0.3s ease;
  border: 2px solid white;
  font-size: 0.95rem;
}

.cta-secondary:hover {
  background: rgba(255,255,255,0.1);
  transform: translateY(-2px);
  border-color: white;
}

/* Animations */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeInDown 0.3s ease-out forwards;
}

/* Định dạng nội dung HTML danh sách */
.policy-content :deep(ul), .policy-content :deep(ol) {
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;
}

.policy-content :deep(li) {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.policy-content :deep(strong) {
  color: #e8191a;
  font-weight: 700;
}

/* Responsive */
@media (max-width: 640px) {
  .hero-section {
    padding: 2.5rem 0 3rem;
  }

  .summary-card {
    padding: 1rem;
  }

  .summary-icon {
    width: 3rem;
    height: 3rem;
    font-size: 1.5rem;
  }

  .policy-trigger {
    padding: 1rem;
  }

  .policy-number {
    width: 1.8rem;
    height: 1.8rem;
    font-size: 0.75rem;
  }

  .policy-trigger span {
    font-size: 0.9rem;
  }

  .cta-primary, .cta-secondary {
    padding: 0.6rem 1.2rem;
    font-size: 0.85rem;
  }
}
</style>