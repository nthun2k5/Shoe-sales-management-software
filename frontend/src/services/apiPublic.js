import axios from 'axios'

const apiPublic = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default apiPublic
