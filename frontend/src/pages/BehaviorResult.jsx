import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function BehaviorResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const response = location.state?.response || 'No response recorded';
  const feedback = location.state?.feedback || 'No feedback received';

  const handleBack = () => {
    navigate('/behavior');
  };

  return (
    <div 
      className="h-full w-full flex flex-col items-center justify-center" 
      style={{ backgroundColor: '#FFFFFF', padding: '20px', color: '#000000', fontFamily: 'sans-serif' }}
    >
      <div className="max-w-3xl w-full" style={{ paddingTop: '20px' }}>
        
        {/* Title */}
        <h1 
          className="text-3xl font-bold text-center" 
          style={{ 
            marginBottom: '24px', 
            color: '#552583', 
            borderBottom: '3px solid #FDB927', 
            display: 'inline-block', 
            paddingBottom: '6px'
          }}
        >
          Review Your Response
        </h1>

        {/* Your Recorded Response */}
        <div 
          className="shadow-md" 
          style={{ 
            marginBottom: '24px', 
            backgroundColor: '#FDB927', 
            color: '#000000',
            fontWeight: 500,
            padding: '16px',
            borderRadius: '10px',
            border: '2px solid #552583'
          }}
        >
          <h2 className="text-lg font-semibold mb-3" style={{ color: '#552583' }}>
            Your Recorded Response:
          </h2>
          <div 
            className="w-full p-3 border rounded-lg overflow-y-auto"
            style={{
              minHeight: '150px',
              maxHeight: '200px',
              backgroundColor: '#FFFFFF',
              borderColor: '#552583',
              borderWidth: '2px',
              fontSize: '0.95rem'
            }}
          >
            <p className="leading-relaxed whitespace-pre-wrap">{response}</p>
          </div>
        </div>
        
        {/* AI Feedback */}
        <div 
          className="shadow-md" 
          style={{ 
            marginBottom: '24px', 
            backgroundColor: '#FDFCFB', 
            padding: '16px',
            borderRadius: '10px',
            border: '2px solid #552583'
          }}
        >
          <h2 className="text-lg font-semibold mb-3" style={{ color: '#552583' }}>
            AI Feedback:
          </h2>
          <div 
            className="w-full p-3 border rounded-lg overflow-y-auto"
            style={{
              minHeight: '150px',
              maxHeight: '200px',
              backgroundColor: '#FFFFFF',
              borderColor: '#FDB927',
              borderWidth: '2px',
              fontSize: '0.95rem'
            }}
          >
            <p className="leading-relaxed whitespace-pre-wrap">{feedback}</p>
          </div>
        </div>
        
        {/* Buttons */}
        <div className="text-center" style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <button
            onClick={handleBack}
            style={{
              backgroundColor: '#FDB927',
              color: '#000000',
              padding: '10px 20px',
              borderRadius: '8px',
              fontSize: '0.95rem',
              fontWeight: '600',
              border: 'none',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = '#FFC94D'}
            onMouseLeave={(e) => e.target.style.backgroundColor = '#FDB927'}
          >
            Back
          </button>
          <button
            onClick={() => navigate('/technical')}
            style={{
              backgroundColor: '#552583',
              color: '#FFFFFF',
              padding: '10px 24px',
              borderRadius: '8px',
              fontSize: '0.95rem',
              fontWeight: '600',
              border: 'none',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = '#6E3AA9'}
            onMouseLeave={(e) => e.target.style.backgroundColor = '#552583'}
          >
            Continue to Technical Interview
          </button>
        </div>
      </div>
    </div>
  );
}

export default BehaviorResult;
