import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './hooks/useAuth.jsx'
import { DarkModeProvider } from './hooks/useDarkMode.jsx'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import ChatSimple from './pages/ChatSimple'
import YouTube from './pages/YouTube'
import LoadingSpinner from './components/LoadingSpinner'
import ErrorBoundary from './components/ErrorBoundary'

function AppContent() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-primary">
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-primary transition-colors duration-200">
        <Routes>
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/chat" />} />
          <Route path="/register" element={!user ? <Register /> : <Navigate to="/chat" />} />
          <Route path="/" element={user ? <Layout /> : <Navigate to="/login" />}>
            <Route index element={<Navigate to="/chat" />} />
            <Route path="chat" element={<ChatSimple />} />
            <Route path="youtube" element={<YouTube />} />
          </Route>
        </Routes>
      </div>
    </ErrorBoundary>
  )
}

function App() {
  return (
    <ErrorBoundary>
      <DarkModeProvider>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </DarkModeProvider>
    </ErrorBoundary>
  )
}

export default App
