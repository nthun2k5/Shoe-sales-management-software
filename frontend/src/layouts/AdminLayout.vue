<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Mobile Overlay -->
    <Transition name="fade">
      <div v-if="sidebarOpen" class="fixed inset-0 z-30 bg-black/50 lg:hidden" @click="sidebarOpen = false"></div>
    </Transition>

    <!-- Mobile Sidebar (only for mobile) -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 z-40 w-64 bg-linear-to-b from-surface to-surface-light text-white flex flex-col',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'transition-transform duration-300 ease-in-out lg:hidden'
      ]"
    >
      <!-- Logo -->
      <div class="flex items-center justify-between h-16 px-6 border-b border-white/10 shrink-0">
        <RouterLink to="/admin" class="flex items-center gap-3 group" @click="sidebarOpen = false">
          <div class="relative w-9 h-9 flex items-center justify-center">
            <div class="absolute inset-0 bg-red-600 rounded-lg rotate-6"></div>
            <div class="absolute inset-0 bg-white/20 rounded-lg -rotate-3 backdrop-blur-sm"></div>
            <svg class="relative w-5 h-5 text-white transform -rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </div>
          <span class="text-lg font-bold text-white tracking-tight">LBG <span class="text-red-500">ADMIN</span></span>
        </RouterLink>
        <button @click="sidebarOpen = false" class="text-gray-400 hover:text-white transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>



      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        <p class="px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Tổng quan</p>
        <RouterLink v-for="item in mainMenu" :key="item.path" :to="item.path"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200',
            isActive(item.path)
              ? 'bg-white/10 text-white shadow-lg shadow-white/5'
              : 'text-gray-300 hover:bg-white/5 hover:text-white hover:translate-x-1'
          ]"
          @click="sidebarOpen = false"
        >
          <div v-html="item.icon" class="w-5 h-5 shrink-0" :class="{'text-primary-400': isActive(item.path)}"></div>
          {{ item.label }}
          <span v-if="item.badge" class="ml-auto bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">{{ item.badge }}</span>
        </RouterLink>

        <p class="px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 mt-6">Quản lý</p>
        <RouterLink v-for="item in manageMenu" :key="item.path" :to="item.path"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200',
            isActive(item.path)
              ? 'bg-white/10 text-white shadow-lg shadow-white/5'
              : 'text-gray-300 hover:bg-white/5 hover:text-white hover:translate-x-1'
          ]"
          @click="sidebarOpen = false"
        >
          <div v-html="item.icon" class="w-5 h-5 shrink-0" :class="{'text-primary-400': isActive(item.path)}"></div>
          {{ item.label }}
        </RouterLink>

        <p class="px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 mt-6">Hệ thống</p>
        <RouterLink v-for="item in systemMenu" :key="item.path" :to="item.path"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200',
            isActive(item.path)
              ? 'bg-white/10 text-white shadow-lg shadow-white/5'
              : 'text-gray-300 hover:bg-white/5 hover:text-white hover:translate-x-1'
          ]"
          @click="sidebarOpen = false"
        >
          <div v-html="item.icon" class="w-5 h-5 shrink-0" :class="{'text-primary-400': isActive(item.path)}"></div>
          {{ item.label }}
        </RouterLink>
      </nav>

      <!-- Bottom Actions -->
      <div class="px-3 py-4 border-t border-white/10 shrink-0 space-y-1">
        <RouterLink to="/" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:bg-white/5 hover:text-white transition-all duration-200 hover:translate-x-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
          Về cửa hàng
        </RouterLink>
        <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-red-400 hover:bg-red-900/30 hover:text-red-300 transition-all duration-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          Đăng xuất
        </button>
      </div>
    </aside>

    <!-- Desktop Sidebar (FIXED) -->
    <aside class="hidden lg:block lg:fixed lg:inset-y-0 lg:left-0 lg:w-64 lg:h-screen bg-linear-to-b from-surface to-surface-light text-white z-10">
      <!-- Logo -->
      <div class="flex items-center h-16 px-6 border-b border-white/10 shrink-0">
        <RouterLink to="/admin" class="flex items-center gap-3 group">
          <div class="relative w-9 h-9 flex items-center justify-center">
            <div class="absolute inset-0 bg-red-600 rounded-lg rotate-6 group-hover:rotate-12 transition-transform duration-500"></div>
            <div class="absolute inset-0 bg-white/20 rounded-lg -rotate-3 backdrop-blur-sm transition-transform duration-500"></div>
            <svg class="relative w-5 h-5 text-white transform -rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </div>
          <span class="text-lg font-bold text-white tracking-tight">LBG <span class="text-red-500">ADMIN</span></span>
        </RouterLink>
      </div>



      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        <RouterLink v-for="item in mainMenu" :key="item.path" :to="item.path"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200',
            isActive(item.path)
              ? 'bg-white/10 text-white shadow-lg shadow-white/5'
              : 'text-gray-300 hover:bg-white/5 hover:text-white hover:translate-x-1'
          ]"
        >
          <div v-html="item.icon" class="w-5 h-5 shrink-0" :class="{'text-primary-400': isActive(item.path)}"></div>
          {{ item.label }}
          <span v-if="item.badge" class="ml-auto bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">{{ item.badge }}</span>
        </RouterLink>


        <RouterLink v-for="item in manageMenu" :key="item.path" :to="item.path"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200',
            isActive(item.path)
              ? 'bg-white/10 text-white shadow-lg shadow-white/5'
              : 'text-gray-300 hover:bg-white/5 hover:text-white hover:translate-x-1'
          ]"
        >
          <div v-html="item.icon" class="w-5 h-5 shrink-0" :class="{'text-primary-400': isActive(item.path)}"></div>
          {{ item.label }}
        </RouterLink>


        <RouterLink v-for="item in systemMenu" :key="item.path" :to="item.path"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200',
            isActive(item.path)
              ? 'bg-white/10 text-white shadow-lg shadow-white/5'
              : 'text-gray-300 hover:bg-white/5 hover:text-white hover:translate-x-1'
          ]"
        >
          <div v-html="item.icon" class="w-5 h-5 shrink-0" :class="{'text-primary-400': isActive(item.path)}"></div>
          {{ item.label }}
        </RouterLink>
      </nav>

      <!-- Bottom Actions -->
      <div class="px-3 py-4 border-t border-white/10 shrink-0 space-y-1">
        <RouterLink to="/" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:bg-white/5 hover:text-white transition-all duration-200 hover:translate-x-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
          Về cửa hàng
        </RouterLink>
        <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-red-400 hover:bg-red-900/30 hover:text-red-300 transition-all duration-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          Đăng xuất
        </button>
      </div>
    </aside>

    <!-- Main Content (offset by fixed sidebar on desktop) -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64">
      <!-- Top Header -->
      <header class="bg-white shadow-sm h-16 flex items-center justify-between px-6 shrink-0 sticky top-0 z-20">
        <div class="flex items-center gap-4">
          <button @click="sidebarOpen = true" class="lg:hidden text-gray-600 hover:text-gray-900 transition-colors p-1 rounded-lg hover:bg-gray-100">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
          </button>
          <h1 class="text-lg font-semibold text-gray-800 animate-fade-in">{{ pageTitle }}</h1>
        </div>

        <div class="flex items-center gap-4">
          <RouterLink to="/admin/products/new" class="hidden sm:flex items-center gap-2 px-4 py-2 bg-primary-50 text-primary-700 rounded-lg text-sm font-medium hover:bg-primary-100 transition-all duration-200 hover:scale-105">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            Thêm sản phẩm
          </RouterLink>

          <button class="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.607a2 2 0 01-.599-1.416V11a6 6 0 10-12 0v3.977a2 2 0 01-.601 1.416L5 17h10m5 0v-2a2 2 0 00-2-2h-2a2 2 0 00-2 2v2"/></svg>
            <span class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-bold">3</span>
          </button>

          <div class="flex items-center gap-3 pl-4 border-l border-gray-200">
            <div class="text-right hidden sm:block">
              <p class="text-sm font-medium text-gray-700">{{ authStore.user?.ho_ten }}</p>
              <p class="text-xs text-gray-500">Quản trị viên</p>
            </div>
            <div class="w-9 h-9 rounded-full bg-linear-to-r from-primary-500 to-primary-700 flex items-center justify-center text-white text-sm font-bold shadow-lg shadow-primary-500/30 transition-transform hover:scale-110 cursor-pointer">
              {{ authStore.user?.ho_ten?.charAt(0) || 'A' }}
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

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const sidebarOpen = ref(false)

