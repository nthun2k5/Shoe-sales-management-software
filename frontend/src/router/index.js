import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import AOS from 'aos'

// Configure NProgress
NProgress.configure({ showSpinner: false, speed: 400, minimum: 0.2 })

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior() { return { top: 0 } },
  routes: [
    // === AUTH ===
    { path: '/login', name: 'login', component: () => import('@/views/auth/LoginView.vue'), meta: { guest: true } },
    { path: '/register', name: 'register', component: () => import('@/views/auth/RegisterView.vue'), meta: { guest: true } },

    // === CLIENT (public) ===
    { path: '/', name: 'home', component: () => import('@/views/client/HomeView.vue') },
    { path: '/products', name: 'products', component: () => import('@/views/client/ProductListView.vue') },
    { path: '/products/:id', name: 'product-detail', component: () => import('@/views/client/ProductDetailView.vue') },
    { path: '/cart', name: 'cart', component: () => import('@/views/client/CartView.vue'), meta: { requiresAuth: true } },
    { path: '/checkout', name: 'checkout', component: () => import('@/views/client/CheckoutView.vue'), meta: { requiresAuth: true } },

    // === CLIENT ACCOUNT (with sidebar layout) ===
    {
      path: '/account',
      component: () => import('@/layouts/AccountLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', name: 'account-dashboard', component: () => import('@/views/client/DashboardView.vue') },
        { path: 'orders', name: 'account-orders', component: () => import('@/views/client/OrderHistoryView.vue') },
        { path: 'orders/:id', name: 'account-order-detail', component: () => import('@/views/client/OrderDetailView.vue') },
        { path: 'wishlist', name: 'account-wishlist', component: () => import('@/views/client/WishlistView.vue') },
        { path: 'addresses', name: 'account-addresses', component: () => import('@/views/client/AddressManagementView.vue') },
        { path: 'coupons', name: 'account-coupons', component: () => import('@/views/client/CouponsView.vue') },
        { path: 'profile', name: 'account-profile', component: () => import('@/views/client/ProfileView.vue') },
      ]
    },
    // Redirect old paths
    { path: '/orders', redirect: '/account/orders' },
    { path: '/wishlist', redirect: '/account/wishlist' },
    { path: '/contact', redirect: '/lien-he' },

    // === STATIC / INFO PAGES ===
    { path: '/lien-he', name: 'contact', component: () => import('@/views/client/ContactView.vue') },
    { path: '/chinh-sach-doi-tra', name: 'return-policy', component: () => import('@/views/client/PolicyView.vue') },
    { path: '/huong-dan-mua-hang', name: 'buy-guide', component: () => import('@/views/client/BuyGuideView.vue') },
    { path: '/bang-size-giay', name: 'size-guide', component: () => import('@/views/client/SizeGuideView.vue') },
    { path: '/chinh-sach-bao-mat', name: 'privacy', component: () => import('@/views/client/PrivacyView.vue') },
    { path: '/dieu-khoan', name: 'terms', component: () => import('@/views/client/TermsView.vue') },
    { path: '/faq', name: 'faq', component: () => import('@/views/client/FaqView.vue') },
    { path: '/about', name: 'about', component: () => import('@/views/client/AboutView.vue') },
    { path: '/policies', name: 'policies', component: () => import('@/views/client/PolicyView.vue') },

    // === ADMIN ===
    { path: '/admin', name: 'admin-dashboard', component: () => import('@/views/admin/DashboardView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/analytics', name: 'admin-analytics', component: () => import('@/views/admin/AnalyticsView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/products', name: 'admin-products', component: () => import('@/views/admin/ProductsView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/products/new', name: 'admin-product-new', component: () => import('@/views/admin/ProductFormView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/products/:id/edit', name: 'admin-product-edit', component: () => import('@/views/admin/ProductFormView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/categories', name: 'admin-categories', component: () => import('@/views/admin/CategoriesView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/orders', name: 'admin-orders', component: () => import('@/views/admin/OrdersView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/users', name: 'admin-users', component: () => import('@/views/admin/UsersView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/coupons', name: 'admin-coupons', component: () => import('@/views/admin/CouponsView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/inventory', name: 'admin-inventory', component: () => import('@/views/admin/InventoryView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/logs', name: 'admin-logs', component: () => import('@/views/admin/LogsView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/banks', name: 'admin-banks', component: () => import('@/views/admin/BanksView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },

    // === 404 ===
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/client/NotFoundView.vue') },
  ],
})

router.beforeEach((to, from, next) => {
  NProgress.start()
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    NProgress.done()
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    NProgress.done()
    return next({ name: 'home' })
  }
  if (to.meta.guest && authStore.isLoggedIn) {
    NProgress.done()
    return next(authStore.isAdmin ? { name: 'admin-dashboard' } : { name: 'home' })
  }
  next()
})

router.afterEach(() => {
  NProgress.done()
  setTimeout(() => { AOS.refresh() }, 100)
})

export default router
