import React from 'react';

function Past() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="bg-white rounded-lg shadow-xl p-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-6 text-center">
              Past Analysis
            </h1>
            
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
                <h3 className="text-xl font-semibold text-blue-800 mb-3">Historical Trends</h3>
                <p className="text-blue-700 mb-4">
                  Analyze patterns and trends from historical data to identify long-term insights.
                </p>
                <div className="bg-blue-100 rounded p-3">
                  <p className="text-sm text-blue-800">Last 12 months: +15% growth</p>
                </div>
              </div>
              
              <div className="bg-green-50 rounded-lg p-6 border border-green-200">
                <h3 className="text-xl font-semibold text-green-800 mb-3">Performance Metrics</h3>
                <p className="text-green-700 mb-4">
                  Review past performance indicators and key metrics for optimization.
                </p>
                <div className="bg-green-100 rounded p-3">
                  <p className="text-sm text-green-800">Average response time: 2.3s</p>
                </div>
              </div>
              
              <div className="bg-purple-50 rounded-lg p-6 border border-purple-200">
                <h3 className="text-xl font-semibold text-purple-800 mb-3">User Engagement</h3>
                <p className="text-purple-700 mb-4">
                  Track historical user engagement patterns and interaction data.
                </p>
                <div className="bg-purple-100 rounded p-3">
                  <p className="text-sm text-purple-800">Monthly active users: 45K</p>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Data Timeline</h2>
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                  <div>
                    <p className="font-semibold text-gray-800">Q1 2024</p>
                    <p className="text-gray-600">Initial platform launch and user onboarding</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <div>
                    <p className="font-semibold text-gray-800">Q2 2024</p>
                    <p className="text-gray-600">Feature expansion and performance optimization</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                  <div>
                    <p className="font-semibold text-gray-800">Q3 2024</p>
                    <p className="text-gray-600">Advanced analytics and reporting tools</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Past;
