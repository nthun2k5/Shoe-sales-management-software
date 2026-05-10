import { createApp } from 'vue'
import { createPinia } from 'pinia'
import AOS from 'aos'
import 'aos/dist/aos.css'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// Initialize AOS after mount
AOS.init({
  once: false,
  offset: 50,
  duration: 800,
  easing: 'ease-out-cubic'
})

