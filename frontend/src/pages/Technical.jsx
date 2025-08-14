import React from 'react';

function Technical() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="bg-white rounded-lg shadow-xl p-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-6 text-center">
              Technical Dashboard
            </h1>
            
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-purple-50 rounded-lg p-6 border border-purple-200">
                <h3 className="text-xl font-semibold text-purple-800 mb-3">System Performance</h3>
                <p className="text-purple-700 mb-4">
                  Monitor system health, response times, and overall performance metrics.
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-purple-700">CPU Usage:</span>
                    <span className="text-sm font-semibold text-purple-800">45%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-purple-700">Memory:</span>
                    <span className="text-sm font-semibold text-purple-800">2.3GB/8GB</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-purple-700">Disk Space:</span>
                    <span className="text-sm font-semibold text-purple-800">67%</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
                <h3 className="text-xl font-semibold text-blue-800 mb-3">API Metrics</h3>
                <p className="text-blue-700 mb-4">
                  Track API performance, response times, and error rates across all endpoints.
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-blue-700">Avg Response:</span>
                    <span className="text-sm font-semibold text-blue-800">180ms</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-blue-700">Success Rate:</span>
                    <span className="text-sm font-semibold text-blue-800">99.2%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-blue-700">Requests/min:</span>
                    <span className="text-sm font-semibold text-blue-800">1,247</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-green-50 rounded-lg p-6 border border-green-200">
                <h3 className="text-xl font-semibold text-green-800 mb-3">Database Health</h3>
                <p className="text-green-700 mb-4">
                  Monitor database performance, query times, and connection pool status.
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-green-700">Query Time:</span>
                    <span className="text-sm font-semibold text-green-800">45ms</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-green-700">Connections:</span>
                    <span className="text-sm font-semibold text-green-800">12/50</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-green-700">Cache Hit:</span>
                    <span className="text-sm font-semibold text-green-800">87%</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              <div className="bg-gray-50 rounded-lg p-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">Error Logs</h2>
                <div className="space-y-3">
                  <div className="bg-red-50 border-l-4 border-red-500 p-3">
                    <p className="text-sm font-semibold text-red-800">API Timeout Error</p>
                    <p className="text-xs text-red-600">2 minutes ago - /api/users endpoint</p>
                  </div>
                  <div className="bg-yellow-50 border-l-4 border-yellow-500 p-3">
                    <p className="text-sm font-semibold text-yellow-800">High Memory Usage</p>
                    <p className="text-xs text-yellow-600">15 minutes ago - Server warning</p>
                  </div>
                  <div className="bg-green-50 border-l-4 border-green-500 p-3">
                    <p className="text-sm font-semibold text-green-800">System Recovery</p>
                    <p className="text-xs text-green-600">1 hour ago - Auto-restart completed</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 rounded-lg p-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">Deployment Status</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-gray-800">Production</p>
                      <p className="text-sm text-gray-600">v2.1.4 - Stable</p>
                    </div>
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-gray-800">Staging</p>
                      <p className="text-sm text-gray-600">v2.1.5 - Testing</p>
                    </div>
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-gray-800">Development</p>
                      <p className="text-sm text-gray-600">v2.2.0 - In Progress</p>
                    </div>
                    <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg p-6 text-white">
              <h2 className="text-2xl font-semibold mb-4">Real-time Monitoring</h2>
              <div className="grid md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-3xl font-bold mb-1">99.9%</div>
                  <p className="text-purple-100">Uptime</p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold mb-1">180ms</div>
                  <p className="text-purple-100">Avg Response</p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold mb-1">1.2K</div>
                  <p className="text-purple-100">Requests/min</p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold mb-1">0</div>
                  <p className="text-purple-100">Active Issues</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Technical;
