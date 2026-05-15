import React from 'react'

const ChatTest = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Chat Test Page
        </h1>
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
          <p className="text-gray-700 dark:text-gray-300">
            If you can see this page, the routing is working correctly.
          </p>
          <p className="text-gray-700 dark:text-gray-300 mt-2">
            The issue is likely in the Chat component logic.
          </p>
        </div>
      </div>
    </div>
  )
}

export default ChatTest
