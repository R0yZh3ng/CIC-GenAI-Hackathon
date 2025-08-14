import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-xl p-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-6 text-center">
              Welcome to Our Platform
            </h1>
            
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                <h2 className="text-2xl font-semibold mb-4">Past Analysis</h2>
                <p className="text-blue-100 mb-4">
                  Explore historical data and trends to understand patterns and insights from the past.
                </p>
                <Link 
                  to="/past" 
                  className="inline-block bg-white text-blue-600 px-4 py-2 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
                >
                  View Past Data
                </Link>
              </div>
              
              <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white">
                <h2 className="text-2xl font-semibold mb-4">Behavior Analysis</h2>
                <p className="text-green-100 mb-4">
                  Analyze user behavior patterns and interactions to optimize user experience.
                </p>
                <Link 
                  to="/behavior" 
                  className="inline-block bg-white text-green-600 px-4 py-2 rounded-lg font-semibold hover:bg-green-50 transition-colors"
                >
                  Analyze Behavior
                </Link>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-6 text-white">
              <h2 className="text-2xl font-semibold mb-4">Technical Insights</h2>
              <p className="text-purple-100 mb-4">
                Dive deep into technical metrics, performance data, and system analytics.
              </p>
              <Link 
                to="/technical" 
                className="inline-block bg-white text-purple-600 px-4 py-2 rounded-lg font-semibold hover:bg-purple-50 transition-colors"
              >
                Technical Dashboard
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
