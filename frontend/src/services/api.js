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
    let token = null;
    try {
      token = localStorage.getItem('token');
    } catch (error) {
      console.warn('localStorage access failed in interceptor:', error);
    }
    
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
    console.log('API Response:', response.config.url, response.status, response.data)
    return response
  },
  (error) => {
    console.error('API Error:', error.config?.url, error.response?.status, error.response?.data)
    console.error('Full error object:', error)
    
    if (error.response?.status === 401) {
      console.log('Unauthorized - clearing token and redirecting to login')
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    
    // Add more detailed error logging
    if (error.code === 'ECONNABORTED') {
      console.error('Request was aborted or timed out')
    }
    if (error.code === 'ERR_NETWORK') {
      console.error('Network error - check backend connectivity')
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
  sendMessage: async (message, retryCount = 0) => {
    try {
      return await api.post('/chat/', { message: message })
    } catch (error) {
      console.error('Chat API error:', error)
      
      // Retry logic for temporary failures
      if (retryCount < 2 && (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK' || error.response?.status >= 500)) {
        console.log(`Retrying chat request (attempt ${retryCount + 1})`)
        await new Promise(resolve => setTimeout(resolve, 1000 * (retryCount + 1))) // Exponential backoff
        return chatAPI.sendMessage(message, retryCount + 1)
      }
      
      throw error
    }
  },
  
  sendMessageWithFile: async (formData, retryCount = 0) => {
    try {
      return api.post('/chat/with-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
    } catch (error) {
      console.error('Chat with file API error:', error)
      
      // Retry logic for temporary failures
      if (retryCount < 2 && (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK' || error.response?.status >= 500)) {
        console.log(`Retrying file upload request (attempt ${retryCount + 1})`)
        await new Promise(resolve => setTimeout(resolve, 2000 * (retryCount + 1))) // Longer backoff for file uploads
        return chatAPI.sendMessageWithFile(formData, retryCount + 1)
      }
      
      throw error
    }
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