const mainMenu = [
  {
    path: '/admin',
    label: 'Dashboard',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>'
  },
  {
    path: '/admin/analytics',
    label: 'Thống kê',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6M15 19v-4a2 2 0 00-2-2h-2a2 2 0 00-2 2v4M21 19V9a2 2 0 00-2-2h-2a2 2 0 00-2 2v10"/></svg>'
  },
]

const manageMenu = [
  {
    path: '/admin/products',
    label: 'Sản phẩm',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>'
  },
  {
    path: '/admin/categories',
    label: 'Danh mục',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 10h16M4 14h16M4 18h16"/></svg>'
  },
  {
    path: '/admin/orders',
    label: 'Đơn hàng',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>'
  },
  {
    path: '/admin/users',
    label: 'Người dùng',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>'
  },
  {
    path: '/admin/coupons',
    label: 'Mã giảm giá',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/></svg>'
  },
  {
    path: '/admin/banks',
    label: 'Tài khoản nhận tiền',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/></svg>'
  },
]

const systemMenu = [
  {
    path: '/admin/logs',
    label: 'Nhật ký',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 6v6h4.5m4.5 0a9 9 0 110 18 9 9 0 010-18z"/></svg>'
  },
]

const pageTitles = {
  '/admin': 'Dashboard',
  '/admin/analytics': 'Báo cáo & Thống kê',
  '/admin/products': 'Quản lý sản phẩm',
  '/admin/categories': 'Quản lý danh mục',
  '/admin/orders': 'Quản lý đơn hàng',
  '/admin/users': 'Quản lý người dùng',
  '/admin/coupons': 'Mã giảm giá',
  '/admin/coupons': 'Mã giảm giá',
  '/admin/logs': 'Nhật ký hoạt động',
  '/admin/banks': 'Tài khoản nhận tiền',
}

const pageTitle = computed(() => {
  for (const [path, title] of Object.entries(pageTitles)) {
    if (route.path === path) return title
  }
  if (route.path.includes('/products/new')) return 'Thêm sản phẩm'
  if (route.path.includes('/edit')) return 'Chỉnh sửa sản phẩm'
  return 'Quản trị'
})

function isActive(path) {
  if (path === '/admin') return route.path === '/admin'
  return route.path.startsWith(path)
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
