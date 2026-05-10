<template>
  <div class="min-h-screen flex flex-col" style="background:#f5f5f5">

    <!-- Top announcement bar -->
    <div class="bg-[#0a0a0a] text-white border-b border-white/5 relative z-60 overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-center md:justify-between h-9 text-[11px] font-bold uppercase tracking-widest">
          <!-- Left side: Sliding Announcements -->
          <div class="flex items-center gap-3 overflow-hidden h-full relative flex-1 justify-center md:justify-start">
            <Transition name="slide-up" mode="out-in">
              <div :key="currentAnnounceIdx" class="flex items-center gap-2 whitespace-nowrap">
                <span class="text-base leading-none">{{ announcements[currentAnnounceIdx].icon }}</span>
                <span class="text-gray-300">{{ announcements[currentAnnounceIdx].text }}</span>
              </div>
            </Transition>
          </div>

          <!-- Right side: Quick Links (Desktop only) -->
          <div class="hidden md:flex items-center gap-6 text-gray-400">
            <RouterLink to="/lien-he" class="hover:text-red-500 transition-colors">Trợ giúp</RouterLink>
            <span class="w-px h-3 bg-white/10"></span>
            <RouterLink to="/huong-dan-mua-hang" class="hover:text-red-500 transition-colors">Tra cứu đơn hàng</RouterLink>
            <span class="w-px h-3 bg-white/10"></span>
            <div class="flex items-center gap-2 group cursor-pointer">
              <span class="text-red-500">VN</span>
              <svg class="w-3 h-3 group-hover:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-width="3"/></svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Header -->
    <header :class="['bg-white sticky top-0 z-50 transition-all duration-300 border-b border-gray-100', isScrolled ? 'shadow-md' : '']">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-20 gap-4 lg:gap-8">
          
          <!-- Logo -->
          <RouterLink to="/" class="flex items-center gap-3 shrink-0 group">
            <div class="relative w-11 h-11 lg:w-13 lg:h-13 flex items-center justify-center shrink-0">
              <div class="absolute inset-0 bg-red-600 rounded-xl rotate-6 group-hover:rotate-12 transition-transform duration-500"></div>
              <div class="absolute inset-0 bg-black rounded-xl -rotate-3 group-hover:rotate-0 transition-transform duration-500"></div>
              <svg class="relative w-7 h-7 lg:w-8 lg:h-8 text-white transform -rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <div class="hidden sm:flex flex-col leading-none">
              <span class="font-black text-xl lg:text-2xl tracking-tighter" style="color:#111;line-height:1">
                GIÀY<span style="color:#e8191a">ĐẸP</span>
              </span>
              <span class="text-[9px] lg:text-[10px] font-black uppercase tracking-[0.3em] text-gray-400 mt-1">Premium Store</span>
            </div>
          </RouterLink>

          <!-- Desktop Navigation -->
          <nav class="hidden lg:flex items-center justify-center gap-5 xl:gap-8 flex-1 px-4">
            <RouterLink v-for="(link,i) in navLinks" :key="link.path" :to="link.path"
              class="text-[13px] xl:text-[14px] font-bold text-gray-800 hover:text-red-600 uppercase tracking-wider transition-colors relative group py-2 whitespace-nowrap"
              :class="{'text-red-600': $route.path === link.path}">
              {{ link.label }}
              <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-red-600 transition-all group-hover:w-full"
                    :class="{'w-full': $route.path === link.path}"></span>
            </RouterLink>
          </nav>

          <!-- Right Actions -->
          <div class="flex items-center justify-end gap-3 lg:gap-4 shrink-0">
            
            <!-- Search bar -->
            <div class="hidden lg:flex relative group">
              <input v-model="searchQuery" @keyup.enter="doSearch" type="text"
                placeholder="Tìm sản phẩm..."
                class="w-48 xl:w-64 bg-gray-50 border-2 border-transparent focus:border-red-600/20 focus:bg-white focus:w-64 xl:focus:w-80 rounded-2xl py-2.5 pl-11 pr-4 text-sm font-medium transition-all duration-500 outline-none shadow-xs group-hover:shadow-md" />
              <button @click="doSearch" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-red-600 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
              </button>
            </div>

            <div class="w-px h-6 bg-gray-200 hidden lg:block mx-1"></div>

            <!-- Wishlist -->
            <button @click="handleProtectedClick('/wishlist')"
              class="relative flex items-center justify-center w-10 h-10 rounded-full bg-gray-50 text-gray-600 hover:text-red-600 hover:bg-red-50 transition-colors group">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              </svg>
              <span v-if="authStore.isLoggedIn && wishlistStore.items?.length > 0"
                class="absolute -top-1 -right-1 w-4 h-4 text-white text-[10px] rounded-full flex items-center justify-center font-bold shadow-sm"
                style="background:#e8191a">{{ wishlistStore.items.length }}</span>
            </button>

            <!-- Cart -->
            <button @click="cartStore.toggleDrawer(true)"
              class="relative flex items-center justify-center w-10 h-10 rounded-full bg-gray-50 text-gray-600 hover:text-red-600 hover:bg-red-50 transition-colors group">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
              </svg>
              <span v-if="authStore.isLoggedIn && cartStore.totalItems > 0"
                class="absolute -top-1 -right-1 w-4 h-4 text-white text-[10px] rounded-full flex items-center justify-center font-bold shadow-sm"
                style="background:#e8191a">{{ cartStore.totalItems }}</span>
            </button>

            <!-- Account Menu -->
            <div class="relative" ref="userMenuRef">
              <button @click="showUserMenu = !showUserMenu"
                class="flex items-center justify-center p-1 rounded-full hover:bg-gray-100 transition-colors">
                <div v-if="authStore.isLoggedIn" class="w-9 h-9 rounded-full overflow-hidden flex items-center justify-center text-white text-sm font-bold shadow-sm" style="background:#e8191a">
                  <img
                    v-if="authStore.user?.anh_dai_dien"
                    :src="avatarSrc"
                    alt="Avatar"
                    class="w-full h-full object-cover"
                    @error="onAvatarImgError"
                  />
                  <span v-else class="relative z-10">
                    {{ authStore.user?.ho_ten?.charAt(0) || 'U' }}
                  </span>
                </div>
                <div v-else class="w-9 h-9 rounded-full flex items-center justify-center text-gray-600 bg-gray-50 border border-gray-100 shadow-sm">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
              </button>
              
              <Transition name="dropdown">
                <div v-if="showUserMenu" class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-100 py-1 z-50">
                  <template v-if="authStore.isLoggedIn">
                    <div class="px-4 py-3 border-b border-gray-100">
                      <p class="text-sm font-bold text-gray-900">{{ authStore.user?.ho_ten }}</p>
                      <p class="text-xs text-gray-400 mt-0.5 line-clamp-1">{{ authStore.user?.email }}</p>
                    </div>
                    <RouterLink v-if="authStore.isAdmin" to="/admin" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 transition-colors font-medium" @click="showUserMenu=false">
                      Trang quản trị
                    </RouterLink>
                    <RouterLink to="/account" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 transition-colors" @click="showUserMenu=false">
                      Tài khoản của tôi
                    </RouterLink>
                    <RouterLink to="/account/orders" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 transition-colors" @click="showUserMenu=false">
                      Đơn hàng
                    </RouterLink>
                    <div class="border-t border-gray-100 mt-1 pt-1">
                      <button @click="handleLogout" class="w-full text-left flex items-center gap-3 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors font-medium">
                        Đăng xuất
                      </button>
                    </div>
                  </template>
                  <template v-else>
                    <RouterLink to="/login" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 transition-colors font-medium" @click="showUserMenu=false">
                      Đăng nhập
                    </RouterLink>
                    <RouterLink to="/register" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 transition-colors font-medium" @click="showUserMenu=false">
                      Đăng ký
                    </RouterLink>
                  </template>
                </div>
              </Transition>
            </div>

            <!-- Mobile menu btn -->
            <button @click="mobileMenuOpen=!mobileMenuOpen" class="lg:hidden p-2 text-gray-600 hover:text-red-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Menu -->
      <Transition name="mobile-menu">
        <div v-if="mobileMenuOpen" class="lg:hidden bg-white border-t border-gray-100">
          <div class="px-4 py-2 space-y-1">
            <RouterLink v-for="link in navLinks" :key="link.path" :to="link.path"
              class="block px-2 py-3 text-sm font-semibold text-gray-700 hover:text-red-600 border-b border-gray-50 transition-colors"
              @click="mobileMenuOpen=false">
              {{ link.label }}
            </RouterLink>
          </div>
        </div>
      </Transition>
    </header>

    <!-- Main Content -->
    <main class="flex-1">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>

    <!-- Cart Drawer -->
    <Teleport to="body">
      <div v-if="cartStore.isDrawerOpen" class="fixed inset-0 z-60 flex justify-end">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm transition-opacity" @click="cartStore.toggleDrawer(false)"></div>
        <!-- Panel -->
        <div class="relative w-screen max-w-md bg-white shadow-2xl flex flex-col transform transition-transform duration-500 ease-in-out">
          <div class="flex items-center justify-between px-6 py-6 border-b border-gray-100">
            <h2 class="text-xl font-black text-gray-900 tracking-tight">Giỏ hàng ({{ cartStore.totalItems }})</h2>
            <button @click="cartStore.toggleDrawer(false)" class="p-2 text-gray-400 hover:text-red-600"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-width="2"/></svg></button>
          </div>
          <div class="flex-1 overflow-y-auto px-6 py-6 custom-scrollbar">
            <div v-if="cartStore.items.length === 0" class="h-full flex flex-col items-center justify-center text-center text-gray-400">
              <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" stroke-width="1.5"/></svg>
              <p>Giỏ hàng đang trống</p>
            </div>
            <div v-else class="space-y-6">
              <div v-for="item in cartStore.items" :key="item.id" class="flex gap-4">
                <div class="w-20 h-20 bg-gray-50 rounded-xl overflow-hidden shrink-0">
                  <img v-if="item.anh_san_pham" :src="item.anh_san_pham" class="w-full h-full object-cover" />
                  <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  </div>
                </div>
                <div class="flex-1">
                  <div class="flex justify-between items-start">
                    <h3 class="text-sm font-bold text-gray-900 line-clamp-1">{{ item.ten_san_pham }}</h3>
                    <button @click="cartStore.removeItem(item.id)" class="text-gray-300 hover:text-red-600"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 7l-1 12H6L5 7m5 4v6m4-6v6M4 7h16M10 4h4" stroke-width="2"/></svg></button>
                  </div>
                  <p v-if="item.kich_thuoc" class="text-xs text-gray-400 mt-1">Size: {{ item.kich_thuoc }}</p>
                  <div class="flex items-center justify-between mt-2">
                    <div class="flex items-center border rounded-lg h-8">
                      <button @click="updateDrawerQty(item.id, item.so_luong - 1)" class="w-8 hover:bg-gray-50">−</button>
                      <span class="w-8 text-center text-xs font-bold">{{ item.so_luong }}</span>
                      <button @click="updateDrawerQty(item.id, item.so_luong + 1)" class="w-8 hover:bg-gray-50">+</button>
                    </div>
                    <span class="font-bold text-gray-900 text-sm">{{ formatPrice(item.thanh_tien) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="cartStore.items.length > 0" class="p-6 border-t bg-gray-50/50">
            <div class="flex justify-between items-center mb-6">
              <span class="text-gray-500">Tạm tính</span>
              <span class="text-2xl font-black text-red-600">{{ formatPrice(cartStore.totalAmount) }}</span>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <RouterLink to="/cart" @click="cartStore.toggleDrawer(false)" class="px-4 py-3 border border-gray-200 rounded-xl text-center text-sm font-bold hover:bg-white transition-colors">Xem giỏ hàng</RouterLink>
              <RouterLink to="/checkout" @click="cartStore.toggleDrawer(false)" class="px-4 py-3 bg-red-600 text-white rounded-xl text-center text-sm font-bold hover:bg-red-700 transition-colors shadow-lg shadow-red-500/20">Thanh toán</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Footer -->
    <footer class="bg-[#0d0d0d] text-gray-400 mt-auto relative overflow-hidden">
      <!-- Decorative gradient line -->
      <div class="h-1 bg-linear-to-r from-red-700 via-red-500 to-red-700"></div>

      <!-- Newsletter Banner -->
      <div class="bg-linear-to-r from-red-700 via-red-600 to-red-700 relative">
        <div class="absolute inset-0 opacity-10" style="background-image:url('data:image/svg+xml,%3Csvg width=60 height=60 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cpath d=%22M0 0h60v60H0z%22 fill=%22none%22/%3E%3Cpath d=%22M30 0v60M0 30h60%22 stroke=%22white%22 stroke-width=%221%22/%3E%3C/svg%3E')"></div>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
          <div class="text-center md:text-left">
            <h3 class="text-white font-black text-xl tracking-tight">📩 Nhận ưu đãi độc quyền</h3>
            <p class="text-red-200 text-sm mt-1">Đăng ký email — nhận ngay voucher giảm 10% cho đơn đầu tiên</p>
          </div>
          <form @submit.prevent class="flex gap-2 w-full md:w-auto">
            <input type="email" placeholder="Nhập email của bạn..."
              class="flex-1 md:w-72 px-5 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 text-sm outline-none focus:border-white/50 focus:bg-white/15 transition-all backdrop-blur-sm" />
            <button type="submit" class="px-6 py-3 bg-white text-red-600 font-bold text-sm rounded-xl hover:bg-red-50 transition-all shadow-lg shadow-black/10 whitespace-nowrap">
              Đăng ký
            </button>
          </form>
        </div>
      </div>

      <!-- Main Footer -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">

          <!-- Brand Column -->
          <div>
            <RouterLink to="/" class="flex items-center gap-3 mb-5 group">
              <div class="relative w-10 h-10 flex items-center justify-center shrink-0">
                <div class="absolute inset-0 bg-red-600 rounded-xl rotate-6 group-hover:rotate-12 transition-transform duration-500"></div>
                <div class="absolute inset-0 bg-white/5 rounded-xl -rotate-3"></div>
                <svg class="relative w-6 h-6 text-white transform -rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
              </div>
              <div class="flex flex-col leading-none">
                <span class="font-black text-xl text-white tracking-tighter">GIÀY<span class="text-red-500">ĐẸP</span></span>
                <span class="text-[9px] font-bold uppercase tracking-[0.3em] text-gray-600 mt-0.5">Premium Store</span>
              </div>
            </RouterLink>
            <p class="text-sm leading-relaxed mb-5 text-gray-500">Thương hiệu giày dép uy tín — Chính hãng 100%, giá tốt nhất thị trường.</p>
            <div class="space-y-2.5 text-sm text-gray-500">
              <p class="flex items-center gap-2.5">
                <svg class="w-4 h-4 shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                123 Đường Giày Đẹp, Q.1, TP.HCM
              </p>
              <p class="flex items-center gap-2.5">
                <svg class="w-4 h-4 shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                <span class="text-white font-semibold">0123 456 789</span>
              </p>
              <p class="flex items-center gap-2.5">
                <svg class="w-4 h-4 shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                contact@giaydep.vn
              </p>
            </div>
            <div class="flex gap-2 mt-5">
              <a v-for="s in socialLinks" :key="s.name" :href="s.href" 
                class="w-9 h-9 rounded-lg bg-white/5 hover:bg-red-600 flex items-center justify-center text-white transition-all duration-300 hover:scale-110 hover:-translate-y-0.5"
                v-html="s.icon"></a>
            </div>
          </div>

          <!-- Quick Links -->
          <div>
            <h4 class="text-white font-bold mb-5 text-sm uppercase tracking-widest relative pb-3">
              Danh mục
              <span class="absolute bottom-0 left-0 w-8 h-0.5 bg-red-600 rounded-full"></span>
            </h4>
            <ul class="space-y-3 text-sm">
              <li><RouterLink to="/" class="text-gray-500 hover:text-white hover:pl-1.5 transition-all duration-200 flex items-center gap-1.5 group"><span class="w-0 overflow-hidden group-hover:w-3 transition-all duration-200 text-red-500">→</span> Trang chủ</RouterLink></li>
              <li><RouterLink to="/products" class="text-gray-500 hover:text-white hover:pl-1.5 transition-all duration-200 flex items-center gap-1.5 group"><span class="w-0 overflow-hidden group-hover:w-3 transition-all duration-200 text-red-500">→</span> Sản phẩm</RouterLink></li>
              <li><RouterLink to="/about" class="text-gray-500 hover:text-white hover:pl-1.5 transition-all duration-200 flex items-center gap-1.5 group"><span class="w-0 overflow-hidden group-hover:w-3 transition-all duration-200 text-red-500">→</span> Giới thiệu</RouterLink></li>
              <li><RouterLink to="/lien-he" class="text-gray-500 hover:text-white hover:pl-1.5 transition-all duration-200 flex items-center gap-1.5 group"><span class="w-0 overflow-hidden group-hover:w-3 transition-all duration-200 text-red-500">→</span> Liên hệ</RouterLink></li>
            </ul>
          </div>

          <!-- Support -->
          <div>
            <h4 class="text-white font-bold mb-5 text-sm uppercase tracking-widest relative pb-3">
              Hỗ trợ
              <span class="absolute bottom-0 left-0 w-8 h-0.5 bg-red-600 rounded-full"></span>
            </h4>
            <ul class="space-y-3 text-sm">
              <li><RouterLink to="/faq" class="text-gray-500 hover:text-white hover:pl-1.5 transition-all duration-200 flex items-center gap-1.5 group"><span class="w-0 overflow-hidden group-hover:w-3 transition-all duration-200 text-red-500">→</span> Câu hỏi thường gặp</RouterLink></li>
              <li><RouterLink to="/policies" class="text-gray-500 hover:text-white hover:pl-1.5 transition-all duration-200 flex items-center gap-1.5 group"><span class="w-0 overflow-hidden group-hover:w-3 transition-all duration-200 text-red-500">→</span> Chính sách đổi trả</RouterLink></li>
              <li><RouterLink to="/huong-dan-mua-hang" class="text-gray-500 hover:text-white hover:pl-1.5 transition-all duration-200 flex items-center gap-1.5 group"><span class="w-0 overflow-hidden group-hover:w-3 transition-all duration-200 text-red-500">→</span> Hướng dẫn mua hàng</RouterLink></li>
              <li><RouterLink to="/bang-size-giay" class="text-gray-500 hover:text-white hover:pl-1.5 transition-all duration-200 flex items-center gap-1.5 group"><span class="w-0 overflow-hidden group-hover:w-3 transition-all duration-200 text-red-500">→</span> Bảng size giày</RouterLink></li>
            </ul>
          </div>

          <!-- Payment & Hours -->
          <div>
            <h4 class="text-white font-bold mb-5 text-sm uppercase tracking-widest relative pb-3">
              Thanh toán
              <span class="absolute bottom-0 left-0 w-8 h-0.5 bg-red-600 rounded-full"></span>
            </h4>
            <p class="text-sm text-gray-500 mb-3">Chấp nhận đa dạng hình thức thanh toán</p>
            <div class="flex flex-wrap gap-2 mb-6">
              <span v-for="p in ['VISA','MasterCard','Momo','ZaloPay','COD','VNPay']" :key="p"
                class="text-[10px] px-2.5 py-1.5 rounded-md font-bold bg-white/5 text-gray-400 border border-white/5">{{ p }}</span>
            </div>
            <div class="p-4 rounded-xl bg-white/5 border border-white/5">
              <p class="text-xs text-gray-500 mb-1.5 font-medium">Giờ hoạt động</p>
              <p class="text-white text-sm font-bold">T2 - CN: 8:00 – 22:00</p>
              <p class="text-xs text-gray-500 mt-1">Hỗ trợ online 24/7</p>
            </div>
          </div>
        </div>

        <!-- Bottom Bar -->
        <div class="border-t border-white/5 mt-12 pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <p class="text-xs text-gray-600">© 2026 Giày Đẹp Store. All rights reserved.</p>
          <div class="flex items-center gap-5 text-xs text-gray-600">
            <RouterLink to="/chinh-sach-bao-mat" class="hover:text-white transition-colors">Chính sách bảo mật</RouterLink>
            <span class="w-1 h-1 rounded-full bg-gray-700"></span>
            <RouterLink to="/dieu-khoan" class="hover:text-white transition-colors">Điều khoản sử dụng</RouterLink>
            <span class="w-1 h-1 rounded-full bg-gray-700"></span>
            <RouterLink to="/policies" class="hover:text-white transition-colors">Chính sách đổi trả</RouterLink>
          </div>
        </div>
      </div>
    </footer>

    <!-- Floating Contact Buttons -->
    <div class="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
      <!-- Chat Tooltip -->
      <Transition name="fade-slide">
        <div v-if="showChatTip" class="bg-gray-900 text-white text-xs font-bold px-3 py-2 rounded-xl shadow-lg whitespace-nowrap mr-1">
          💬 Chat tư vấn ngay!
        </div>
      </Transition>

      <!-- Chat Button -->
      <button id="float-chat-btn"
        @mouseenter="showChatTip = true" @mouseleave="showChatTip = false"
        @click="openChat"
        class="w-14 h-14 bg-red-600 text-white rounded-2xl shadow-2xl shadow-red-500/40 hover:bg-red-700 hover:scale-110 transition-all duration-300 flex items-center justify-center relative group"
        title="Chat tư vấn">
        <!-- Pulse ring -->
        <div class="absolute inset-0 bg-red-500 rounded-2xl animate-ping opacity-30"></div>
        <!-- Icon -->
        <svg v-if="!chatOpen" class="w-7 h-7 relative" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>
        <svg v-else class="w-6 h-6 relative" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
        <!-- Notification badge -->
        <span class="absolute -top-1 -right-1 w-5 h-5 bg-yellow-400 text-gray-900 text-[10px] font-black rounded-full flex items-center justify-center shadow">1</span>
      </button>
    </div>

    <!-- Chat Window -->
    <Teleport to="body">
      <Transition name="chat-window">
        <div v-if="chatOpen"
          class="fixed bottom-28 right-6 z-50 w-80 bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden flex flex-col"
          style="max-height: 420px;">
          <!-- Header -->
          <div class="bg-red-600 px-4 py-4 flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center shrink-0">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
            </div>
            <div class="flex-1">
              <p class="text-white font-bold text-sm">Giày Đẹp Support</p>
              <div class="flex items-center gap-1.5 mt-0.5">
                <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                <span class="text-white/80 text-xs">Đang hoạt động</span>
              </div>
            </div>
            <button @click="chatOpen = false" class="text-white/70 hover:text-white transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>
          <!-- Messages -->
          <div class="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
            <div class="flex items-end gap-2">
              <div class="w-7 h-7 rounded-full bg-red-100 flex items-center justify-center shrink-0">
                <span class="text-xs">👟</span>
              </div>
              <div class="bg-white rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm max-w-[80%]">
                <p class="text-sm text-gray-800">Xin chào! Tôi có thể giúp gì cho bạn? 😊</p>
                <p class="text-[10px] text-gray-400 mt-1">Giày Đẹp • Vừa xong</p>
              </div>
            </div>
            <div class="flex items-end gap-2">
              <div class="w-7 h-7 rounded-full bg-red-100 flex items-center justify-center shrink-0">
                <span class="text-xs">👟</span>
              </div>
              <div class="bg-white rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm max-w-[80%]">
                <p class="text-sm text-gray-800">Bạn có thể hỏi về sản phẩm, size giày, hoặc đơn hàng nhé!</p>
                <p class="text-[10px] text-gray-400 mt-1">Giày Đẹp • Vừa xong</p>
              </div>
            </div>
            <!-- Quick replies -->
            <div class="flex flex-wrap gap-2 pt-1">
              <button v-for="q in quickReplies" :key="q" @click="sendQuickReply(q)"
                class="px-3 py-1.5 bg-red-50 text-red-600 text-xs font-bold rounded-full border border-red-100 hover:bg-red-100 transition-colors">
                {{ q }}
              </button>
            </div>
          </div>
          <!-- Input -->
          <div class="p-3 border-t border-gray-100 flex gap-2">
            <input v-model="chatMessage" @keyup.enter="sendChat"
              type="text" placeholder="Nhập tin nhắn..."
              class="flex-1 px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:border-red-400 transition-colors" />
            <button @click="sendChat"
              class="w-9 h-9 bg-red-600 text-white rounded-xl flex items-center justify-center hover:bg-red-700 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'

import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const { success } = useToast()

const avatarSrc = computed(() => {
  const v = authStore.user?.anh_dai_dien
  if (!v) return ''
  if (typeof v === 'string' && v.startsWith('data:')) return v
  // backend đang lưu base64 thuần
  return `data:image/*;base64,${v}`
})

function onAvatarImgError() {
  // fallback handled by v-else
}

const searchQuery = ref('')

const showUserMenu = ref(false)
const mobileMenuOpen = ref(false)
const userMenuRef = ref(null)
const isScrolled = ref(false)
const chatOpen = ref(false)
const showChatTip = ref(false)
const chatMessage = ref('')

const announcements = [
  { icon: '🚚', text: 'Miễn phí vận chuyển cho đơn hàng từ 500K' },
  { icon: '🎁', text: 'Đổi trả dễ dàng trong vòng 30 ngày' },
  { icon: '⭐', text: 'Cam kết hàng chính hãng 100%' },
  { icon: '⚡', text: 'Giao hàng hỏa tốc trong 2h tại TP.HCM' }
]
const currentAnnounceIdx = ref(0)

const quickReplies = ['Kiểm tra đơn hàng', 'Chính sách đổi trả', 'Bảng size giày', 'Hotline hỗ trợ']

function openChat() {
  chatOpen.value = true
  showChatTip.value = false
}

function sendChat() {
  if (!chatMessage.value.trim()) return

  // Demo: gửi xong thì giữ chat mở và chỉ xóa input để người dùng thấy tác vụ đã nhận
  chatMessage.value = ''
}

function sendQuickReply(q) {
  // Với quick reply: chỉ điều hướng, không đóng chat để tránh cảm giác “không chạy”
  if (q === 'Kiểm tra đơn hàng') router.push('/account/orders')
  else if (q === 'Chính sách đổi trả') router.push('/policies')
  else if (q === 'Bảng size giày') router.push('/bang-size-giay')
  else if (q === 'Hotline hỗ trợ') window.location.href = 'tel:0123456789'
}


const navLinks = [
  { path: '/', label: 'Trang chủ' },
  { path: '/products?sort=gia', label: 'Giá tốt 🔥' },
  { path: '/about', label: 'Giới thiệu' },
  { path: '/policies', label: 'Chính sách' },
  { path: '/lien-he', label: 'Liên hệ' },
]

const socialLinks = [
  {
    name: 'Facebook',
    href: '#',
    icon: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 3.656 10.995 9 11.835v-8.37h-3.047v-3.465h3.047v-2.646c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.465h-2.796v8.37c5.344-.84 9-5.845 9-11.835z"/></svg>`
  },
  {
    name: 'Instagram',
    href: '#',
    icon: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 1.17.054 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.012 3.584-.07 4.85c-.054 1.17-.249 1.805-.413 2.227-.217.562-.477.96-.896 1.382-.419.419-.819.679-1.381.896-.422.164-1.056.36-2.227.413-1.266.057-1.646.07-4.85.07s-3.584-.012-4.85-.07c-1.17-.054-1.805-.249-2.227-.415-.562-.217-.96-.477-1.382-.896-.418-.42-.679-.819-.896-1.381-.164-.422-.36-1.057-.413-2.227-.058-1.266-.07-1.646-.07-4.85s.012-3.584.07-4.85c.054-1.17.249-1.805.415-2.227.217-.562.477-.96.896-1.382.42-.419.819-.679 1.381-.896.422-.164 1.057-.36 2.227-.413 1.266-.058 1.646-.07 4.85-.07zm0-2.163c-3.259 0-3.667.014-4.947.072-1.277.057-2.148.258-2.911.554-.788.305-1.458.711-2.124 1.381-.666.666-1.072 1.336-1.378 2.124-.298.766-.499 1.636-.557 2.911-.059 1.28-.073 1.688-.073 4.947s.014 3.667.072 4.947c.057 1.277.258 2.148.554 2.911.305.788.711 1.458 1.381 2.124.666.666 1.336 1.072 2.124 1.378.766.298 1.636.499 2.911.557 1.28.059 1.688.073 4.947.073s3.667-.014 4.947-.072c1.277-.057 2.148-.258 2.911-.554.788-.305 1.458-.711 2.124-1.381.666-.666 1.072-1.336 1.378-2.124.298-.766.499-1.636.557-2.911.059-1.28.073-1.688.073-4.947s-.014-3.667-.072-4.947c-.057-1.277-.258-2.148-.554-2.911-.305-.788-.711-1.458-1.381-2.124-.666-.666-1.336-1.072-2.124-1.378-.766-.298-1.636-.499-2.911-.557-1.28-.059-1.688-.073-4.947-.073zm0 5.838c-3.403 0-5.838 2.435-5.838 5.838s2.435 5.838 5.838 5.838 5.838-2.435 5.838-5.838-2.435-5.838-5.838-5.838zm0 9.512c-2.029 0-3.674-1.645-3.674-3.674s1.645-3.674 3.674-3.674 3.674 1.645 3.674 3.674-1.645 3.674-3.674 3.674zm5.274-10.372c0 .73-.592 1.322-1.322 1.322-.731 0-1.322-.592-1.322-1.322 0-.73.591-1.322 1.322-1.322.73 0 1.322.592 1.322 1.322z"/></svg>`
  },
  {
    name: 'YouTube',
    href: '#',
    icon: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.016 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.016 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>`
  },
  {
    name: 'TikTok',
    href: '#',
    icon: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12.525.02c1.31 0 2.591.21 3.824.627v4.148c-.68-.14-1.385-.211-2.103-.211-3.676 0-6.657 2.981-6.657 6.657v1.442c0 3.676 2.981 6.657 6.657 6.657 3.676 0 6.657-2.981 6.657-6.657V0h4.148c0 2.261 1.833 4.094 4.094 4.094v4.148c-4.551 0-8.242-3.691-8.242-8.242z"/></svg>`
  }
]

function doSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: 'products', query: { search: searchQuery.value.trim() } })
    mobileMenuOpen.value = false
  }
}

