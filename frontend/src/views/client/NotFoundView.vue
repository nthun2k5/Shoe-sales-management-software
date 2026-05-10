<template>
  <div class="not-found-page">
    <!-- Hero Section nhỏ gọn nhưng ấn tượng -->
    <div class="hero-section">
      <div class="hero-bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <div class="flex items-center justify-center gap-2 text-sm mb-4 text-white/70">
          <RouterLink to="/" class="hover:text-white transition-colors">Trang chủ</RouterLink>
          <span>/</span>
          <span class="text-[#e8191a] font-medium">404</span>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
      <div class="text-center">
        <!-- 404 illustration với hiệu ứng -->
        <div class="relative mb-8 select-none">
          <div class="absolute inset-0 flex items-center justify-center opacity-10">
            <div class="text-[15rem] font-black text-gray-900 leading-none">404</div>
          </div>
          <div class="relative z-10">
            <div class="inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-to-br from-red-50 to-orange-50 shadow-lg mb-4">
              <span class="text-7xl animate-bounce-slow">👟</span>
            </div>
            <div class="text-7xl md:text-8xl font-black tracking-tight">
              <span class="text-gray-800">4</span>
              <span class="text-[#e8191a]">0</span>
              <span class="text-gray-800">4</span>
            </div>
          </div>
        </div>

        <h1 class="text-2xl md:text-3xl font-black text-gray-800 mb-3">Trang không tồn tại</h1>
        <p class="text-gray-500 max-w-md mx-auto mb-8 leading-relaxed">
          Rất tiếc, trang bạn đang tìm kiếm có thể đã bị xóa, đổi tên hoặc tạm thời không hoạt động.
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <RouterLink to="/" class="btn-primary inline-flex items-center justify-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
            </svg>
            Về trang chủ
          </RouterLink>
          <RouterLink to="/products" class="btn-outline inline-flex items-center justify-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
            </svg>
            Xem sản phẩm
          </RouterLink>
        </div>

        <!-- Tìm kiếm nâng cao -->
        <div class="max-w-md mx-auto">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5">
            <div class="flex items-center gap-2 mb-3 justify-center">
              <span class="w-8 h-0.5 bg-gray-200 rounded-full"></span>
              <span class="text-xs font-semibold text-gray-400 tracking-wider">HOẶC TÌM KIẾM</span>
              <span class="w-8 h-0.5 bg-gray-200 rounded-full"></span>
            </div>
            <div class="flex gap-2">
              <input
                v-model="search"
                @keyup.enter="doSearch"
                type="text"
                placeholder="Nhập tên sản phẩm..."
                class="search-input"
              />
              <button @click="doSearch" class="search-btn">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
              </button>
            </div>
            <p class="text-xs text-gray-400 mt-3">Gợi ý: giày thể thao, giày da, sandal...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'

const router = useRouter()
const search = ref('')

function doSearch() {
  if (search.value.trim()) {
    router.push({ name: 'products', query: { search: search.value.trim() } })
  }
}
</script>

<style scoped>
.not-found-page {
  background: linear-gradient(180deg, #f9fafc 0%, #ffffff 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Hero Section giống các trang khác nhưng nhỏ hơn */
.hero-section {
  position: relative;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
  padding: 2rem 0 3rem 0;
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
  top: -30%;
  right: -15%;
  animation: float 20s infinite ease-in-out;
}

.shape-2 {
  width: 25vw;
  height: 25vw;
  background: radial-gradient(circle, #ff4d4d, transparent);
  bottom: -40%;
  left: -10%;
  animation: float 25s infinite reverse;
}

.shape-3 {
  width: 15vw;
  height: 15vw;
  background: radial-gradient(circle, #ff7b7b, transparent);
  top: 20%;
  left: 20%;
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

/* Buttons */
.btn-primary {
  display: inline-flex;
  align-items: center;
  background: #e8191a;
  color: white;
  font-weight: 700;
  padding: 0.75rem 1.8rem;
  border-radius: 60px;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px -6px rgba(232, 25, 26, 0.4);
  font-size: 0.95rem;
}

.btn-primary:hover {
  background: #c41516;
  transform: translateY(-2px);
  box-shadow: 0 15px 25px -10px rgba(232, 25, 26, 0.5);
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  background: transparent;
  color: #1f2937;
  font-weight: 700;
  padding: 0.75rem 1.8rem;
  border-radius: 60px;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
  font-size: 0.95rem;
}

.btn-outline:hover {
  border-color: #e8191a;
  background: rgba(232, 25, 26, 0.04);
  transform: translateY(-2px);
  color: #e8191a;
}

/* Search input */
.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 60px;
  font-size: 0.9rem;
  transition: all 0.2s;
  background: white;
  outline: none;
}

.search-input:focus {
  border-color: #e8191a;
  box-shadow: 0 0 0 3px rgba(232, 25, 26, 0.1);
}

.search-btn {
  background: #e8191a;
  color: white;
  padding: 0 1.2rem;
  border-radius: 60px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.search-btn:hover {
  background: #c41516;
  transform: scale(0.98);
}

/* Animation chậm cho icon giày */
@keyframes bounceSlow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.animate-bounce-slow {
  animation: bounceSlow 2s ease-in-out infinite;
}

/* Responsive */
@media (max-width: 640px) {
  .hero-section {
    padding: 1.5rem 0 2rem;
  }
  
  .btn-primary, .btn-outline {
    padding: 0.6rem 1.2rem;
    font-size: 0.85rem;
  }
  
  .search-input {
    padding: 0.6rem 1rem;
  }
  
  .search-btn {
    padding: 0 1rem;
  }
}
</style>