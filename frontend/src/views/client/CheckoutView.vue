<template>
  <div class="min-h-screen bg-[#f8f9fa] pb-20">
    <!-- Progress Header -->
    <div class="bg-white border-b border-gray-100 pt-8 pb-6 mb-8">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex items-center justify-center space-x-4 md:space-x-12">
          <div class="flex items-center space-x-2 text-primary-600 font-medium">
            <span class="w-8 h-8 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-sm">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            </span>
            <span class="hidden md:block">Giỏ hàng</span>
          </div>
          <div class="w-12 md:w-24 h-px bg-primary-600"></div>
          <div class="flex items-center space-x-2 text-primary-600 font-bold">
            <span class="w-8 h-8 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm">2</span>
            <span class="hidden md:block">Thanh toán</span>
          </div>
          <div class="w-12 md:w-24 h-px bg-gray-200"></div>
          <div class="flex items-center space-x-2 text-gray-400 font-medium">
            <span class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm">3</span>
            <span class="hidden md:block">Hoàn tất</span>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-4 mb-8">
        <button @click="$router.back()" class="p-2 bg-white rounded-full shadow-sm hover:shadow transition-all text-gray-500 hover:text-primary-600">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </button>
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Thanh toán</h1>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Main Form Content -->
        <div class="lg:col-span-8 space-y-6">
          <!-- Shipping Info -->
          <div class="bg-white rounded-2xl p-6 md:p-8 border border-gray-100 shadow-sm animate-fade-in">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center text-primary-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                </div>
                <h3 class="font-bold text-gray-900 text-xl">Địa chỉ nhận hàng</h3>
              </div>
              <RouterLink to="/account/addresses" class="text-xs font-bold text-primary-600 hover:underline">Quản lý địa chỉ</RouterLink>
            </div>
            
            <div v-if="userAddresses.length > 0" class="space-y-4">
              <div v-for="addr in userAddresses" :key="addr.id"
                @click="selectedAddressId = addr.id"
                :class="['relative p-4 rounded-xl border-2 cursor-pointer transition-all duration-300',
                  selectedAddressId === addr.id ? 'border-primary-600 bg-primary-50/20 ring-4 ring-primary-50' : 'border-gray-50 hover:border-gray-100 bg-white']">
                
                <div class="flex items-start gap-3">
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 mb-1">
                      <span class="font-bold text-gray-900">{{ addr.ten_nguoi_nhan }}</span>
                      <span class="text-gray-300">|</span>
                      <span class="font-semibold text-gray-600">{{ addr.so_dien_thoai }}</span>
                      <span v-if="addr.la_mac_dinh" class="text-[8px] font-black bg-gray-900 text-white px-1.5 py-0.5 rounded uppercase tracking-widest ml-1">Mặc định</span>
                    </div>
                    <p class="text-sm text-gray-500 leading-relaxed">{{ addr.dia_chi }}</p>
                  </div>
                  
                  <div class="shrink-0 pt-1">
                    <div v-if="selectedAddressId === addr.id" class="w-5 h-5 bg-primary-600 rounded-full flex items-center justify-center">
                      <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                    </div>
                    <div v-else class="w-5 h-5 border-2 border-gray-200 rounded-full"></div>
                  </div>
                </div>
              </div>

              <!-- Order Note -->
              <div class="mt-6 pt-6 border-t border-gray-100">
                <label class="block text-sm font-bold text-gray-700 mb-2">Ghi chú đơn hàng (Tùy chọn)</label>
                <textarea v-model="form.ghi_chu" class="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm text-gray-900 focus:bg-white focus:border-primary-600 transition-all outline-none min-h-[80px]" placeholder="Lưu ý về thời gian nhận hàng, chỉ dẫn đường đi..."></textarea>
              </div>
            </div>

            <div v-else class="py-12 text-center bg-gray-50 rounded-2xl border border-dashed border-gray-200">
              <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
                <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              </div>
              <p class="text-gray-500 font-medium mb-4">Bạn chưa có địa chỉ nhận hàng nào</p>
              <RouterLink to="/account/addresses" class="btn-primary px-6 py-2.5 text-sm inline-flex">Thêm địa chỉ ngay</RouterLink>
            </div>
          </div>

          <!-- Payment Method -->
          <div class="bg-white rounded-2xl p-6 md:p-8 border border-gray-100 shadow-sm animate-fade-in" style="animation-delay: 0.1s">
            <div class="flex items-center gap-3 mb-6">
              <div class="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center text-primary-600">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/></svg>
              </div>
              <h3 class="font-bold text-gray-900 text-xl">Phương thức thanh toán</h3>
            </div>

            <div class="space-y-2">
              <label v-for="method in paymentMethods" :key="method.value"
                :class="['group relative flex items-center gap-3 p-3 rounded-xl border-2 cursor-pointer transition-all duration-300',
                  form.phuong_thuc_thanh_toan === method.value ? 'border-primary-600 bg-primary-50/20 shadow-sm translate-x-1' : 'border-gray-50 hover:border-gray-100 bg-white hover:bg-gray-50/50']">
                <input type="radio" v-model="form.phuong_thuc_thanh_toan" :value="method.value" class="hidden" />

                <!-- Icon Container -->
                <div :class="['w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-500',
                  form.phuong_thuc_thanh_toan === method.value ? 'bg-primary-600 text-white shadow-md' : 'bg-gray-50 text-gray-400 group-hover:scale-110']" 
                  v-html="method.icon">
                </div>

                <!-- Text Content -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <p class="font-bold text-gray-900 text-sm tracking-tight">{{ method.label }}</p>
                    <span v-if="method.value === 'bank_transfer' || method.value === 'cod'" class="text-[8px] font-black text-primary-600 bg-primary-50 px-1 py-0.5 rounded uppercase tracking-tighter">
                      {{ method.value === 'bank_transfer' ? 'Auto' : 'Free' }}
                    </span>
                  </div>
                  <p class="text-[10px] text-gray-400 line-clamp-1 leading-none mt-0.5">{{ method.desc }}</p>
                </div>

                <!-- Selection Status -->
                <div class="flex items-center justify-center">
                  <div v-if="form.phuong_thuc_thanh_toan === method.value" class="w-5 h-5 bg-primary-600 rounded-full flex items-center justify-center animate-scale-up">
                    <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                  </div>
                  <div v-else class="w-5 h-5 border-2 border-gray-200 rounded-full group-hover:border-primary-200 transition-colors"></div>
                </div>
              </label>
            </div>

            <!-- Account details are now automatic, no selection needed -->
          </div>
        </div>

        <!-- Order Summary Sidebar -->
        <div class="lg:col-span-4 sticky top-24">
          <div class="glass-card bg-white p-6 border border-gray-100 shadow-xl relative overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-primary-600 to-primary-400"></div>
            
            <h3 class="font-bold text-gray-900 text-xl mb-6 flex items-center justify-between">
              Đơn hàng
              <RouterLink to="/cart" class="text-xs font-bold text-primary-600 hover:underline">Sửa</RouterLink>
            </h3>
            
            <!-- Items Preview -->
            <div class="space-y-4 mb-6 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
              <div v-for="item in cartStore.items" :key="item.id" class="flex items-center gap-3 group">
                <div class="w-14 h-14 rounded-lg bg-gray-50 overflow-hidden shrink-0 border border-gray-100 relative">
                  <img v-if="item.anh_san_pham" :src="item.anh_san_pham" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                  <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="font-bold text-gray-900 text-sm line-clamp-1 mb-0.5">{{ item.ten_san_pham }}</p>
                  <p v-if="item.kich_thuoc" class="text-xs text-gray-400 mb-0.5">Size: {{ item.kich_thuoc }}</p>
                  <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-500">x{{ item.so_luong }}</span>
                    <span class="font-semibold text-gray-900">{{ formatPrice(item.thanh_tien) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Coupon Input -->
            <div class="mb-6 space-y-3">
              <label class="block text-sm font-bold text-gray-700">Mã giảm giá</label>
              <div class="flex gap-2">
                <input type="text" v-model="ma_giam_gia" placeholder="Nhập mã giảm giá..." class="input-field flex-1 uppercase" :disabled="couponValid">
                <button v-if="!couponValid" @click="applyCoupon" :disabled="!ma_giam_gia || orderLoading" class="btn-outline px-4 text-sm whitespace-nowrap">Áp dụng</button>
                <button v-else @click="removeCoupon" class="btn-outline border-red-200 text-red-500 hover:bg-red-50 px-4 text-sm whitespace-nowrap">Hủy</button>
              </div>
              <p v-if="couponMsg" :class="['text-xs font-bold', couponValid ? 'text-green-600' : 'text-red-500']">{{ couponMsg }}</p>
            </div>

            <!-- Totals -->
            <div class="space-y-4 pt-6 border-t border-gray-100">
              <div class="flex justify-between text-gray-500 text-sm">
                <span>Tạm tính</span>
                <span class="font-semibold text-gray-900">{{ formatPrice(cartStore.totalAmount || cartStore.tong_tien || 0) }}</span>
              </div>
              <div v-if="discount > 0" class="flex justify-between text-sm">
                <span class="text-gray-500">Giảm giá</span>
                <span class="font-bold text-primary-600">-{{ formatPrice(discount) }}</span>
              </div>
              <div class="flex justify-between text-gray-500 text-sm">
                <span>Phí vận chuyển</span>
                <span class="font-semibold text-green-600" v-if="shipping === 0">Miễn phí</span>
                <span class="font-semibold text-gray-900" v-else>{{ formatPrice(shipping) }}</span>
              </div>
              
              <div class="pt-4 border-t border-gray-100">
                <div class="flex justify-between items-center mb-1">
                  <span class="font-bold text-gray-900 text-lg">Tổng cộng</span>
                  <span class="font-black text-2xl text-primary-600 tracking-tighter">
                    {{ formatPrice(finalAmount) }}
                  </span>
                </div>
                <p class="text-[10px] text-gray-400 text-right uppercase tracking-widest font-bold">Thanh toán cuối cùng</p>
              </div>
            </div>

            <button @click="placeOrder" :disabled="orderLoading" 
              class="w-full btn-primary py-4 justify-center mt-8 shadow-lg shadow-primary-500/20 group relative overflow-hidden">
              <span v-if="orderLoading" class="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></span>
              <span v-else class="relative z-10 flex items-center gap-2">
                Xác nhận đặt hàng
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
              </span>
            </button>
            
            <p v-if="orderError" class="text-red-500 text-xs text-center mt-3 font-bold px-4 py-2 bg-red-50 rounded-lg animate-bounce">{{ orderError }}</p>

            <div class="mt-8 flex items-center justify-center gap-4">
              <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg" class="h-4 opacity-50 grayscale hover:grayscale-0 transition-all" />
              <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" class="h-3 opacity-50 grayscale hover:grayscale-0 transition-all" />
              <img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg" class="h-4 opacity-50 grayscale hover:grayscale-0 transition-all" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bank Transfer Modal -->
    <Teleport to="body">
      <div v-if="showBankModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" @click.self="finishOrder">
        <div class="bg-white rounded-2xl w-full max-w-md flex flex-col shadow-2xl animate-scale-up overflow-hidden">
          <div class="p-6 text-center border-b border-gray-100 bg-primary-50/30">
            <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm border border-primary-100">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <h2 class="text-xl font-black text-gray-900">Đặt hàng thành công!</h2>
            <p class="text-sm text-gray-500 mt-1">Mã đơn hàng: <span class="font-bold text-primary-600">{{ createdOrderCode }}</span></p>
          </div>
          
          <div class="p-6 space-y-6">
            <div v-if="selectedBank" class="text-center">
              <p class="text-sm font-bold text-gray-700 mb-4">Quét mã QR qua ứng dụng ngân hàng</p>
              <!-- VietQR Image -->
              <div class="w-48 h-48 mx-auto bg-gray-50 rounded-xl p-2 border border-gray-200 shadow-inner flex items-center justify-center">
                <img :src="qrCodeUrl" alt="VietQR" class="w-full h-full object-contain" />
              </div>
            </div>

            <div v-if="selectedBank" class="bg-gray-50 rounded-xl p-4 text-sm space-y-3 border border-gray-100">
              <div class="flex justify-between items-center"><span class="text-gray-500">Ngân hàng</span> <span class="font-bold text-gray-900">{{ selectedBank.ten_ngan_hang || selectedBank.ma_ngan_hang }}</span></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Chủ tài khoản</span> <span class="font-bold text-gray-900 uppercase">{{ selectedBank.chu_tai_khoan }}</span></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Số tài khoản</span> <div class="flex items-center gap-2"><span class="font-bold text-primary-600 tracking-wider text-base">{{ selectedBank.so_tai_khoan }}</span></div></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Số tiền</span> <span class="font-bold text-red-600 text-base">{{ formatPrice(finalAmount) }}</span></div>
              <div class="flex justify-between items-center pt-2 border-t border-gray-200"><span class="text-gray-500">Nội dung chuyển khoản</span> <span class="font-black text-primary-600 bg-primary-50 px-2 py-0.5 rounded">{{ createdOrderCode }}</span></div>
            </div>
            
            <div v-else class="text-center p-4 bg-yellow-50 text-yellow-700 rounded-lg text-sm border border-yellow-200">
              Chưa có thông tin ngân hàng thanh toán. Vui lòng liên hệ shop.
            </div>

            <button @click="finishOrder" class="w-full btn-primary py-3 justify-center shadow-lg shadow-primary-500/20">
              Tôi đã thanh toán
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import api from '@/services/api'
import apiPublic from '@/services/apiPublic'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()
const { success } = useToast()

const form = reactive({
  ten_nguoi_nhan: authStore.user?.ho_ten || '',
  sdt_nguoi_nhan: authStore.user?.so_dien_thoai || '',
  dia_chi_nhan: authStore.user?.dia_chi || '',
  phuong_thuc_thanh_toan: 'cod',
  ghi_chu: ''
})

const userAddresses = ref([])
const selectedAddressId = ref(null)
const paymentMethods = ref([])
const bankAccounts = ref([])
const selectedBankId = ref(null)
const walletAccounts = ref([])
const selectedWalletId = ref(null)

const ma_giam_gia = ref('')
const discount = ref(0)
const couponMsg = ref('')
const couponValid = ref(false)
const orderLoading = ref(false)
const orderError = ref('')

const showBankModal = ref(false)
const createdOrderId = ref(null)
const createdOrderCode = ref('')

const shipping = computed(() => (cartStore.totalAmount || cartStore.tong_tien) >= 500000 ? 0 : 30000)
const finalAmount = computed(() => (cartStore.totalAmount || cartStore.tong_tien) - discount.value + shipping.value)

function formatPrice(p) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p) }

