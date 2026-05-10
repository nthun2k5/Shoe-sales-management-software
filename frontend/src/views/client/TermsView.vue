<template>
  <div class="guide-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex items-center gap-2 text-sm mb-4 text-white/70" data-aos="fade-right" data-aos-duration="400">
          <RouterLink to="/" class="hover:text-white transition-colors">Trang chủ</RouterLink>
          <span>/</span>
          <span class="text-[#e8191a] font-medium">Điều khoản sử dụng</span>
        </div>
        <div class="max-w-2xl">
          <h1 class="text-4xl md:text-5xl font-black text-white leading-tight" data-aos="fade-up" data-aos-duration="600">
            Điều khoản <span class="text-gradient">sử dụng</span>
          </h1>
          <p class="mt-4 text-white/80 text-lg" data-aos="fade-up" data-aos-delay="100" data-aos-duration="600">Cam kết bảo vệ quyền lợi và xây dựng cộng đồng mua sắm văn minh</p>
          <p class="mt-2 text-white/50 text-sm" data-aos="fade-up" data-aos-delay="200" data-aos-duration="600">Cập nhật lần cuối: 01/01/2026</p>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
      <div class="bg-white rounded-3xl shadow-xl border border-gray-100 p-8 md:p-10 space-y-10" data-aos="fade-up" data-aos-duration="800">

        <div class="p-5 rounded-2xl text-sm flex items-start gap-4 transition-all hover:bg-blue-100/50" style="background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe" data-aos="zoom-in" data-aos-delay="300">
          <span class="text-xl">📋</span>
          <p class="font-medium leading-relaxed">Bằng việc sử dụng website này, bạn đồng ý với các điều khoản và điều kiện dưới đây. Vui lòng đọc kỹ trước khi sử dụng dịch vụ của Giày Đẹp Store.</p>
        </div>

        <div v-for="(section, idx) in sections" :key="section.title" class="space-y-4 group" data-aos="fade-up" :data-aos-delay="idx * 50">
          <h2 class="text-xl font-black text-gray-900 flex items-center gap-4 group-hover:text-[#e8191a] transition-colors">
            <span class="w-8 h-8 rounded-xl text-white text-sm font-black flex items-center justify-center shrink-0 shadow-lg shadow-red-500/20" style="background: linear-gradient(135deg, #ff4d4d, #e8191a)">
              {{ section.num }}
            </span>
            {{ section.title }}
          </h2>
          <div class="text-sm md:text-base text-gray-600 leading-relaxed pl-12 border-l-2 border-gray-50 group-hover:border-red-100 transition-colors" v-html="section.content"></div>
        </div>

        <div class="pt-8 border-t border-gray-100 text-center">
          <p class="text-gray-400 text-sm">Cảm ơn bạn đã tin tưởng và đồng hành cùng <span class="text-[#e8191a] font-bold">Giày Đẹp Store</span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
const sections = [
  {
    num: 1, title: 'Chấp nhận điều khoản',
    content: `<p>Bằng việc truy cập và sử dụng website Giày Đẹp Store, bạn xác nhận rằng bạn đã đọc, hiểu và đồng ý bị ràng buộc bởi các điều khoản sử dụng này và tất cả các chính sách có liên quan.</p>`
  },
  {
    num: 2, title: 'Tài khoản người dùng',
    content: `<ul class="list-disc pl-5 space-y-1">
      <li>Bạn chịu trách nhiệm bảo mật tài khoản và mật khẩu của mình</li>
      <li>Không được chia sẻ tài khoản với người khác</li>
      <li>Thông tin đăng ký phải chính xác và đầy đủ</li>
      <li>Bạn phải thông báo ngay khi phát hiện tài khoản bị xâm phạm</li>
      <li>Chúng tôi có quyền đình chỉ tài khoản vi phạm điều khoản</li>
    </ul>`
  },
  {
    num: 3, title: 'Quy định về đặt hàng và thanh toán',
    content: `<ul class="list-disc pl-5 space-y-1">
      <li>Giá sản phẩm có thể thay đổi mà không cần báo trước</li>
      <li>Đơn hàng chỉ được xác nhận sau khi thanh toán thành công</li>
      <li>Chúng tôi có quyền từ chối hoặc hủy đơn hàng bất thường</li>
      <li>Mọi giao dịch đều được ghi nhận và có thể được kiểm tra</li>
    </ul>`
  },
  {
    num: 4, title: 'Sở hữu trí tuệ',
    content: `<p>Tất cả nội dung trên website bao gồm logo, hình ảnh, văn bản, giao diện đều thuộc quyền sở hữu của Giày Đẹp Store. Nghiêm cấm sao chép, sử dụng lại dưới bất kỳ hình thức nào khi chưa được sự đồng ý bằng văn bản.</p>`
  },
  {
    num: 5, title: 'Hành vi bị cấm',
    content: `<ul class="list-disc pl-5 space-y-1">
      <li>Đặt hàng giả, cung cấp thông tin sai lệch</li>
      <li>Hack, tấn công hoặc cố gắng xâm phạm hệ thống</li>
      <li>Spam, quảng cáo trái phép qua hệ thống của chúng tôi</li>
      <li>Sử dụng bot, script để thực hiện giao dịch tự động</li>
      <li>Lợi dụng lỗi hệ thống để hưởng lợi bất chính</li>
    </ul>`
  },
  {
    num: 6, title: 'Giới hạn trách nhiệm',
    content: `<p>Giày Đẹp Store không chịu trách nhiệm đối với các thiệt hại gián tiếp, ngẫu nhiên phát sinh từ việc sử dụng dịch vụ. Trách nhiệm tối đa của chúng tôi giới hạn ở giá trị đơn hàng thực tế.</p>`
  },
  {
    num: 7, title: 'Thay đổi điều khoản',
    content: `<p>Chúng tôi có quyền cập nhật điều khoản này bất cứ lúc nào. Những thay đổi quan trọng sẽ được thông báo qua email. Việc tiếp tục sử dụng dịch vụ sau khi thay đổi có nghĩa là bạn chấp nhận điều khoản mới.</p>`
  },
]
</script>

<style scoped>
.guide-page {
  background: linear-gradient(180deg, #f9fafc 0%, #ffffff 100%);
}

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

@media (max-width: 640px) {
  .hero-section {
    padding: 2.5rem 0 3rem;
  }
}
</style>
