<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Mobile Overlay -->
    <Transition name="fade">
      <div v-if="sidebarOpen" class="fixed inset-0 z-30 bg-black/50 lg:hidden" @click="sidebarOpen = false"></div>
    </Transition>

    <!-- Mobile Sidebar -->
    <aside
      :class="['fixed inset-y-0 left-0 z-40 w-64 bg-white flex flex-col border-r border-gray-100',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'transition-transform duration-300 ease-in-out lg:hidden']">
      <!-- User Card -->
      <div class="p-6 border-b border-gray-100 flex items-center justify-between">
        <RouterLink to="/" class="flex items-center gap-2 group">
          <div class="relative w-9 h-9 flex items-center justify-center shrink-0">
            <div class="absolute inset-0 bg-red-600 rounded-lg rotate-6 group-hover:rotate-12 transition-transform duration-500"></div>
            <div class="absolute inset-0 bg-black rounded-lg -rotate-3 transition-transform duration-500"></div>
            <svg class="relative w-5 h-5 text-white transform -rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </div>
          <span class="font-black text-xl text-gray-900 tracking-tighter">GIÀY<span style="color:#e8191a">ĐẸP</span></span>
        </RouterLink>
        <button @click="sidebarOpen = false" class="lg:hidden text-gray-400 hover:text-red-600 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        <RouterLink v-for="item in menuItems" :key="item.path" :to="item.path"
          :class="['flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200',
            isActive(item.path)
              ? 'bg-red-50 text-red-600 shadow-sm'
              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 hover:translate-x-1']"
          @click="sidebarOpen = false">
          <div v-html="item.icon" class="w-5 h-5 shrink-0" :class="{'text-red-500': isActive(item.path)}"></div>
          {{ item.label }}
          <span v-if="item.badge" class="ml-auto bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">{{ item.badge }}</span>
        </RouterLink>
      </nav>
      <div class="px-3 py-4 border-t border-gray-100 space-y-1">
        <RouterLink to="/" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-500 hover:bg-gray-50 hover:text-gray-900 transition-all">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
          Về cửa hàng
        </RouterLink>
        <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-red-500 hover:bg-red-50 transition-all">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          Đăng xuất
        </button>
      </div>
    </aside>

    <!-- Desktop Sidebar (FIXED) -->
    <aside class="hidden lg:block lg:fixed lg:inset-y-0 lg:left-0 lg:w-64 lg:h-screen bg-white border-r border-gray-100 z-10">
      <!-- User Card -->
      <div class="p-6 border-b border-gray-100">
        <RouterLink to="/" class="flex items-center gap-3 group">
          <div class="relative w-11 h-11 flex items-center justify-center shrink-0">
            <div class="absolute inset-0 bg-red-600 rounded-xl rotate-6 group-hover:rotate-12 transition-transform duration-500"></div>
            <div class="absolute inset-0 bg-black rounded-xl -rotate-3 group-hover:rotate-0 transition-transform duration-500"></div>
            <svg class="relative w-6 h-6 text-white transform -rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </div>
          <div class="flex flex-col leading-none">
            <span class="font-black text-xl tracking-tighter text-gray-900">GIÀY<span style="color:#e8191a">ĐẸP</span></span>
            <span class="text-[9px] font-black uppercase tracking-[0.3em] text-gray-400 mt-1">Premium Store</span>
          </div>
        </RouterLink>
      </div>

      <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        <p class="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Tài khoản</p>
        <RouterLink v-for="item in menuItems" :key="item.path" :to="item.path"
          :class="['flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200',
            isActive(item.path)
              ? 'bg-red-50 text-red-600 shadow-sm font-semibold'
              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 hover:translate-x-1']">
          <div v-html="item.icon" class="w-5 h-5 shrink-0" :class="{'text-red-500': isActive(item.path)}"></div>
          {{ item.label }}
          <span v-if="item.badge" class="ml-auto bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">{{ item.badge }}</span>
        </RouterLink>
      </nav>

      <div class="px-3 py-4 border-t border-gray-100 space-y-1">
        <RouterLink to="/" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:bg-gray-50 hover:text-gray-900 transition-all hover:translate-x-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
          Về cửa hàng
        </RouterLink>
        <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-red-400 hover:bg-red-50 hover:text-red-600 transition-all">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          Đăng xuất
        </button>
      </div>
    </aside>

    <!-- Main Content (offset by fixed sidebar) -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64">
      <!-- Top Header -->
      <header class="bg-white shadow-sm h-16 flex items-center justify-between px-6 shrink-0 sticky top-0 z-20">
        <div class="flex items-center gap-4">
          <button @click="sidebarOpen = true" class="lg:hidden text-gray-600 hover:text-gray-900 transition-colors p-1 rounded-lg hover:bg-gray-100">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
          </button>
          <h1 class="text-lg font-semibold text-gray-800">{{ pageTitle }}</h1>
        </div>
        <div class="flex items-center gap-3">
          <RouterLink to="/cart" class="relative p-2 text-gray-600 hover:text-red-600 hover:bg-gray-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
            <span v-if="cartStore.totalItems" class="absolute -top-0.5 -right-0.5 w-4 h-4 bg-red-500 text-white text-[10px] rounded-full flex items-center justify-center font-bold">{{ cartStore.totalItems }}</span>
          </RouterLink>
          <div class="flex items-center gap-2 pl-3 border-l border-gray-200">
            <div class="text-right hidden sm:block">
              <p class="text-sm font-medium text-gray-700">{{ authStore.user?.ho_ten }}</p>
              <p class="text-xs text-gray-400">Khách hàng</p>
            </div>
            <div class="w-8 h-8 rounded-full overflow-hidden bg-linear-to-r from-red-500 to-red-600 flex items-center justify-center text-white text-sm font-bold shadow-lg shadow-red-500/20">
              <img
                v-if="authStore.user?.anh_dai_dien"
                :src="avatarSrc"
                alt="Avatar"
                class="w-full h-full object-cover"
                @error="onAvatarImgError"
              />
              <span v-else class="relative z-10">{{ authStore.user?.ho_ten?.charAt(0) || 'U' }}</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 p-6">
        <RouterView v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" class="animate-fade-in" />
          </Transition>
        </RouterView>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const sidebarOpen = ref(false)

