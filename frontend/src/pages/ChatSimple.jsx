import React, { useState, useRef } from 'react'
import { chatAPI } from '../services/api'
import { useAuth } from '../hooks/useAuth.jsx'
import LoadingSpinner from '../components/LoadingSpinner'
import { 
  PaperAirplaneIcon, 
  CloudArrowUpIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'

const ChatSimple = () => {
  const { user } = useAuth()
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0])
    }
  }

  const handleFileSelect = (file) => {
    // Accept PDF, DOC, DOCX, TXT files
    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain',
      'image/jpeg',
      'image/png'
    ]
    
    if (allowedTypes.includes(file.type) || file.type.startsWith('image/')) {
      setSelectedFile(file)
      console.log('File selected:', file.name)
    } else {
      alert('Please select a PDF, DOC, DOCX, TXT, or image file')
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0])
    }
  }

  const removeFile = () => {
    setSelectedFile(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim() || loading) return

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date(),
      file: selectedFile ? {
        name: selectedFile.name,
        size: selectedFile.size,
        type: selectedFile.type
      } : null
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setLoading(true)

    try {
      let response
      if (selectedFile) {
        // Send message with file
        const formData = new FormData()
        formData.append('message', inputMessage)
        formData.append('file', selectedFile)
        
        response = await chatAPI.sendMessageWithFile(formData)
        removeFile()
      } else {
        // Send text message only
        response = await chatAPI.sendMessage({ message: inputMessage })
      }

      const assistantMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'assistant',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
      setTimeout(scrollToBottom, 100)
    } catch (error) {
      console.error('Error sending message:', error)
      console.error('Error details:', {
        message: error.message,
        status: error.response?.status,
        data: error.response?.data,
        code: error.code
      })
      
      let errorText = 'Sorry, I encountered an error. Please try again.'
      
      // Provide more specific error messages
      if (error.response?.status === 401) {
        errorText = 'Authentication expired. Please login again.'
      } else if (error.response?.status === 422) {
        errorText = 'Invalid request format. Please try again.'
      } else if (error.response?.status === 429) {
        errorText = 'Too many requests. Please wait a moment and try again.'
      } else if (error.code === 'ECONNABORTED') {
        errorText = 'Request timed out. Please check your connection and try again.'
      } else if (error.code === 'ERR_NETWORK') {
        errorText = 'Network error. Please check your connection and try again.'
      } else if (error.response?.data?.detail) {
        errorText = `Server error: ${error.response.data.detail}`
      }
      
      const errorMessage = {
        id: Date.now() + 1,
        text: errorText,
        sender: 'assistant',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  // If user is not authenticated, show login prompt
  if (!user) {
    return (
      <div className="flex items-center justify-center h-full bg-primary">
        <div className="text-center p-8">
          <div className="bg-warning/20 border border-warning rounded-lg p-6 max-w-md card">
            <h3 className="text-lg font-medium text-warning mb-2">
              Authentication Required
            </h3>
            <p className="text-secondary">
              Please sign in to access the chat assistant.
            </p>
            <a
              href="/login"
              className="mt-4 inline-block bg-accent hover:bg-accent-hover text-primary px-4 py-2 rounded-md transition-colors"
            >
              Go to Login
            </a>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-primary">
      {/* Chat Header */}
      <div className="bg-card border border-b border-custom px-6 py-4">
        <h2 className="text-xl font-semibold text-primary">
          AI Chat Assistant
        </h2>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Upload documents and ask questions about them!
        </p>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
            <div className="mb-4">
              <CloudArrowUpIcon className="w-12 h-12 mx-auto text-gray-400" />
            </div>
            <p className="text-lg font-medium mb-2">Welcome to AI Chat!</p>
            <p className="text-sm mb-4">Upload a PDF, DOC, or TXT file and ask questions about it.</p>
            <p className="text-xs">Or just type a message to chat normally.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-700'
                }`}
              >
                {message.file && (
                  <div className="text-xs opacity-75 mb-1">
                    📎 {message.file.name}
                  </div>
                )}
                <p className="text-sm">{message.text}</p>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* File Upload Area */}
      {selectedFile && (
        <div className="mx-6 mb-2 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="text-blue-600 dark:text-blue-400">
              📎
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                {selectedFile.name}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {(selectedFile.size / 1024).toFixed(1)} KB • {selectedFile.type}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={removeFile}
            className="p-1 rounded-full hover:bg-blue-100 dark:hover:bg-blue-800 transition-colors"
          >
            <XMarkIcon className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          </button>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-custom p-4">
        <form onSubmit={handleSubmit} className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={selectedFile ? "Ask about your document..." : "Type your message..."}
              className="w-full px-4 py-3 pr-12 border border-custom rounded-full focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent bg-input text-primary placeholder-text-muted transition-colors"
              disabled={loading}
            />
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
              onChange={handleFileChange}
              className="hidden"
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 rounded-full hover:bg-tertiary transition-colors"
              title="Upload PDF, DOC, or TXT file"
            >
              <CloudArrowUpIcon className="w-5 h-5 text-secondary" />
            </button>
          </div>
          <button
            type="submit"
            disabled={loading || !inputMessage.trim()}
            className="bg-accent text-primary p-3 rounded-full hover:bg-accent-hover transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {loading ? (
              <LoadingSpinner size="sm" />
            ) : (
              <PaperAirplaneIcon className="w-5 h-5" />
            )}
          </button>
        </form>
      </div>
    </div>
  )
}

export default ChatSimple
