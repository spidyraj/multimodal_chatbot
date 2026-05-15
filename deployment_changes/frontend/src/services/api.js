import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'https://multimodal-backend-production.up.railway.app'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    console.log('API Request:', config.method?.toUpperCase(), config.url, token ? 'with token' : 'no token')
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.url, response.status)
    return response
  },
  (error) => {
    console.error('API Error:', error.config?.url, error.response?.status, error.response?.data)
    
    if (error.response?.status === 401) {
      console.log('Unauthorized - clearing token and redirecting to login')
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getMe: () => api.get('/auth/me'),
}

// Chat API
export const chatAPI = {
  sendMessage: (message) => api.post('/chat/', { message }),
  sendMessageWithFile: (message, file) => {
    const formData = new FormData()
    formData.append('message', message)
    if (file) {
      formData.append('file', file)
    }
    return api.post('/chat/with-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  getHistory: (limit = 10) => api.get(`/chat/history?limit=${limit}`),
}

// Upload API
export const uploadAPI = {
  uploadPDF: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload/pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  deleteDocument: (documentId) => api.delete(`/upload/${documentId}`),
}

// YouTube API
export const youtubeAPI = {
  summarize: (url) => api.post('/youtube/summarize', { url }),
}

// Health check
export const healthAPI = {
  check: () => api.get('/health'),
}

export default api
