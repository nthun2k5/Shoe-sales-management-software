<template>
  <div class="bg-white">
    <!-- Hero Section -->
    <div class="relative py-20 bg-slate-900 overflow-hidden">
      <div class="absolute inset-0 opacity-20">
        <div class="absolute inset-0 bg-linear-to-r from-red-600 to-transparent"></div>
        <div class="grid grid-cols-8 gap-4 transform -rotate-12 scale-150">
          <div v-for="i in 32" :key="i" class="aspect-square rounded-2xl bg-white/10 animate-pulse" :style="{ animationDelay: (i * 100) + 'ms' }"></div>
        </div>
      </div>
      
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <h1 class="text-4xl md:text-6xl font-black text-white mb-6 tracking-tight" data-aos="fade-down">
          Về <span class="text-red-500">Giày Đẹp</span> Store
        </h1>
        <p class="text-xl text-slate-300 max-w-2xl mx-auto font-medium leading-relaxed" data-aos="fade-up" data-aos-delay="100">
          Nơi khơi nguồn đam mê và khẳng định phong cách qua từng bước chân. 
          Chúng tôi mang đến những siêu phẩm giày dép chất lượng nhất từ các thương hiệu hàng đầu thế giới.
        </p>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div data-aos="fade-right">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold mb-4 uppercase tracking-widest bg-red-50 text-red-600">
            Câu chuyện của chúng tôi
          </div>
          <h2 class="text-3xl font-black text-slate-900 mb-6 leading-tight">Hành trình mang lại sự tự tin cho khách hàng Việt</h2>
          <div class="space-y-4 text-slate-600 leading-relaxed font-medium">
            <p>
              Được thành lập từ năm 2020, Giày Đẹp Store bắt đầu với một niềm tin đơn giản: Mỗi đôi giày không chỉ là phụ kiện, mà là người bạn đồng hành trên mọi nẻo đường thành công.
            </p>
            <p>
              Chúng tôi không ngừng tìm kiếm và tuyển chọn những mẫu giày đa dạng từ Sneakers năng động, giày Tây lịch lãm đến những đôi Sandal thoải mái. Mọi sản phẩm đều được kiểm duyệt gắt gao về chất liệu và thiết kế trước khi đến tay bạn.
            </p>
            <div class="grid grid-cols-2 gap-6 pt-6">
              <div>
                <div class="text-3xl font-black text-red-600 mb-1">50K+</div>
                <div class="text-sm text-slate-400 font-bold uppercase tracking-wider">Khách hàng tin dùng</div>
              </div>
              <div>
                <div class="text-3xl font-black text-red-600 mb-1">100+</div>
                <div class="text-sm text-slate-400 font-bold uppercase tracking-wider">Thương hiệu đối tác</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="relative" data-aos="fade-left">
          <div class="absolute -inset-4 bg-red-100 rounded-3xl -rotate-3"></div>
          <div class="relative bg-slate-100 rounded-2xl overflow-hidden aspect-4/3 shadow-2xl">
             <img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=1000" class="w-full h-full object-cover" />
          </div>
          <div class="absolute -bottom-6 -right-6 bg-white p-6 rounded-2xl shadow-xl hidden md:block">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center text-white">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
              </div>
              <div>
                <p class="text-sm font-bold text-slate-900">Cam kết chính hãng</p>
                <p class="text-xs text-slate-400">Hoàn tiền 200% nếu phát hiện giả</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AOS from 'aos'

onMounted(() => {
  AOS.init({ duration: 800, once: true })
})
</script>
