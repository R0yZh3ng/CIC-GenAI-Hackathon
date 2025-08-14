import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

function Behavior() {
  const [response, setResponse] = useState('');
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);
  const navigate = useNavigate();
  
  const question = "Tell me about a time when you had to work with a difficult team member. How did you handle the situation and what was the outcome?";
  
  const startListening = () => {
    setResponse('');
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';
      
      recognitionRef.current.onstart = () => setIsListening(true);
      
      recognitionRef.current.onresult = (event) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const result = event.results[i];
          if (result.isFinal) {
            for (let j = 0; j < result.length; j++) {
              const alternative = result[j];
              if (alternative.transcript) {
                finalTranscript += alternative.transcript;
              }
            }
          }
        }
        if (finalTranscript.trim() && finalTranscript !== 'undefined') {
          setResponse(prev => (prev.trim() + ' ' + finalTranscript.trim()).trim());
        }
      };
      
      recognitionRef.current.onerror = () => setIsListening(false);
      recognitionRef.current.onend = () => setIsListening(false);
      
      recognitionRef.current.start();
    } else {
      alert('Speech recognition is not supported in this browser.');
    }
  };
  
  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };
  
  const handleSubmit = async () => {
    try {
      const apiResponse = await fetch('/api/behavioral-feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, response })
      });
      
      if (!apiResponse.ok) throw new Error('Failed to get feedback');
      
      const data = await apiResponse.json();
      navigate('/behavior-result', { 
        state: { response, feedback: data.feedback } 
      });
    } catch {
      navigate('/behavior-result', { 
        state: { response, feedback: 'Error: Could not get feedback from server' } 
      });
    }
  };

  return (
    <div 
      className="h-full w-full flex flex-col items-center justify-center" 
      style={{ backgroundColor: '#FFFFFF', padding: '40px', color: '#000000', fontFamily: 'sans-serif' }}
    >
      <div className="max-w-4xl w-full" style={{ paddingTop: '40px' }}>
        
        {/* Title */}
        <h1 
          className="text-4xl font-bold text-center" 
          style={{ 
            marginBottom: '40px', 
            color: '#552583', 
            borderBottom: '4px solid #FDB927', 
            display: 'inline-block', 
            paddingBottom: '8px'
          }}
        >
          Behavioral Question
        </h1>

        {/* Question Box - Gold with Rounded Edges */}
        <div 
          className="shadow-lg" 
          style={{ 
            marginBottom: '40px', 
            backgroundColor: '#FDB927', 
            color: '#000000',
            fontWeight: 500,
            padding: '24px',
            borderRadius: '12px', // Rounded corners
            border: '2px solid #552583' // Purple border for Lakers theme
          }}
        >
          <p className="text-lg leading-relaxed">{question}</p>
        </div>

        {/* Recording Box */}
        <div 
          className="rounded-lg p-6 shadow-lg" 
          style={{ marginBottom: '40px', backgroundColor: '#FDFCFB', borderRadius: '12px' }}
        >
          <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <button
              onClick={isListening ? stopListening : startListening}
              style={{
                padding: '10px 20px',
                borderRadius: '8px',
                fontWeight: '600',
                backgroundColor: isListening ? '#552583' : '#FDB927',
                color: isListening ? '#FFFFFF' : '#000000',
                border: 'none',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.target.style.backgroundColor = isListening ? '#6E3AA9' : '#FFC94D';
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = isListening ? '#552583' : '#FDB927';
              }}
            >
              {isListening ? '🛑 Stop Recording' : '🎤 Start Recording'}
            </button>
            {isListening && (
              <span style={{ color: '#552583', fontWeight: 'bold', fontSize: '1.1rem' }}>● Recording...</span>
            )}
          </div>

          {/* Transcript Box */}
          <div
            className="w-full h-64 p-4 border rounded-lg overflow-y-auto"
            style={{
              minHeight: '256px',
              backgroundColor: '#FFFFFF',
              borderColor: '#552583',
              borderWidth: '2px'
            }}
          >
            {response ? (
              <p className="leading-relaxed whitespace-pre-wrap">{response}</p>
            ) : (
              <p style={{ color: '#999999', fontStyle: 'italic' }}>
                Your response will appear here when you start speaking...
              </p>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <div className="text-center">
          <button
            onClick={handleSubmit}
            style={{
              backgroundColor: '#552583',
              color: '#FFFFFF',
              padding: '12px 32px',
              borderRadius: '8px',
              fontSize: '1.1rem',
              fontWeight: '600',
              border: 'none',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = '#6E3AA9'}
            onMouseLeave={(e) => e.target.style.backgroundColor = '#552583'}
          >
            Submit Response
          </button>
        </div>
      </div>
    </div>
  );
}

export default Behavior;
