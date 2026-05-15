import React, { useState, useEffect, useRef } from 'react'
import { chatAPI } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import { 
  PaperAirplaneIcon, 
  DocumentTextIcon, 
  PhotoIcon, 
  SpeakerWaveIcon,
  CloudArrowUpIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'

const Chat = () => {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [historyLoading, setHistoryLoading] = useState(true)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    loadChatHistory()
  }, [])

  const loadChatHistory = async () => {
    try {
      console.log('Loading chat history...')
      const response = await chatAPI.getHistory()
      console.log('Chat history response:', response)
      
      const history = response.data.map(chat => ({
        id: chat.id,
        text: chat.question,
        sender: 'user',
        timestamp: new Date(chat.created_at)
      })).concat(
        response.data.map(chat => ({
          id: chat.id + '_response',
          text: chat.answer,
          sender: 'assistant',
          timestamp: new Date(chat.created_at)
        }))
      ).sort((a, b) => a.timestamp - b.timestamp)

      setMessages(history)
      console.log('Chat history loaded successfully:', history.length, 'messages')
    } catch (error) {
      console.error('Failed to load chat history:', error)
      console.error('Error details:', error.response?.status, error.response?.data)
      
      // Don't show error to user, just start with empty chat
      setMessages([])
    } finally {
      setHistoryLoading(false)
    }
  }

  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      // Cancel any ongoing speech
      window.speechSynthesis.cancel()
      
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.9
      utterance.pitch = 1
      utterance.volume = 1
      
      utterance.onstart = () => setIsSpeaking(true)
      utterance.onend = () => setIsSpeaking(false)
      utterance.onerror = () => setIsSpeaking(false)
      
      window.speechSynthesis.speak(utterance)
    }
  }

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel()
      setIsSpeaking(false)
    }
  }

  // File handling functions
  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
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
    if (file.type === 'application/pdf') {
      setSelectedFile(file)
      console.log('PDF file selected:', file.name)
    } else if (file.type.startsWith('image/')) {
      setSelectedFile(file)
      console.log('Image file selected:', file.name)
    } else {
      alert('Please select a PDF or image file')
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
        type: selectedFile.type,
        size: selectedFile.size
      } : null
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setLoading(true)

    try {
      let response
      
      if (selectedFile) {
        // Send message with file
        console.log('Sending message with file:', selectedFile.name)
        response = await chatAPI.sendMessageWithFile(inputMessage, selectedFile)
      } else {
        // Send regular message
        response = await chatAPI.sendMessage(inputMessage)
      }
      
      const assistantMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'assistant',
        timestamp: new Date(),
        contextUsed: response.data.context_used
      }

      setMessages(prev => [...prev, assistantMessage])
      
      // Clear file after successful upload
      if (selectedFile) {
        removeFile()
      }
      
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'assistant',
        timestamp: new Date(),
        error: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  if (historyLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      {/* Chat Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 transition-colors">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          AI Chat Assistant
        </h2>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Ask me anything! I can help with your questions and provide intelligent responses.
        </p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto mb-4 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center">
              <ChatBubbleLeftRightIcon className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Start a conversation
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Send a message below to begin chatting with your AI assistant.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className="flex items-start space-x-2 max-w-2xl">
                {message.sender === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
                    <ChatBubbleLeftRightIcon className="w-4 h-4 text-white" />
                  </div>
                )}
                <div
                  className={`px-4 py-3 rounded-2xl ${
                    message.sender === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : message.error
                      ? 'bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-bl-none'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white rounded-bl-none'
                  } shadow-sm transition-colors`}
                >
                  <p className="text-sm whitespace-pre-wrap leading-relaxed">
                    {message.text}
                  </p>
                  {message.file && (
                    <div className="mt-2 p-2 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-center space-x-2">
                      <DocumentTextIcon className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                      <span className="text-xs text-gray-600 dark:text-gray-300">
                        {message.file.name} ({(message.file.size / 1024).toFixed(1)} KB)
                      </span>
                    </div>
                  )}
                  {message.contextUsed && (
                    <p className="text-xs mt-2 opacity-75 flex items-center">
                      <DocumentTextIcon className="w-3 h-3 mr-1" />
                      Used document context
                    </p>
                  )}
                  <p className="text-xs mt-2 opacity-75">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
                {message.sender === 'assistant' && (
                  <button
                    onClick={() => isSpeaking ? stopSpeaking() : speakText(message.text)}
                    className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    title={isSpeaking ? 'Stop speaking' : 'Speak response'}
                  >
                    <SpeakerWaveIcon className={`w-4 h-4 ${isSpeaking ? 'text-red-500' : 'text-gray-500 dark:text-gray-400'}`} />
                  </button>
                )}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-start">
            <div className="flex items-start space-x-2">
              <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
                <ChatBubbleLeftRightIcon className="w-4 h-4 text-white" />
              </div>
              <div className="bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white px-4 py-3 rounded-2xl rounded-bl-none shadow-sm">
                <LoadingSpinner size="sm" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div 
        className={`bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-6 py-4 transition-colors ${
          dragActive ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : ''
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {/* File Upload Area */}
        {selectedFile && (
          <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <DocumentTextIcon className="w-5 h-5 text-blue-500" />
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
              className="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              <XMarkIcon className="w-4 h-4 text-gray-500 dark:text-gray-400" />
            </button>
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={selectedFile ? "Ask about your document..." : "Type your message..."}
              className="w-full px-4 py-3 pr-12 border border-gray-300 dark:border-gray-600 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-colors"
              disabled={loading}
            />
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,image/*"
              onChange={handleFileChange}
              className="hidden"
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              title="Upload PDF or image"
            >
              <CloudArrowUpIcon className="w-5 h-5 text-gray-500 dark:text-gray-400" />
            </button>
          </div>
          <button
            type="submit"
            disabled={loading || !inputMessage.trim()}
            className="bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <PaperAirplaneIcon className="w-5 h-5" />
          </button>
        </form>
        
        {dragActive && (
          <div className="absolute inset-0 flex items-center justify-center bg-blue-50 dark:bg-blue-900/20 rounded-lg border-2 border-dashed border-blue-300 dark:border-blue-600">
            <div className="text-center">
              <CloudArrowUpIcon className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <p className="text-sm text-blue-600 dark:text-blue-400">
                Drop your PDF or image here
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Chat
