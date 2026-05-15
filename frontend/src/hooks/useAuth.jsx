import { useState, useEffect, createContext, useContext } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      try {
        // Safely access localStorage
        let token = null;
        try {
          token = localStorage.getItem('token');
        } catch (error) {
          console.warn('localStorage access failed:', error);
        }
        
        if (token) {
          try {
            const response = await authAPI.getMe()
            setUser(response.data)
          } catch (error) {
            console.error('Auth initialization error:', error)
            try {
              localStorage.removeItem('token')
            } catch (e) {
              console.warn('localStorage removal failed:', e);
            }
          }
        }
      } catch (error) {
        console.error('Token retrieval error:', error)
      } finally {
        setLoading(false)
      }
    }

    // Add timeout to prevent infinite loading
    const timeoutId = setTimeout(() => {
      setLoading(false)
    }, 5000) // 5 second timeout

    initAuth()
    
    return () => clearTimeout(timeoutId)
  }, [])

  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ email, password })
      const { access_token } = response.data
      
      // Safely store token
      try {
        localStorage.setItem('token', access_token)
      } catch (error) {
        console.warn('localStorage storage failed:', error);
      }
      
      // Get user info
      const userResponse = await authAPI.getMe()
      setUser(userResponse.data)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const register = async (username, email, password) => {
    try {
      await authAPI.register({ username, email, password })
      
      // Auto login after registration
      const loginResult = await login(email, password)
      return loginResult
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      }
    }
  }

  const logout = () => {
    try {
      localStorage.removeItem('token')
    } catch (error) {
      console.warn('localStorage removal failed:', error);
    }
    setUser(null)
  }

  const value = {
    user,
    login,
    register,
    logout,
    loading
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
