import React, { useState } from 'react'
import { uploadAPI } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import { 
  CloudArrowUpIcon, 
  DocumentIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  TrashIcon
} from '@heroicons/react/24/outline'

const Upload = () => {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [error, setError] = useState('')
  const [dragActive, setDragActive] = useState(false)

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

  const handleFileSelect = (selectedFile) => {
    if (selectedFile.type === 'application/pdf') {
      setFile(selectedFile)
      setError('')
      setUploadResult(null)
    } else {
      setError('Please select a PDF file')
      setFile(null)
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0])
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file || loading) return

    setLoading(true)
    setError('')
    setUploadResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await uploadAPI.uploadPDF(formData)
      setUploadResult(response.data)
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to upload file')
    } finally {
      setLoading(false)
    }
  }

  const resetUpload = () => {
    setFile(null)
    setUploadResult(null)
    setError('')
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          PDF Upload
        </h2>
        <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
          Upload PDF documents to make them searchable and available for AI-powered Q&A.
        </p>
      </div>

      {/* Upload Area */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 transition-colors">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div
            className={`
              relative border-2 border-dashed rounded-lg p-8 text-center transition-colors
              ${dragActive
                ? 'border-blue-400 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
              }
              ${file ? 'border-green-400 bg-green-50 dark:bg-green-900/20' : ''}
            `}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              disabled={loading}
            />
            
            <div className="space-y-4">
              <div className="mx-auto w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center">
                {file ? (
                  <DocumentIcon className="w-8 h-8 text-green-600 dark:text-green-400" />
                ) : (
                  <CloudArrowUpIcon className="w-8 h-8 text-gray-500 dark:text-gray-400" />
                )}
              </div>
              
              <div>
                {file ? (
                  <div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Drop your PDF here, or click to browse
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      PDF files up to 10MB
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {error && (
            <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
              <div className="flex items-center space-x-2">
                <ExclamationTriangleIcon className="w-5 h-5 text-red-400" />
                <p className="text-sm text-red-700 dark:text-red-400">{error}</p>
              </div>
            </div>
          )}

          {file && (
            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                {loading ? <LoadingSpinner size="sm" /> : <CloudArrowUpIcon className="w-4 h-4" />}
                <span>{loading ? 'Uploading...' : 'Upload PDF'}</span>
              </button>
              
              <button
                type="button"
                onClick={resetUpload}
                disabled={loading}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                <TrashIcon className="w-4 h-4" />
                <span>Clear</span>
              </button>
            </div>
          )}
        </form>
      </div>

      {/* Upload Result */}
      {uploadResult && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 transition-colors">
          <div className="mb-4">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2 flex items-center">
              <CheckCircleIcon className="w-5 h-5 text-green-500 mr-2" />
              Upload Successful
            </h3>
            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-md p-4">
              <p className="text-sm text-green-800 dark:text-green-200">
                Your PDF has been successfully uploaded and processed. You can now ask questions about its content in the chat.
              </p>
            </div>
          </div>
          
          {uploadResult.filename && (
            <div className="space-y-2">
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                File Details:
              </p>
              <div className="bg-gray-50 dark:bg-gray-700 rounded-md p-3">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  <strong>Name:</strong> {uploadResult.filename}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  <strong>Size:</strong> {uploadResult.size ? `${(uploadResult.size / 1024 / 1024).toFixed(2)} MB` : 'Unknown'}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  <strong>Status:</strong> Processed and ready for Q&A
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Instructions */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg shadow-md p-6 border-blue-200 dark:border-blue-800 transition-colors">
        <h3 className="text-sm font-medium text-blue-900 dark:text-blue-100 mb-2">
          How it works:
        </h3>
        <ol className="text-sm text-blue-800 dark:text-blue-200 space-y-1 list-decimal list-inside">
          <li>Upload a PDF document using the area above</li>
          <li>The system processes and indexes the document content</li>
          <li>Go to the Chat section to ask questions about your document</li>
          <li>The AI will provide answers based on the uploaded content</li>
        </ol>
        
        <div className="mt-3 p-2 bg-blue-100 dark:bg-blue-800/30 rounded text-xs text-blue-700 dark:text-blue-300">
          <strong>Note:</strong> PDF files are processed using advanced text extraction and indexing. 
          The content becomes searchable and available for intelligent Q&A.
        </div>
      </div>
    </div>
  )
}

export default Upload
