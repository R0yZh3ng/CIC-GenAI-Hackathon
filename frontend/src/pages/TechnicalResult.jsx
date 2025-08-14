import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function TechnicalResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const code = location.state?.code || 'No code submitted';
  const feedback = location.state?.feedback || 'No feedback received';

  return (
    <div className="h-full w-full bg-[#F9F4F1] flex flex-col items-center justify-center" style={{padding: '40px'}}>
      <div className="max-w-4xl w-full" style={{paddingTop: '40px'}}>
        <h1 className="text-4xl font-bold text-center text-[#171717]" style={{marginBottom: '40px'}}>Review Your Code</h1>
        
        <div className="bg-white rounded-lg p-6 shadow-md" style={{marginBottom: '40px'}}>
          <h2 className="text-xl font-semibold text-[#1f1f1f] mb-4">Your Submitted Code:</h2>
          <div 
            className="w-full p-4 border border-gray-300 rounded-lg bg-gray-50 overflow-y-auto"
            style={{minHeight: '200px'}}
          >
            <pre className="text-[#1f1f1f] leading-relaxed whitespace-pre-wrap font-mono text-sm">
              {code}
            </pre>
          </div>
        </div>
        
        <div className="bg-white rounded-lg p-6 shadow-md" style={{marginBottom: '40px'}}>
          <h2 className="text-xl font-semibold text-[#1f1f1f] mb-4">AI Feedback:</h2>
          <div 
            className="w-full p-4 border border-gray-300 rounded-lg bg-blue-50 overflow-y-auto"
            style={{minHeight: '200px'}}
          >
            <p className="text-[#1f1f1f] leading-relaxed whitespace-pre-wrap">
              {feedback}
            </p>
          </div>
        </div>
        
        <div className="text-center">
          <button
            onClick={() => navigate('/')}
            className="bg-[#2c2c2c] hover:bg-[#444444] text-white px-8 py-3 rounded-lg text-lg font-medium transition-colors duration-200"
          >
            Return to Home
          </button>
        </div>
      </div>
    </div>
  );
}

export default TechnicalResult;
