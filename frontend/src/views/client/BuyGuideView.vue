<template>
  <div class="guide-page">
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
          <span class="text-[#e8191a] font-medium">Hướng dẫn mua hàng</span>
        </div>
        <div class="max-w-2xl">
          <h1 class="text-4xl md:text-5xl font-black text-white leading-tight" data-aos="fade-up" data-aos-duration="600">
            Hướng dẫn <span class="text-gradient">mua hàng</span>
          </h1>
          <p class="mt-4 text-white/80 text-lg" data-aos="fade-up" data-aos-delay="100" data-aos-duration="600">Mua sắm dễ dàng, nhanh chóng và an toàn chỉ với vài bước đơn giản</p>
        </div>
      </div>
    </div>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16 space-y-10">
      <!-- Steps - Dạng timeline hiện đại -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden" data-aos="fade-up" data-aos-duration="600">
        <div class="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-b border-gray-100">
          <h2 class="text-lg font-bold text-gray-800 flex items-center gap-2">
            <span class="w-1 h-5 bg-[#e8191a] rounded-full"></span>
            Quy trình mua hàng online
          </h2>
        </div>
        <div class="p-6 md:p-8">
          <div class="relative">
            <!-- Đường kẻ dọc dạng gradient -->
            <div class="absolute left-[1.15rem] top-6 bottom-6 w-0.5 bg-gradient-to-b from-red-200 via-gray-200 to-red-100 hidden md:block"></div>
            <div class="space-y-10">
              <div v-for="(step, i) in buySteps" :key="i" class="step-item flex gap-5 group" data-aos="fade-left" :data-aos-delay="i * 50">
                <div class="relative z-10">
                  <div class="step-number w-10 h-10 rounded-full bg-gradient-to-br from-red-500 to-[#e8191a] text-white font-bold text-lg flex items-center justify-center shadow-md group-hover:scale-110 transition-transform duration-300">
                    {{ i+1 }}
                  </div>
                </div>
                <div class="flex-1 pb-2">
                  <h3 class="font-bold text-gray-800 text-base md:text-lg mb-1 group-hover:text-[#e8191a] transition-colors">
                    {{ step.title }}
                  </h3>
                  <p class="text-sm text-gray-600 leading-relaxed">{{ step.desc }}</p>
                  <div v-if="step.tip" class="mt-2 flex items-start gap-2 text-xs bg-blue-50 text-blue-700 p-2 rounded-lg">
                    <span class="shrink-0">💡</span>
                    <span>{{ step.tip }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Payment Methods -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden" data-aos="fade-up" data-aos-duration="600">
        <div class="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-b border-gray-100">
          <h2 class="text-lg font-bold text-gray-800 flex items-center gap-2">
            <span class="w-1 h-5 bg-[#e8191a] rounded-full"></span>
            Phương thức thanh toán
          </h2>
        </div>
        <div class="p-6 md:p-8">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div v-for="(pm, i) in paymentMethods" :key="pm.name"
              class="payment-card flex items-start gap-4 p-4 rounded-xl border border-gray-100 transition-all duration-300 hover:shadow-md hover:border-red-200 group cursor-default"
              data-aos="zoom-in" :data-aos-delay="i * 50">
              <div class="text-3xl shrink-0 group-hover:scale-110 transition-transform duration-200">{{ pm.icon }}</div>
              <div>
                <h3 class="font-bold text-gray-800 text-sm mb-1">{{ pm.name }}</h3>
                <p class="text-xs text-gray-500 leading-relaxed">{{ pm.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Shipping Table -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden" data-aos="fade-up" data-aos-duration="600">
        <div class="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-b border-gray-100">
          <h2 class="text-lg font-bold text-gray-800 flex items-center gap-2">
            <span class="w-1 h-5 bg-[#e8191a] rounded-full"></span>
            Thông tin vận chuyển
          </h2>
        </div>
        <div class="p-6 md:p-8">
          <div class="overflow-x-auto">
            <table class="w-full text-sm shipping-table">
              <thead>
                <tr class="bg-gray-50 rounded-lg">
                  <th class="px-4 py-3 text-left font-bold text-gray-700 rounded-l-lg">Khu vực</th>
                  <th class="px-4 py-3 text-center font-bold text-gray-700">Thời gian</th>
                  <th class="px-4 py-3 text-center font-bold text-gray-700">Phí ship (dưới 500k)</th>
                  <th class="px-4 py-3 text-center font-bold text-gray-700 rounded-r-lg">Phí ship (từ 500k)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, i) in shippingRows" :key="i" class="border-b border-gray-100 hover:bg-red-50/30 transition-colors">
                  <td class="px-4 py-3 font-semibold text-gray-800">{{ row[0] }}</td>
                  <td class="px-4 py-3 text-center text-gray-600">{{ row[1] }}</td>
                  <td class="px-4 py-3 text-center text-gray-600">{{ row[2] }}</td>
                  <td class="px-4 py-3 text-center font-bold text-green-600">{{ row[3] }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Notes Box -->
      <div class="rounded-2xl bg-gradient-to-r from-red-50 to-orange-50 border-l-8 border-[#e8191a] p-6 shadow-md" data-aos="zoom-in" data-aos-duration="600">
        <div class="flex items-start gap-3">
          <div class="shrink-0 text-2xl">⚠️</div>
          <div>
            <h3 class="font-bold text-gray-800 mb-2 text-base">Lưu ý quan trọng</h3>
            <ul class="space-y-1.5 text-sm text-gray-700">
              <li v-for="note in notes" :key="note" class="flex items-start gap-2">
                <span class="text-[#e8191a] shrink-0 mt-0.5">•</span>
                <span>{{ note }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Contact support (optional) -->
      <div class="text-center pt-4" data-aos="fade-up">
        <p class="text-gray-500 text-sm">Vẫn cần hỗ trợ? <RouterLink to="/lien-he" class="text-[#e8191a] font-semibold hover:underline">Liên hệ ngay</RouterLink></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const buySteps = [
  { title: 'Tìm kiếm sản phẩm', desc: 'Duyệt qua các danh mục hoặc sử dụng thanh tìm kiếm để tìm sản phẩm mong muốn.', tip: 'Sử dụng bộ lọc để thu hẹp kết quả theo giá, danh mục, size' },
  { title: 'Xem chi tiết sản phẩm', desc: 'Click vào sản phẩm để xem hình ảnh, mô tả, size, màu sắc và đánh giá từ khách hàng.' },
  { title: 'Chọn size và thêm vào giỏ hàng', desc: 'Chọn size phù hợp (tham khảo bảng size nếu cần) và nhấn "Thêm vào giỏ hàng".', tip: 'Tham khảo bảng size giày nếu bạn chưa chắc chắn về size' },
  { title: 'Đăng nhập / Đăng ký', desc: 'Nếu chưa có tài khoản, hãy đăng ký miễn phí. Nếu đã có, đăng nhập để tiếp tục.' },
  { title: 'Kiểm tra giỏ hàng', desc: 'Xem lại danh sách sản phẩm, số lượng, áp dụng mã giảm giá (voucher) nếu có.' },
  { title: 'Thanh toán', desc: 'Điền địa chỉ giao hàng, chọn phương thức thanh toán và xác nhận đơn hàng.' },
  { title: 'Nhận xác nhận đơn hàng', desc: 'Email xác nhận sẽ được gửi đến địa chỉ của bạn. Theo dõi trạng thái tại mục "Đơn hàng".' },
]

const paymentMethods = [
  { icon: '💵', name: 'COD - Thanh toán khi nhận hàng', desc: 'Thanh toán bằng tiền mặt khi shipper giao hàng tận tay. An toàn và tiện lợi.' },
  { icon: '📱', name: 'Momo / ZaloPay', desc: 'Quét mã QR hoặc nhập số điện thoại để thanh toán qua ví điện tử.' },
  { icon: '🏦', name: 'VNPay / Thẻ ATM nội địa', desc: 'Thanh toán qua cổng VNPay với hầu hết các ngân hàng nội địa.' },
  { icon: '💳', name: 'Visa / Mastercard', desc: 'Thanh toán bằng thẻ tín dụng/ghi nợ quốc tế Visa hoặc Mastercard.' },
]

const shippingRows = [
  ['Nội thành TP.HCM / Hà Nội', '1-2 ngày', '25.000đ', 'Miễn phí'],
  ['Các tỉnh thành lớn', '2-3 ngày làm việc', '30.000đ', 'Miễn phí'],
  ['Tỉnh thành khác', '3-5 ngày làm việc', '35.000đ', 'Miễn phí'],
  ['Vùng sâu, vùng xa', '5-7 ngày làm việc', '40.000đ', 'Miễn phí'],
]

const notes = [
  'Thời gian giao hàng có thể thay đổi vào dịp lễ, Tết hoặc do điều kiện thời tiết.',
  'Kiểm tra hàng hóa trước khi ký nhận. Nếu phát hiện vấn đề, yêu cầu shipper xác nhận trước.',
  'Giữ lại hóa đơn/biên lai để thuận tiện cho việc đổi trả sau này.',
  'Liên hệ hotline 0123 456 789 nếu đơn hàng quá hạn hoặc có vấn đề.',
]
</script>

<style scoped>
.guide-page {
  background: linear-gradient(180deg, #f9fafc 0%, #ffffff 100%);
}

/* Hero Section giống các trang khác */
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

/* Step Items */
.step-number {
  transition: all 0.2s ease;
}

.step-item:hover .step-number {
  box-shadow: 0 0 0 4px rgba(232, 25, 26, 0.2);
}

/* Payment Card */
.payment-card {
  transition: all 0.25s cubic-bezier(0.2, 0, 0, 1);
}

.shipping-table th {
  background-color: #f8fafc;
  font-weight: 700;
}

.shipping-table td, .shipping-table th {
  padding: 0.75rem 1rem;
}

/* Responsive */
@media (max-width: 640px) {
  .hero-section {
    padding: 2rem 0 2.5rem;
  }
  
  .step-number {
    width: 2rem;
    height: 2rem;
    font-size: 0.9rem;
  }
  
  .payment-card {
    padding: 0.75rem;
  }
  
  .shipping-table th, .shipping-table td {
    padding: 0.5rem;
    font-size: 0.75rem;
  }
}
</style>