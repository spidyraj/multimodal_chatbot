import React, { useState, useRef } from 'react'
import { uploadAPI } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import { 
  CloudArrowUpIcon, 
  DocumentIcon, 
  TrashIcon,
  CheckCircleIcon 
} from '@heroicons/react/24/outline'

const Upload = () => {
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState('')
  const [documents, setDocuments] = useState([])
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const fileInputRef = useRef(null)

  const handleFileSelect = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Please select a PDF file')
      return
    }

    setUploading(true)
    setError('')
    setSuccess('')
    setUploadProgress(`Uploading ${file.name}...`)

    try {
      const response = await uploadAPI.uploadPDF(file)
      
      const newDoc = {
        id: response.data.document_id,
        filename: response.data.filename,
        chunks: response.data.chunks_processed,
        uploaded_at: new Date()
      }

      setDocuments(prev => [newDoc, ...prev])
      setSuccess(`Successfully uploaded ${file.name} with ${response.data.chunks_processed} chunks processed`)
      
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to upload document')
    } finally {
      setUploading(false)
      setUploadProgress('')
    }
  }

  const handleDelete = async (documentId) => {
    if (!confirm('Are you sure you want to delete this document?')) return

    try {
      await uploadAPI.deleteDocument(documentId)
      setDocuments(prev => prev.filter(doc => doc.id !== documentId))
      setSuccess('Document deleted successfully')
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to delete document')
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      const file = files[0]
      if (fileInputRef.current) {
        fileInputRef.current.files = files
        handleFileSelect({ target: { files: [file] } })
      }
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Document Upload</h2>
        <p className="mt-1 text-sm text-gray-600">
          Upload PDF documents to enhance your chat experience with contextual information.
        </p>
      </div>

      {/* Upload Area */}
      <div className="card">
        <div
          className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-400 transition-colors"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="hidden"
            id="file-upload"
            disabled={uploading}
          />
          
          <label htmlFor="file-upload" className="cursor-pointer">
            <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
            <div className="mt-4">
              <span className="btn-primary inline-flex items-center">
                {uploading ? <LoadingSpinner size="sm" /> : <CloudArrowUpIcon className="w-4 h-4 mr-2" />}
                {uploading ? 'Processing...' : 'Choose PDF file'}
              </span>
            </div>
            <p className="mt-2 text-sm text-gray-600">
              or drag and drop your PDF here
            </p>
            <p className="text-xs text-gray-500 mt-1">
              PDF files only, up to 10MB
            </p>
          </label>
        </div>

        {uploadProgress && (
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
            <p className="text-sm text-blue-700">{uploadProgress}</p>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md">
            {error}
          </div>
        )}

        {success && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-md">
            {success}
          </div>
        )}
      </div>

      {/* Documents List */}
      {documents.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Your Documents</h3>
          <div className="space-y-3">
            {documents.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <DocumentIcon className="w-5 h-5 text-gray-400" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{doc.filename}</p>
                    <p className="text-xs text-gray-500">
                      {doc.chunks} chunks • {doc.uploaded_at.toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(doc.id)}
                  className="text-red-600 hover:text-red-800 p-1"
                  title="Delete document"
                >
                  <TrashIcon className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="card bg-blue-50 border-blue-200">
        <h3 className="text-sm font-medium text-blue-900 mb-2">How it works:</h3>
        <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
          <li>Upload a PDF document using the area above</li>
          <li>The system processes and chunks your document</li>
          <li>Ask questions in chat, and the AI will use your documents as context</li>
          <li>Delete documents when you no longer need them</li>
        </ol>
      </div>
    </div>
  )
}

export default Upload
