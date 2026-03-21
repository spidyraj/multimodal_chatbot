import React, { useState } from 'react'
import { youtubeAPI } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import { 
  PlayIcon, 
  LinkIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'

const YouTube = () => {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState('')
  const [error, setError] = useState('')
  const [videoInfo, setVideoInfo] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!url.trim() || loading) return

    setLoading(true)
    setError('')
    setSummary('')
    setVideoInfo(null)

    try {
      const response = await youtubeAPI.summarize(url)
      
      if (response.data.error) {
        setError(response.data.error)
      } else {
        setSummary(response.data.response)
        setVideoInfo({
          videoId: response.data.video_id,
          url: url
        })
      }
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to summarize video')
    } finally {
      setLoading(false)
    }
  }

  const getYouTubeEmbedUrl = (videoId) => {
    return `https://www.youtube.com/embed/${videoId}`
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">YouTube Summarizer</h2>
        <p className="mt-1 text-sm text-gray-600">
          Get AI-powered summaries of YouTube videos by extracting and analyzing their transcripts.
        </p>
      </div>

      {/* URL Input */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="youtube-url" className="block text-sm font-medium text-gray-700 mb-2">
              YouTube Video URL
            </label>
            <div className="flex space-x-4">
              <input
                id="youtube-url"
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://www.youtube.com/watch?v=..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent flex-1"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !url.trim()}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                {loading ? <LoadingSpinner size="sm" /> : <PlayIcon className="w-4 h-4" />}
                <span>Summarize</span>
              </button>
            </div>
          </div>
        </form>

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center space-x-2">
              <ExclamationTriangleIcon className="w-5 h-5 text-red-400" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        )}
      </div>

      {/* Results */}
      {summary && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="mb-4">
            <h3 className="text-lg font-medium text-gray-900 mb-2 flex items-center">
              <CheckCircleIcon className="w-5 h-5 text-green-500 mr-2" />
              Video Summary
            </h3>
            {videoInfo && (
              <div className="mb-4">
                <a
                  href={videoInfo.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-800 flex items-center"
                >
                  <LinkIcon className="w-4 h-4 mr-1" />
                  {videoInfo.url}
                </a>
              </div>
            )}
          </div>
          
          <div className="prose max-w-none">
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-800 whitespace-pre-wrap">{summary}</p>
            </div>
          </div>
        </div>
      )}

      {/* Video Preview */}
      {videoInfo && videoInfo.videoId && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Video Preview</h3>
          <div className="aspect-w-16 aspect-h-9">
            <iframe
              src={getYouTubeEmbedUrl(videoInfo.videoId)}
              title="YouTube video player"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              className="w-full h-64 rounded-lg"
            />
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="bg-blue-50 rounded-lg shadow-md p-6 border-blue-200">
        <h3 className="text-sm font-medium text-blue-900 mb-2">How it works:</h3>
        <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
          <li>Paste a YouTube video URL in the input field above</li>
          <li>The system extracts the video transcript</li>
          <li>AI analyzes the content and generates a comprehensive summary</li>
          <li>View the summary alongside the original video</li>
        </ol>
        
        <div className="mt-3 p-2 bg-blue-100 rounded text-xs text-blue-700">
          <strong>Note:</strong> Only videos with available transcripts can be summarized. 
          Some videos may not have transcripts available.
        </div>
      </div>
    </div>
  )
}

export default YouTube