async function applyCoupon() {
  try {
    const res = await api.post('/coupons/validate', { ma: ma_giam_gia.value, tong_tien_don: (cartStore.totalAmount || cartStore.tong_tien) })
    discount.value = res.data.so_tien_giam
    couponMsg.value = `Giảm ${formatPrice(discount.value)}`
    couponValid.value = true
  } catch (e) {
    discount.value = 0
    couponMsg.value = e.response?.data?.detail || 'Mã không hợp lệ'
    couponValid.value = false
  }
}

function removeCoupon() {
  ma_giam_gia.value = ''
  discount.value = 0
  couponMsg.value = ''
  couponValid.value = false
}

const selectedBank = computed(() => {
  if (!selectedBankId.value || bankAccounts.value.length === 0) return bankAccounts.value[0] || null
  return bankAccounts.value.find(b => b.id === selectedBankId.value) || bankAccounts.value[0] || null
})

const selectedWallet = computed(() => {
  if (!selectedWalletId.value || walletAccounts.value.length === 0) return walletAccounts.value[0] || null
  return walletAccounts.value.find(w => w.id === selectedWalletId.value) || walletAccounts.value[0] || null
})

const qrCodeUrl = computed(() => {
  if (form.phuong_thuc_thanh_toan === 'bank_transfer' && selectedBank.value) {
    const bank = selectedBank.value
    return `https://img.vietqr.io/image/${bank.ma_ngan_hang}-${bank.so_tai_khoan}-compact.png?amount=${Math.round(finalAmount.value)}&addInfo=${createdOrderCode.value}&accountName=${encodeURIComponent(bank.chu_tai_khoan)}`
  }
  return ''
})

