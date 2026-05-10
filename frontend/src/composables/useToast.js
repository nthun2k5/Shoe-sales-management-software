import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

function removeToast(id) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

export function useToast() {
  /**
   * Backward compatible:
   * - showToast(message, type, duration)
   * - showToast({ message, type, duration, title })
   */
  function showToast(messageOrOptions, type = 'info', duration = 3000) {
    const opts = typeof messageOrOptions === 'string'
      ? { message: messageOrOptions, type, duration }
      : {
          message: messageOrOptions.message,
          type: messageOrOptions.type ?? 'info',
          duration: messageOrOptions.duration ?? 3000,
          title: messageOrOptions.title
        }

    const id = ++toastId
    const payload = {
      id,
      type: opts.type,
      title: opts.title,
      message: opts.message
    }

    toasts.value.push(payload)

    window.setTimeout(() => {
      removeToast(id)
    }, opts.duration)
  }

  function success(message) { showToast(message, 'success') }
  function error(message) { showToast(message, 'error') }
  function info(message) { showToast(message, 'info') }

  return { toasts, showToast, success, error, info, removeToast }
}

