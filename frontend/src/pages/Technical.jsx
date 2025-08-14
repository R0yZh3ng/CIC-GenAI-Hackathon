import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Editor from "@monaco-editor/react";

export default function Technical({question = "Given the root of a binary tree, return the level order traversal of its nodes' values."}) {
  const navigate = useNavigate();
  
  // Left pane content (unchanged, just styled)
  const leftTitle = "Problem Description";
  const leftText = question;

  // Code editor state
  const [code, setCode] = useState(`// Type your C++ solution here
#include <bits/stdc++.h>
using namespace std;

int main() {
    return 0;
}
`);

  const handleSubmit = async () => {
    try {
      // Show loading state (optional)
      console.log('Sending code to backend:', code);
      
      // TODO: Replace with your actual backend endpoint
      const apiResponse = await fetch('/api/technical-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          code: code
        })
      });
      
      if (!apiResponse.ok) {
        throw new Error('Failed to get feedback');
      }
      
      const data = await apiResponse.json();
      const feedback = data.feedback; // Assuming your backend returns { feedback: "string" }
      
      // Navigate to TechnicalResult page with both code and feedback
      navigate('/technical-result', { 
        state: { 
          code: code, 
          feedback: feedback 
        } 
      });
      
    } catch (error) {
      console.error('Error getting feedback:', error);
      // Handle error - maybe show a message or navigate with just the code
      navigate('/technical-result', { 
        state: { 
          code: code, 
          feedback: 'Error: Could not get feedback from server' 
        } 
      });
    }
  };

  return (
    <div style={styles.container}>
      {/* Left Pane (Lakers purple) */}
      <div style={styles.leftPane}>
        <h2 style={styles.leftHeading}>{leftTitle}</h2>
        <p style={styles.leftText}>{leftText}</p>
      </div>

      {/* Right Pane (Lakers gold) */}
      <div style={styles.rightPane}>
        <h2 style={styles.rightHeading}>Your C++ Solution</h2>

        <div style={styles.editorWrapper}>
          <Editor
            height="100%"
            defaultLanguage="cpp"
            value={code}
            // keep your existing Monaco theme (you mentioned monokai already set)
            theme="vs-dark"
            onChange={(v) => setCode(v || "")}
            options={{
              fontSize: 14,
              fontFamily: "Fira Code, monospace",
              minimap: { enabled: false },
              wordWrap: "on",
            }}
          />
        </div>

        <button style={styles.button} onClick={handleSubmit}>
          Submit Code
        </button>
      </div>
    </div>
  );
}

const LAKERS_PURPLE = "#552583";
const LAKERS_GOLD = "#FDB927";
const LAKERS_GOLD_DARK = "#C69214"; // for hover/border accents

const styles = {
  container: {
    display: "flex",
    height: "100vh",
    backgroundColor: "#0e0e0e", // neutral dark to let purple/gold pop
    gap: 12,
    padding: 12,
  },

  // Left: Purple
  leftPane: {
    flex: 1,
    backgroundColor: LAKERS_PURPLE,
    padding: 20,
    borderRadius: 10,
    border: `2px solid ${LAKERS_GOLD}`,
    boxShadow: "0 6px 20px rgba(0,0,0,0.3)",
    overflow: "auto",
    margin: 10,
    marginBottom: 30,
  },
  leftHeading: {
    color: LAKERS_GOLD,
    margin: "0 0 8px",
    fontWeight: 700,
    letterSpacing: 0.4,
  },
  leftText: {
    color: "#ffffff",
    lineHeight: 1.5,
  },

  // Right: Gold
  rightPane: {
    flex: 1,
    backgroundColor: LAKERS_GOLD,
    padding: 20,
    borderRadius: 10,
    border: `2px solid ${LAKERS_PURPLE}`,
    boxShadow: "0 6px 20px rgba(0,0,0,0.3)",
    display: "flex",
    flexDirection: "column",
    gap: 12,
    margin: 10,
    marginBottom: 30, 
  },
  rightHeading: {
    color: LAKERS_PURPLE,
    margin: "0 0 8px",
    fontWeight: 800,
    letterSpacing: 0.4,
  },

  editorWrapper: {
    flex: 1,
    border: `2px solid ${LAKERS_GOLD_DARK}`,
    borderRadius: 8,
    overflow: "hidden",
    minHeight: 320,
    background: "#1e1e1e", // keeps a clean frame around Monokai/dark editor
  },

  button: {
    alignSelf: "flex-start",
    background: LAKERS_PURPLE,
    color: "#fff",
    border: `2px solid ${LAKERS_GOLD}`,
    borderRadius: 8,
    padding: "10px 16px",
    cursor: "pointer",
    fontWeight: 700,
    letterSpacing: 0.3,
    transition: "transform 120ms ease, background 120ms ease, border-color 120ms ease",
  },
};

// Optional: simple hover effect (inline)
styles.button.onMouseOver = function () {
  this.background = "#4a1f73";
  this.borderColor = LAKERS_GOLD_DARK;
  this.transform = "translateY(-1px)";
};
styles.button.onMouseOut = function () {
  this.background = LAKERS_PURPLE;
  this.borderColor = LAKERS_GOLD;
  this.transform = "translateY(0)";
};