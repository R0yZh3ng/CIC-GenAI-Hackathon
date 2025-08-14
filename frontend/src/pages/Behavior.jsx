import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

function Behavior() {
  const [response, setResponse] = useState('');
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);
  const navigate = useNavigate();
  
  // TODO: Get question from backend
  const question = "Tell me about a time when you had to work with a difficult team member. How did you handle the situation and what was the outcome?";
  
  const startListening = () => {
    // Clear previous response when starting a new recording
    setResponse('');
    
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';
      
      recognitionRef.current.onstart = () => {
        setIsListening(true);
      };
      
      recognitionRef.current.onresult = (event) => {
        console.log('Speech recognition result:', event.results);
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const result = event.results[i];
          if (result.isFinal) {
            // Access the transcript from the nested structure
            for (let j = 0; j < result.length; j++) {
              const alternative = result[j];
              if (alternative.transcript) {
                finalTranscript += alternative.transcript;
              }
            }
          }
        }
        console.log('Final transcript:', finalTranscript);
        if (finalTranscript && finalTranscript.trim() && finalTranscript !== 'undefined') {
          setResponse(prev => {
            const newText = prev.trim() + ' ' + finalTranscript.trim();
            console.log('Setting response to:', newText);
            return newText.trim();
          });
        }
      };
      
      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };
      
      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
      
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
    // Don't navigate automatically - just stop recording
  };
  
  const handleSubmit = () => {
    // TODO: Send response to backend
    console.log('Response to send:', response);
    // Here we'll add the API call to send the response to the backend
    
    // Navigate to BehaviorResult page after submitting
    navigate('/behavior-result', { state: { response: response } });
  };

  return (
    <div className="h-full w-full bg-[#F9F4F1] flex flex-col items-center justify-center" style={{padding: '40px'}}>
      <div className="max-w-4xl w-full" style={{paddingTop: '40px'}}>
                 <h1 className="text-4xl font-bold text-center text-[#171717]" style={{marginBottom: '40px'}}>Behavioral Question</h1>
         
         <div className="bg-white rounded-lg p-6 shadow-md" style={{marginBottom: '40px'}}>
           <p className="text-lg text-[#1f1f1f] leading-relaxed">
             {question}
           </p>
         </div>
         
                   <div className="bg-white rounded-lg p-6 shadow-md" style={{marginBottom: '40px'}}>
            <div style={{marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px'}}>
              <button
                onClick={isListening ? stopListening : startListening}
                className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                  isListening 
                    ? 'bg-red-500 hover:bg-red-600 text-white' 
                    : 'bg-[#2c2c2c] hover:bg-[#444444] text-white'
                }`}
              >
                {isListening ? '🛑 Stop Recording' : '🎤 Start Recording'}
              </button>
              {isListening && (
                <span style={{color: 'red', fontWeight: 'bold'}}>● Recording...</span>
              )}
            </div>
                         <div 
               className="w-full h-64 p-4 border border-gray-300 rounded-lg bg-gray-50 overflow-y-auto"
               style={{minHeight: '256px'}}
             >
               {response ? (
                 <p className="text-[#1f1f1f] leading-relaxed whitespace-pre-wrap">
                   {response}
                 </p>
               ) : (
                 <p className="text-gray-400 italic">
                   Your response will appear here when you start speaking...
                 </p>
               )}
             </div>
          </div>
         
         <div className="text-center">
           <button
             onClick={handleSubmit}
             className="bg-[#2c2c2c] hover:bg-[#444444] text-[#ffffff] px-8 py-3 rounded-lg text-lg font-medium transition-colors duration-200"
           >
             Submit Response
           </button>
         </div>
      </div>
    </div>
  );
}

export default Behavior;