async function placeOrder() {
  if (cartStore.items.length === 0) {
    orderError.value = 'Giỏ hàng của bạn đang trống'
    return
  }

  const selectedAddr = userAddresses.value.find(a => a.id === selectedAddressId.value)
  if (!selectedAddr && userAddresses.value.length > 0) {
    orderError.value = 'Vui lòng chọn địa chỉ giao hàng'
    return
  }

  // Fallback to manual form if no addresses exist
  if (userAddresses.value.length === 0 && (!form.ten_nguoi_nhan || !form.sdt_nguoi_nhan || !form.dia_chi_nhan)) {
    orderError.value = 'Vui lòng điền đầy đủ thông tin giao hàng'
    return
  }

  orderLoading.value = true
  orderError.value = ''
  try {
    let payload = { ...form }
    
    if (selectedAddr) {
      payload.ten_nguoi_nhan = selectedAddr.ten_nguoi_nhan
      payload.sdt_nguoi_nhan = selectedAddr.so_dien_thoai
      payload.dia_chi_nhan = selectedAddr.dia_chi
    }
    
    if (ma_giam_gia.value && couponValid.value) payload.ma_giam_gia = ma_giam_gia.value
    const res = await api.post('/orders', payload)

    createdOrderId.value = res.data.id
    createdOrderCode.value = res.data.ma_don_hang
    if (form.phuong_thuc_thanh_toan === 'bank_transfer' || form.phuong_thuc_thanh_toan === 'momo' || form.phuong_thuc_thanh_toan === 'zalopay') {
      showBankModal.value = true
    } else {
      success('Đặt hàng thành công!')
      cartStore.reset()
      router.push('/orders')
    }
  } catch (e) {
    orderError.value = e.response?.data?.detail || 'Đặt hàng thất bại'
  } finally {
    orderLoading.value = false
  }
}

