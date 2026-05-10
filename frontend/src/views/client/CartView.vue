<template>
  <div class="min-h-screen bg-[#f8f9fa] pb-20">


    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">
          Giỏ hàng của bạn 
          <span class="text-gray-400 font-normal ml-2">({{ cartStore.totalItems }} sản phẩm)</span>
        </h1>
        <RouterLink to="/products" class="text-sm font-bold text-primary-600 hover:text-primary-700 flex items-center gap-1 transition-all hover:gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
          Tiếp tục mua sắm
        </RouterLink>
      </div>

      <div v-if="cartStore.items.length === 0" class="max-w-2xl mx-auto text-center py-24 glass-card bg-white/80 animate-fade-in">
        <div class="w-24 h-24 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 mb-2">Giỏ hàng của bạn đang trống</h2>
        <p class="text-gray-500 mb-8 max-w-sm mx-auto">Có vẻ như bạn chưa thêm bất kỳ sản phẩm nào vào giỏ hàng của mình. Hãy khám phá bộ sưu tập mới nhất của chúng tôi!</p>
        <RouterLink to="/products" class="btn-primary px-10 py-4 shadow-xl shadow-primary-500/20">
          Khám phá ngay
        </RouterLink>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Main Cart Content -->
        <div class="lg:col-span-8 space-y-6">
          <div v-for="(item, index) in cartStore.items" :key="item.id" 
            class="bg-white rounded-2xl p-4 md:p-6 flex flex-col md:flex-row gap-6 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 animate-fade-in group"
            :style="{ animationDelay: `${index * 0.1}s` }">
            
            <!-- Product Image -->
            <div class="w-full md:w-32 h-32 rounded-xl bg-gray-50 overflow-hidden shrink-0 relative">
              <img v-if="item.anh_san_pham" :src="item.anh_san_pham" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              </div>
            </div>

            <!-- Product Details -->
            <div class="flex-1 flex flex-col justify-between min-w-0">
              <div class="flex justify-between items-start gap-4">
                <div>
                  <h3 class="font-bold text-gray-900 text-lg group-hover:text-primary-600 transition-colors line-clamp-1">
                    {{ item.ten_san_pham }}
                  </h3>
                  <div class="flex items-center gap-4 mt-1 text-sm text-gray-500">
                    <span v-if="item.kich_thuoc">Size: <span class="font-semibold text-gray-700">{{ item.kich_thuoc }}</span></span>
                  </div>
                </div>
                <button @click="cartStore.removeItem(item.id)" class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </div>

              <div class="flex items-end justify-between mt-6">
                <div class="flex items-center bg-gray-50 rounded-xl p-1 border border-gray-100">
                  <button @click="updateQty(item.id, item.so_luong - 1)" 
                    class="w-9 h-9 flex items-center justify-center text-gray-500 hover:text-primary-600 hover:bg-white rounded-lg transition-all font-bold">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/></svg>
                  </button>
                  <span class="w-10 text-center font-bold text-gray-900">{{ item.so_luong }}</span>
                  <button @click="updateQty(item.id, item.so_luong + 1)" 
                    class="w-9 h-9 flex items-center justify-center text-gray-500 hover:text-primary-600 hover:bg-white rounded-lg transition-all font-bold">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
                  </button>
                </div>
                <div class="text-right">
                  <p v-if="item.gia_khuyen_mai" class="text-xs text-gray-400 line-through mb-1">
                    {{ formatPrice(item.gia_san_pham * item.so_luong) }}
                  </p>
                  <p class="font-extrabold text-gray-900 text-xl tracking-tight">
                    {{ formatPrice(item.thanh_tien) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Promo Code Section -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <h4 class="font-bold text-gray-900 mb-4">Mã giảm giá</h4>
            <div class="flex gap-3">
              <input type="text" placeholder="Nhập mã ưu đãi..." class="input-field flex-1" />
              <button class="btn-outline border-gray-200 text-gray-600 hover:bg-gray-50 hover:text-gray-900">Áp dụng</button>
            </div>
          </div>
        </div>

        <!-- Order Summary Sidebar -->
        <div class="lg:col-span-4 sticky top-24">
          <div class="glass-card bg-white p-6 border border-gray-100 shadow-xl overflow-hidden relative">
            <div class="absolute top-0 right-0 w-32 h-32 bg-primary-50/50 rounded-full -mr-16 -mt-16 blur-3xl"></div>
            
            <h3 class="font-bold text-gray-900 text-xl mb-6 relative">Tóm tắt đơn hàng</h3>
            
            <div class="space-y-4 relative">
              <div class="flex justify-between text-gray-500">
                <span>Tạm tính ({{ cartStore.totalItems }} sản phẩm)</span>
                <span class="font-semibold text-gray-900">{{ formatPrice(cartStore.totalAmount) }}</span>
              </div>
              <div class="flex justify-between text-gray-500">
                <span>Phí vận chuyển</span>
                <span class="font-semibold text-green-600" v-if="cartStore.totalAmount >= 500000">Miễn phí</span>
                <span class="font-semibold text-gray-900" v-else>{{ formatPrice(30000) }}</span>
              </div>
              <div class="flex justify-between text-gray-500">
                <span>Giảm giá</span>
                <span class="font-semibold text-primary-600">- {{ formatPrice(0) }}</span>
              </div>
              
              <div class="pt-4 border-t border-gray-100">
                <div class="flex justify-between items-center mb-1">
                  <span class="font-bold text-gray-900 text-lg">Tổng cộng</span>
                  <span class="font-black text-2xl text-primary-600 tracking-tighter">
                    {{ formatPrice(cartStore.totalAmount + (cartStore.totalAmount >= 500000 ? 0 : 30000)) }}
                  </span>
                </div>
                <p class="text-xs text-gray-400 text-right">(Đã bao gồm VAT nếu có)</p>
              </div>
            </div>

            <RouterLink to="/checkout" class="w-full btn-primary py-4 justify-center mt-8 shadow-lg shadow-primary-500/20 group relative overflow-hidden">
              <span class="relative z-10 flex items-center gap-2">
                Tiến hành thanh toán
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
              </span>
            </RouterLink>

            <div class="mt-8 pt-8 border-t border-gray-100 space-y-4">
              <div class="flex items-center gap-3 text-xs text-gray-500">
                <div class="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center shrink-0 text-primary-500">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-7.618 3.033A11.966 11.966 0 013 11.723 11.97 11.97 0 0012 21.231 11.97 11.97 0 0021 11.723a11.966 11.966 0 01-1.382-5.751z"/></svg>
                </div>
                <p>Thanh toán bảo mật 100% với mã hóa SSL cao cấp.</p>
              </div>
              <div class="flex items-center gap-3 text-xs text-gray-500">
                <div class="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center shrink-0 text-primary-500">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                </div>
                <p>Đổi trả dễ dàng trong vòng 30 ngày nếu không hài lòng.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const router = useRouter()

function formatPrice(p) { 
  return new Intl.NumberFormat('vi-VN', { 
    style: 'currency', 
    currency: 'VND' 
  }).format(p) 
}

function updateQty(id, qty) { 
  if (qty >= 1) {
    cartStore.updateQuantity(id, qty) 
  } else {
    // If quantity is 0, we could ask to remove or just ignore
    // For better UX, let's keep it at 1 or handle removal via delete button
  }
}
</script>

<style scoped>
.glass-card {
  backdrop-filter: blur(8px);
}
</style>

