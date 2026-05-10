<template>
  <div class="size-guide-page">
    <!-- Hero Section với hiệu ứng động -->
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
          <span class="text-[#e8191a] font-medium">Bảng size giày</span>
        </div>
        <div class="max-w-2xl">
          <h1 class="text-4xl md:text-5xl font-black text-white leading-tight" data-aos="fade-up" data-aos-duration="600">
            Bảng <span class="text-gradient">size giày</span>
          </h1>
          <p class="mt-4 text-white/80 text-lg" data-aos="fade-up" data-aos-delay="100" data-aos-duration="600">Chọn đúng size để có trải nghiệm thoải mái nhất trên từng bước chân</p>
        </div>
      </div>
    </div>

    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16 space-y-12">
      <!-- Hướng dẫn đo size 3 bước -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden" data-aos="fade-up" data-aos-duration="600">
        <div class="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-b border-gray-100">
          <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
            <span class="w-1 h-6 bg-[#e8191a] rounded-full"></span>
            Cách đo size chân tại nhà
          </h2>
        </div>
        <div class="p-6 md:p-8">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div v-for="(step, idx) in measureSteps" :key="idx" class="text-center group" data-aos="zoom-in" :data-aos-delay="idx * 100">
              <div class="relative inline-block mb-4">
                <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-red-500 to-[#e8191a] text-white text-2xl font-black flex items-center justify-center mx-auto shadow-lg group-hover:scale-110 transition-transform duration-300">
                  {{ idx + 1 }}
                </div>
                <div class="absolute -bottom-2 -right-2 text-3xl">{{ step.icon }}</div>
              </div>
              <h3 class="font-bold text-gray-800 text-lg mb-2">{{ step.title }}</h3>
              <p class="text-sm text-gray-500 leading-relaxed">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab selector với hiệu ứng đẹp -->
      <div class="flex flex-wrap justify-center gap-3" data-aos="fade-up">
        <button
          v-for="tab in ['Nam', 'Nữ', 'Trẻ em']"
          :key="tab"
          @click="activeTab = tab"
          class="tab-btn px-8 py-3 rounded-full text-sm font-bold transition-all duration-300"
          :class="activeTab === tab ? 'active' : 'inactive'"
        >
          {{ tab }}
        </button>
      </div>

      <!-- Bảng size chính -->
      <div class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden" data-aos="fade-up" data-aos-duration="600">
        <div class="overflow-x-auto">
          <table class="w-full text-sm size-table">
            <thead>
              <tr class="bg-gray-900 text-white">
                <th class="px-5 py-4 text-left font-bold">Size VN</th>
                <th class="px-5 py-4 text-center font-bold">EU</th>
                <th class="px-5 py-4 text-center font-bold">US</th>
                <th class="px-5 py-4 text-center font-bold">UK</th>
                <th class="px-5 py-4 text-center font-bold">Chiều dài (cm)</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, idx) in currentSizeTable"
                :key="idx"
                class="border-b border-gray-100 hover:bg-red-50/40 transition-colors"
                :class="idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/30'"
              >
                <td class="px-5 py-3 font-black text-[#e8191a] text-base">{{ row[0] }}</td>
                <td class="px-5 py-3 text-center text-gray-700 font-medium">{{ row[1] }}</td>
                <td class="px-5 py-3 text-center text-gray-700 font-medium">{{ row[2] }}</td>
                <td class="px-5 py-3 text-center text-gray-700 font-medium">{{ row[3] }}</td>
                <td class="px-5 py-3 text-center font-semibold text-gray-900 bg-gray-50/50">{{ row[4] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Lưu ý và mẹo chọn size (2 cột) -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 relative overflow-hidden group" data-aos="fade-right">
          <div class="absolute top-0 right-0 w-28 h-28 bg-green-50 rounded-full -mr-14 -mt-14 group-hover:scale-110 transition-transform duration-500"></div>
          <h3 class="font-bold text-gray-800 text-xl mb-4 flex items-center gap-2 relative z-10">
            <span class="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center text-2xl">📏</span>
            Mẹo chọn size chuẩn
          </h3>
          <ul class="space-y-3 text-gray-600 relative z-10">
            <li v-for="tip in sizeTips" :key="tip" class="flex items-start gap-2">
              <span class="w-5 h-5 rounded-full bg-green-500 text-white text-xs flex items-center justify-center mt-0.5 shrink-0">✓</span>
              <span class="text-sm">{{ tip }}</span>
            </li>
          </ul>
        </div>

        <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-6 shadow-lg text-white relative overflow-hidden group" data-aos="fade-left">
          <div class="absolute bottom-0 right-0 w-32 h-32 bg-red-500/20 rounded-full -mr-16 -mb-16 group-hover:scale-110 transition-transform duration-500"></div>
          <h3 class="font-bold text-xl mb-3 flex items-center gap-2 relative z-10">
            <span class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-2xl">💬</span>
            Vẫn chưa chắc chắn?
          </h3>
          <p class="text-gray-300 text-sm mb-6 leading-relaxed relative z-10">
            Đội ngũ tư vấn của chúng tôi sẽ giúp bạn tìm ra size hoàn hảo nhất qua Zalo, Facebook hoặc Hotline.
          </p>
          <RouterLink
            to="/lien-he"
            class="inline-flex items-center gap-2 bg-[#e8191a] hover:bg-[#c41516] text-white font-bold px-6 py-3 rounded-xl transition-all duration-300 shadow-lg shadow-red-500/30 relative z-10"
          >
            Tư vấn ngay
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </RouterLink>
        </div>
      </div>

      <!-- Dòng chú thích cuối -->
      <p class="text-center text-xs text-gray-400 border-t border-gray-100 pt-6">
        Lưu ý: Bảng size chỉ mang tính chất tham khảo. Mỗi dòng giày có thể có sai số nhỏ. Hãy liên hệ tư vấn nếu bạn ở giữa hai size.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { RouterLink } from 'vue-router'
import AOS from 'aos'

const activeTab = ref('Nam')

// Refresh AOS when switching tabs to ensure animations work correctly
watch(activeTab, () => {
  nextTick(() => {
    AOS.refresh()
  })
})

// Dữ liệu bảng size
const menSizeTable = [
  ['38', '38', '6', '5.5', '24.0'],
  ['39', '39', '6.5', '6', '24.5'],
  ['40', '40', '7', '6.5', '25.0'],
  ['41', '41', '8', '7.5', '25.5-26.0'],
  ['42', '42', '8.5', '8', '26.5'],
  ['43', '43', '9.5', '9', '27.0'],
  ['44', '44', '10', '9.5', '27.5'],
  ['45', '45', '11', '10.5', '28.0-28.5'],
]

const womenSizeTable = [
  ['35', '35', '5', '2.5', '22.0'],
  ['36', '36', '5.5', '3', '22.5'],
  ['37', '37', '6', '4', '23.0'],
  ['38', '38', '7', '5', '23.5-24.0'],
  ['39', '39', '8', '6', '24.5'],
  ['40', '40', '9', '7', '25.0'],
  ['41', '41', '9.5', '7.5', '25.5'],
]

const kidsSizeTable = [
  ['28', '28', '11K', '10K', '17.5'],
  ['29', '29', '12K', '11K', '18.0'],
  ['30', '30', '12.5K', '11.5K', '18.5'],
  ['31', '31', '13K', '12K', '19.0'],
  ['32', '32', '1Y', '13K', '19.5'],
  ['33', '33', '2Y', '1Y', '20.5'],
  ['34', '34', '3Y', '2Y', '21.0'],
  ['35', '35', '3.5Y', '2.5Y', '22.0'],
]

const currentSizeTable = computed(() => {
  if (activeTab.value === 'Nam') return menSizeTable
  if (activeTab.value === 'Nữ') return womenSizeTable
  return kidsSizeTable
})

const measureSteps = [
  { icon: '📄', title: 'Chuẩn bị giấy', desc: 'Đặt chân lên tờ giấy trắng, giữ thẳng người và phân bổ đều trọng lượng.' },
  { icon: '✏️', title: 'Đánh dấu', desc: 'Dùng bút đánh dấu điểm dài nhất của ngón chân và điểm cuối của gót chân.' },
  { icon: '📏', title: 'Đo khoảng cách', desc: 'Đo khoảng cách giữa 2 điểm vừa đánh dấu. Đây chính là chiều dài chân của bạn.' },
]

const sizeTips = [
  'Đo vào buổi chiều tối khi chân to nhất trong ngày.',
  'Nếu hai chân có kích thước khác nhau, chọn size theo chân lớn hơn.',
  'Với giày thể thao nên chọn size lớn hơn 0.5-1 số so với giày da.',
  'Khi mua online, hãy tham khảo đánh giá của khách hàng về size.',
  'Giày da thường có thể giãn ra sau thời gian sử dụng.',
]
</script>

<style scoped>
.size-guide-page {
  background: linear-gradient(180deg, #f9fafc 0%, #ffffff 100%);
}

/* Hero Section */
.hero-section {
  position: relative;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
  padding: 4rem 0 5rem 0;
  overflow: hidden;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
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
  0%, 100% {
    transform: translateY(0) translateX(0);
  }
  50% {
    transform: translateY(-30px) translateX(20px);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

.text-gradient {
  background: linear-gradient(135deg, #fff, #ffb3b3);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

/* Tab buttons */
.tab-btn {
  transition: all 0.2s ease;
  cursor: pointer;
}

.tab-btn.active {
  background: #e8191a;
  color: white;
  box-shadow: 0 8px 20px -8px rgba(232, 25, 26, 0.5);
  border: 2px solid transparent;
  transform: scale(1.02);
}

.tab-btn.inactive {
  background: white;
  color: #4b5563;
  border: 2px solid #e5e7eb;
}

.tab-btn.inactive:hover {
  border-color: #e8191a;
  color: #e8191a;
  transform: translateY(-2px);
}

/* Size table styling */
.size-table {
  border-collapse: collapse;
  width: 100%;
}

.size-table th {
  font-weight: 700;
  letter-spacing: 0.5px;
}

.size-table td,
.size-table th {
  white-space: nowrap;
}

/* Responsive */
@media (max-width: 640px) {
  .hero-section {
    padding: 2.5rem 0 3rem;
  }

  .tab-btn {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }

  .size-table td,
  .size-table th {
    padding: 0.6rem 0.8rem;
    font-size: 0.7rem;
  }

  .size-table td:first-child,
  .size-table th:first-child {
    padding-left: 0.8rem;
  }

  .size-table td:last-child,
  .size-table th:last-child {
    padding-right: 0.8rem;
  }
}
</style>