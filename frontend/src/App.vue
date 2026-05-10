<template>
  <div id="qlbg-app">
    <!-- Toast Notifications -->
    <div class="toast-container" aria-live="polite" aria-atomic="true">
      <TransitionGroup name="toast" tag="div" class="toast-stack">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', `toast-${toast.type}`]"
          role="status"
        >
          <div class="toast-left">
            <div class="toast-icon" aria-hidden="true">
              <svg v-if="toast.type==='success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 6 9 17l-5-5" />
              </svg>
              <svg v-else-if="toast.type==='error'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
                <path d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 16v-4" />
                <path d="M12 8h.01" />
                <path d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
            </div>

            <div class="toast-content">
              <div v-if="toast.title" class="toast-title">{{ toast.title }}</div>
              <div class="toast-message">{{ toast.message }}</div>
            </div>
          </div>

          <button class="toast-close" type="button" aria-label="Đóng" @click="removeToast(toast.id)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 6 6 18" />
              <path d="M6 6l12 12" />
            </svg>
          </button>
        </div>
      </TransitionGroup>
    </div>

    <!-- Admin Layout -->
    <AdminLayout v-if="isAdminRoute">
      <RouterView />
    </AdminLayout>

    <!-- Auth Layout (no header/footer) -->
    <div v-else-if="isAuthRoute" class="min-h-screen">
      <RouterView />
    </div>

    <!-- Account Layout (standalone, like admin) -->
    <RouterView v-else-if="isAccountRoute" />

    <!-- Client Layout -->
    <ClientLayout v-else>
      <RouterView />
    </ClientLayout>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from '@/composables/useToast'
import AdminLayout from '@/layouts/AdminLayout.vue'
import ClientLayout from '@/layouts/ClientLayout.vue'

const route = useRoute()
const { toasts, removeToast } = useToast()

const isAdminRoute = computed(() => route.path.startsWith('/admin'))
const isAuthRoute = computed(() => ['/login', '/register'].includes(route.path))
const isAccountRoute = computed(() => route.path.startsWith('/account'))

const preventCopy = (e) => {
  e.preventDefault()
  return false
}

const preventContextMenu = (e) => {
  e.preventDefault()
  return false
}

onMounted(() => {
  document.addEventListener('contextmenu', preventContextMenu)
  document.addEventListener('copy', preventCopy)
})

onUnmounted(() => {
  document.removeEventListener('contextmenu', preventContextMenu)
  document.removeEventListener('copy', preventCopy)
})
</script>