const menuItems = computed(() => [
  { path: '/account', label: 'Tổng quan', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>' },
  { path: '/account/orders', label: 'Đơn hàng', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>' },
  { path: '/account/coupons', label: 'Mã giảm giá', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/></svg>' },
  { path: '/account/wishlist', label: 'Yêu thích', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>', badge: wishlistStore.items?.length || null },
  { path: '/account/addresses', label: 'Địa chỉ nhận hàng', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>' },
  { path: '/account/profile', label: 'Hồ sơ cá nhân', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>' },
])

const pageTitles = {
  '/account': 'Tổng quan tài khoản',
  '/account/orders': 'Đơn hàng của tôi',
  '/account/coupons': 'Mã giảm giá',
  '/account/wishlist': 'Sản phẩm yêu thích',
  '/account/addresses': 'Địa chỉ nhận hàng',
  '/account/profile': 'Hồ sơ cá nhân',
}

const pageTitle = computed(() => {
  for (const [path, title] of Object.entries(pageTitles)) {
    if (route.path === path) return title
  }
  return 'Tài khoản'
})

const avatarSrc = computed(() => {
  const v = authStore.user?.anh_dai_dien
  if (!v) return ''
  if (typeof v === 'string' && v.startsWith('data:')) return v
  return `data:image/*;base64,${v}`
})

function onAvatarImgError() {
  // fallback handled by v-else
}


function isActive(path) {
  if (path === '/account') return route.path === '/account'
  return route.path.startsWith(path)
}

function handleLogout() {
  authStore.logout()
  cartStore.reset()
  wishlistStore.reset()
  router.push('/')
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.page-enter-active, .page-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to { opacity: 0; transform: translateY(-10px); }
</style>
