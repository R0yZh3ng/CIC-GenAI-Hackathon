import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function TechnicalResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const code = location.state?.code || 'No code submitted';
  const feedback = location.state?.feedback || 'No feedback received';

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
          Review Your Code
        </h1>

        {/* Code Section */}
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
            Your Submitted Code:
          </h2>
          <div
            className="w-full p-3 border rounded-lg overflow-y-auto"
            style={{
              minHeight: '150px',
              maxHeight: '220px',
              backgroundColor: '#FFFFFF',
              borderColor: '#FDB927',
              borderWidth: '2px'
            }}
          >
            <pre
              className="leading-relaxed whitespace-pre-wrap font-mono"
              style={{ fontSize: '0.9rem', color: '#1f1f1f', margin: 0 }}
            >
              {code}
            </pre>
          </div>
        </div>

        {/* Feedback Section */}
        <div
          className="shadow-md"
          style={{
            marginBottom: '24px',
            backgroundColor: '#FDB927',
            padding: '16px',
            borderRadius: '10px',
            border: '2px solid #552583',
            color: '#000000',
            fontWeight: 500
          }}
        >
          <h2 className="text-lg font-semibold mb-3" style={{ color: '#552583' }}>
            AI Feedback:
          </h2>
          <div
            className="w-full p-3 border rounded-lg overflow-y-auto"
            style={{
              minHeight: '150px',
              maxHeight: '220px',
              backgroundColor: '#FFFFFF',
              borderColor: '#552583',
              borderWidth: '2px',
              fontSize: '0.95rem'
            }}
          >
            <p className="leading-relaxed whitespace-pre-wrap" style={{ color: '#1f1f1f', margin: 0 }}>
              {feedback}
            </p>
          </div>
        </div>

        {/* Button */}
        <div className="text-center">
          <button
            onClick={() => navigate('/')}
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
            onMouseEnter={(e) => (e.target.style.backgroundColor = '#6E3AA9')}
            onMouseLeave={(e) => (e.target.style.backgroundColor = '#552583')}
          >
            Return to Home
          </button>
        </div>
      </div>
    </div>
  );
}

export default TechnicalResult;
