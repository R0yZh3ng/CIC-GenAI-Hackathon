import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function BehaviorResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const response = location.state?.response || 'No response recorded';

  const handleSubmit = () => {
    // TODO: Send response to backend
    console.log('Response to send:', response);
    // Here we'll add the API call to send the response to the backend
  };

  const handleBack = () => {
    navigate('/behavior');
  };

  return (
    <div className="h-full w-full bg-[#F9F4F1] flex flex-col items-center justify-center" style={{padding: '40px'}}>
      <div className="max-w-4xl w-full" style={{paddingTop: '40px'}}>
        <h1 className="text-4xl font-bold text-center text-[#171717]" style={{marginBottom: '40px'}}>Review Your Response</h1>
        
        <div className="bg-white rounded-lg p-6 shadow-md" style={{marginBottom: '40px'}}>
          <h2 className="text-xl font-semibold text-[#1f1f1f] mb-4">Your Recorded Response:</h2>
          <div 
            className="w-full p-4 border border-gray-300 rounded-lg bg-gray-50 overflow-y-auto"
            style={{minHeight: '200px'}}
          >
            <p className="text-[#1f1f1f] leading-relaxed whitespace-pre-wrap">
              {response}
            </p>
          </div>
        </div>
        
        <div className="flex justify-center gap-4">
          <button
            onClick={handleBack}
            className="bg-gray-500 hover:bg-gray-600 text-white px-8 py-3 rounded-lg text-lg font-medium transition-colors duration-200"
          >
            Back to Recording
          </button>
          <button
            onClick={handleSubmit}
            className="bg-[#2c2c2c] hover:bg-[#444444] text-white px-8 py-3 rounded-lg text-lg font-medium transition-colors duration-200"
          >
            Submit Response
          </button>
        </div>
      </div>
    </div>
  );
}

export default BehaviorResult;
