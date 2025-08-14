import React from 'react';

function Behavior() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="bg-white rounded-lg shadow-xl p-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-6 text-center">
              Behavior Analysis
            </h1>
            
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              <div className="bg-green-50 rounded-lg p-6 border border-green-200">
                <h3 className="text-xl font-semibold text-green-800 mb-3">User Patterns</h3>
                <p className="text-green-700 mb-4">
                  Analyze how users interact with the platform and identify common behavior patterns.
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-green-700">Most active time:</span>
                    <span className="text-sm font-semibold text-green-800">2-4 PM</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-green-700">Average session:</span>
                    <span className="text-sm font-semibold text-green-800">12 minutes</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-green-700">Bounce rate:</span>
                    <span className="text-sm font-semibold text-green-800">23%</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
                <h3 className="text-xl font-semibold text-blue-800 mb-3">Feature Usage</h3>
                <p className="text-blue-700 mb-4">
                  Track which features are most popular and how users navigate through the platform.
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-blue-700">Dashboard views:</span>
                    <span className="text-sm font-semibold text-blue-800">67%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-blue-700">Reports accessed:</span>
                    <span className="text-sm font-semibold text-blue-800">45%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-blue-700">Settings used:</span>
                    <span className="text-sm font-semibold text-blue-800">12%</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-6 mb-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">User Journey Map</h2>
              <div className="grid md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white font-bold mx-auto mb-2">1</div>
                  <p className="text-sm font-semibold text-gray-800">Landing</p>
                  <p className="text-xs text-gray-600">Homepage visit</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold mx-auto mb-2">2</div>
                  <p className="text-sm font-semibold text-gray-800">Explore</p>
                  <p className="text-xs text-gray-600">Browse features</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center text-white font-bold mx-auto mb-2">3</div>
                  <p className="text-sm font-semibold text-gray-800">Engage</p>
                  <p className="text-xs text-gray-600">Use tools</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center text-white font-bold mx-auto mb-2">4</div>
                  <p className="text-sm font-semibold text-gray-800">Return</p>
                  <p className="text-xs text-gray-600">Come back</p>
                </div>
              </div>
            </div>
            
            <div className="bg-gradient-to-r from-green-500 to-blue-500 rounded-lg p-6 text-white">
              <h2 className="text-2xl font-semibold mb-4">Behavioral Insights</h2>
              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <h4 className="font-semibold mb-2">Peak Usage Times</h4>
                  <p className="text-green-100">Users are most active during business hours with a peak at 3 PM</p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Preferred Features</h4>
                  <p className="text-green-100">Analytics dashboard is the most frequently accessed feature</p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Engagement Patterns</h4>
                  <p className="text-green-100">Users typically spend 2-3 sessions per day on the platform</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Behavior;