function handleLogout() {
  authStore.logout()
  cartStore.reset()
  wishlistStore.reset()
  showUserMenu.value = false
  router.push('/')
}

function handleClickOutside(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    showUserMenu.value = false
  }
}

function handleProtectedClick(routePath) {
  if (!authStore.isLoggedIn) router.push('/login')
  else router.push(routePath)
}

function formatPrice(p) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p)
}

function updateDrawerQty(id, qty) {
  if (qty >= 1) cartStore.updateQuantity(id, qty)
}

onMounted(() => {
  // Timer for announcement bar
  setInterval(() => {
    currentAnnounceIdx.value = (currentAnnounceIdx.value + 1) % announcements.length
  }, 4000)

  document.addEventListener('click', handleClickOutside)
  window.addEventListener('scroll', () => { isScrolled.value = window.scrollY > 10 })
  if (authStore.isLoggedIn) {
    cartStore.fetchCart()
    wishlistStore.fetchWishlist()
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
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
.page-enter-active, .page-leave-active { transition: opacity 0.2s; }
.page-enter-from, .page-leave-to { opacity: 0; }

/* Chat window animation */
.chat-window-enter-active { transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.chat-window-leave-active { transition: all 0.2s ease-in; }
.chat-window-enter-from { opacity: 0; transform: translateY(20px) scale(0.9); transform-origin: bottom right; }
.chat-window-leave-to { opacity: 0; transform: translateY(10px) scale(0.95); transform-origin: bottom right; }

/* Fade slide for tooltip */
.fade-slide-enter-active { transition: all 0.2s ease; }
.fade-slide-leave-active { transition: all 0.15s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateX(8px); }
.fade-slide-leave-to { opacity: 0; transform: translateX(8px); }

/* Dropdown */
.dropdown-enter-active { transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1); }
.dropdown-leave-active { transition: all 0.15s ease; }
.dropdown-enter-from { opacity: 0; transform: translateY(-8px) scale(0.96); }
.dropdown-leave-to { opacity: 0; transform: translateY(-4px); }

/* Mobile menu */
.mobile-menu-enter-active { transition: all 0.3s ease; }
.mobile-menu-leave-active { transition: all 0.2s ease; }
.mobile-menu-enter-from { opacity: 0; max-height: 0; }
.mobile-menu-leave-to { opacity: 0; max-height: 0; }

/* Announcement Slide Animation */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.5s ease;
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
