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
          <span class="text-[#e8191a] font-medium">Chính sách bảo mật</span>
        </div>
        <div class="max-w-2xl">
          <h1 class="text-4xl md:text-5xl font-black text-white leading-tight" data-aos="fade-up" data-aos-duration="600">
            Chính sách <span class="text-gradient">bảo mật</span>
          </h1>
          <p class="mt-4 text-white/80 text-lg" data-aos="fade-up" data-aos-delay="100" data-aos-duration="600">Bảo vệ thông tin cá nhân là ưu tiên hàng đầu tại Giày Đẹp Store</p>
          <p class="mt-2 text-white/50 text-sm" data-aos="fade-up" data-aos-delay="200" data-aos-duration="600">Cập nhật lần cuối: 01/01/2026</p>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
      <div class="bg-white rounded-3xl shadow-xl border border-gray-100 p-8 md:p-10 space-y-10" data-aos="fade-up" data-aos-duration="800">

        <div class="p-5 rounded-2xl text-sm flex items-start gap-4 transition-all hover:bg-green-100/50" style="background:#f0fdf4;color:#15803d;border:1px solid #bbf7d0" data-aos="zoom-in" data-aos-delay="300">
          <span class="text-xl">🔒</span>
          <p class="font-medium leading-relaxed">Giày Đẹp Store cam kết bảo vệ tuyệt đối quyền riêng tư và thông tin cá nhân của khách hàng. Chúng tôi sử dụng các công nghệ bảo mật hàng đầu để đảm bảo an toàn cho dữ liệu của bạn.</p>
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

        <div class="pt-10 border-t border-gray-100">
          <div class="bg-gray-50 rounded-2xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6" data-aos="zoom-in">
            <div class="text-center md:text-left">
              <h2 class="text-xl font-black text-gray-900 mb-2">Liên hệ về bảo mật</h2>
              <p class="text-sm text-gray-500">Nếu bạn có bất kỳ câu hỏi hoặc thắc mắc về quyền riêng tư:</p>
            </div>
            <div class="space-y-3 shrink-0">
              <a href="mailto:privacy@giaydep.store" class="flex items-center gap-3 text-sm font-bold text-gray-700 hover:text-[#e8191a] transition-colors">
                <span class="w-8 h-8 rounded-lg bg-white shadow-sm flex items-center justify-center">📧</span>
                privacy@giaydep.store
              </a>
              <div class="flex items-center gap-3 text-sm font-bold text-gray-700">
                <span class="w-8 h-8 rounded-lg bg-white shadow-sm flex items-center justify-center">📞</span>
                0123 456 789
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const sections = [
  {
    num: 1, title: 'Thông tin chúng tôi thu thập',
    content: `<ul class="list-disc pl-5 space-y-1">
      <li>Thông tin cá nhân: họ tên, địa chỉ email, số điện thoại, địa chỉ giao hàng</li>
      <li>Thông tin tài khoản: tên đăng nhập, mật khẩu (được mã hóa)</li>
      <li>Thông tin đơn hàng: lịch sử mua hàng, địa chỉ giao hàng</li>
      <li>Thông tin thiết bị: địa chỉ IP, trình duyệt, hệ điều hành</li>
    </ul>`
  },
  {
    num: 2, title: 'Mục đích sử dụng thông tin',
    content: `<ul class="list-disc pl-5 space-y-1">
      <li>Xử lý đơn hàng và giao hàng đến địa chỉ của bạn</li>
      <li>Gửi thông báo về trạng thái đơn hàng</li>
      <li>Cung cấp hỗ trợ khách hàng</li>
      <li>Gửi thông tin khuyến mãi (nếu bạn đồng ý)</li>
      <li>Cải thiện dịch vụ và trải nghiệm người dùng</li>
      <li>Tuân thủ nghĩa vụ pháp lý</li>
    </ul>`
  },
  {
    num: 3, title: 'Chia sẻ thông tin với bên thứ ba',
    content: `<p>Chúng tôi <strong>không bán, trao đổi hoặc cho thuê</strong> thông tin cá nhân của bạn. Thông tin chỉ được chia sẻ với:</p>
    <ul class="list-disc pl-5 space-y-1 mt-2">
      <li>Đơn vị vận chuyển để thực hiện giao hàng</li>
      <li>Cổng thanh toán để xử lý giao dịch</li>
      <li>Cơ quan nhà nước khi có yêu cầu hợp pháp</li>
    </ul>`
  },
  {
    num: 4, title: 'Bảo mật thông tin',
    content: `<ul class="list-disc pl-5 space-y-1">
      <li>Mã hóa SSL 256-bit cho tất cả giao dịch</li>
      <li>Mật khẩu được băm (hash) với thuật toán bcrypt</li>
      <li>Hệ thống tường lửa và giám sát 24/7</li>
      <li>Không lưu trữ thông tin thẻ tín dụng trực tiếp</li>
      <li>Kiểm tra bảo mật định kỳ</li>
    </ul>`
  },
  {
    num: 5, title: 'Quyền của bạn',
    content: `<ul class="list-disc pl-5 space-y-1">
      <li><strong>Truy cập:</strong> Xem thông tin cá nhân chúng tôi đang lưu trữ</li>
      <li><strong>Chỉnh sửa:</strong> Cập nhật thông tin không chính xác</li>
      <li><strong>Xóa:</strong> Yêu cầu xóa tài khoản và dữ liệu</li>
      <li><strong>Từ chối:</strong> Hủy đăng ký nhận email marketing bất cứ lúc nào</li>
    </ul>`
  },
  {
    num: 6, title: 'Cookie',
    content: `<p>Chúng tôi sử dụng cookie để cải thiện trải nghiệm duyệt web của bạn, bao gồm lưu giỏ hàng và trạng thái đăng nhập. Bạn có thể tắt cookie trong cài đặt trình duyệt, tuy nhiên một số chức năng có thể bị ảnh hưởng.</p>`
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