async function finishOrder() {
  try {
    if (createdOrderId.value) {
      await api.post(`/orders/${createdOrderId.value}/confirm-payment`)
    }
    showBankModal.value = false
    success('Đặt hàng và xác nhận thanh toán thành công!')
    cartStore.reset()
    router.push('/orders')
  } catch (e) {
    console.error('Confirm payment error:', e)
    // Still proceed but maybe show a different message
    showBankModal.value = false
    success('Đặt hàng thành công!')
    cartStore.reset()
    router.push('/orders')
  }
}

onMounted(async () => {
  try {
    const [allBanksRes, addressesRes] = await Promise.all([
      apiPublic.get('/banks/active'),
      api.get('/addresses')
    ])
    const allActive = allBanksRes.data || []
    userAddresses.value = addressesRes.data || []
    
    if (userAddresses.value.length > 0) {
      const def = userAddresses.value.find(a => a.la_mac_dinh)
      selectedAddressId.value = def ? def.id : userAddresses.value[0].id
    }
    
    bankAccounts.value = allActive.filter(a => a.loai === 'ngan_hang')
    walletAccounts.value = allActive.filter(a => a.loai === 'vi_dien_tu')
    const codEnabled = allActive.some(a => a.loai === 'cod')

    const methods = []

    if (codEnabled) {
      methods.push({
        value: 'cod',
        label: 'Thanh toán COD',
        desc: 'Thanh toán tiền mặt khi nhận hàng',
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/></svg>'
      })
    }

    if (bankAccounts.value.length > 0) {
      selectedBankId.value = bankAccounts.value[0].id
      methods.push({
        value: 'bank_transfer',
        label: 'Chuyển khoản ngân hàng',
        desc: 'Chuyển khoản qua ngân hàng hoặc quét mã QR',
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/></svg>'
      })
    }

    // Check for specific wallets in walletAccounts
    const hasMoMo = walletAccounts.value.some(w => w.ten_ngan_hang?.toLowerCase().includes('momo'))
    const hasZaloPay = walletAccounts.value.some(w => w.ten_ngan_hang?.toLowerCase().includes('zalopay'))

    if (hasMoMo) {
      methods.push({
        value: 'momo',
        label: 'Ví MoMo',
        desc: 'Thanh toán qua ứng dụng MoMo',
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 8v8m-4-4h8"/></svg>'
      })
    }

    if (hasZaloPay) {
      methods.push({
        value: 'zalopay',
        label: 'Ví ZaloPay',
        desc: 'Thanh toán qua ứng dụng ZaloPay',
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
      })
    }

    paymentMethods.value = methods
    if (walletAccounts.value.length > 0) {
      selectedWalletId.value = walletAccounts.value[0].id
    }
    if (paymentMethods.value.length > 0) {
      form.phuong_thuc_thanh_toan = paymentMethods.value[0].value
    }
  } catch (e) {
    console.error('Failed to load config', e)
  }
})
</script>

<style scoped>
.glass-card {
  backdrop-filter: blur(8px);
}
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e8191a;
  border-radius: 10px;
}
</style>

