# Data Preprocessing Schemas

This document provides the exact schemas you need to follow when preprocessing your datasets for the AI Interviewer system.

## 1. LeetCode Questions Schema

When preprocessing your LeetCode dataset, structure each question as follows:

```json
{
  "title": "Two Sum",
  "problem_statement": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.",
  "constraints": "2 <= nums.length <= 104\n-109 <= nums[i] <= 109\n-109 <= target <= 109\nOnly one valid answer exists.",
  "examples": [
    {
      "input": "nums = [2,7,11,15], target = 9",
      "output": "[0,1]",
      "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
    },
    {
      "input": "nums = [3,2,4], target = 6",
      "output": "[1,2]",
      "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."
    }
  ],
  "test_cases": [
    {
      "input": {"nums": [2,7,11,15], "target": 9},
      "expected_output": [0,1]
    },
    {
      "input": {"nums": [3,2,4], "target": 6},
      "expected_output": [1,2]
    }
  ],
  "expected_output": "Array of two integers representing indices",
  "difficulty": "easy",
  "tags": ["array", "hash-table"],
  "estimated_time": 15,
  "category_name": "Arrays and Hashing"
}
```

### Required Fields:
- `title`: String - Question title
- `problem_statement`: String - Full problem description
- `difficulty`: String - "easy", "medium", or "hard"
- `category_name`: String - Category for grouping questions

### Optional Fields:
- `constraints`: String - Problem constraints
- `examples`: Array - Example inputs/outputs with explanations
- `test_cases`: Array - Test cases for validation
- `expected_output`: String - Expected output format description
- `tags`: Array - Problem tags
- `estimated_time`: Integer - Estimated time in minutes

## 2. System Design Questions Schema

When preprocessing your System Design dataset:

```json
{
  "title": "Design a URL Shortener",
  "system_requirements": "Design a URL shortening service like TinyURL. The service should be able to take a long URL and return a short URL. When users visit the short URL, they should be redirected to the original long URL.",
  "scale_requirements": "The system should handle 100 million URLs per month with 500 million redirects per month. The system should be highly available with 99.9% uptime.",
  "design_constraints": "URLs should be as short as possible (ideally 6-8 characters). The system should support custom URLs. URLs should not expire.",
  "difficulty": "medium",
  "tags": ["distributed-systems", "databases", "caching"],
  "estimated_time": 45,
  "category_name": "Distributed Systems"
}
```

### Required Fields:
- `title`: String - Question title
- `system_requirements`: String - What the system should do
- `difficulty`: String - "easy", "medium", or "hard"
- `category_name`: String - Category for grouping questions

### Optional Fields:
- `scale_requirements`: String - Scale and performance requirements
- `design_constraints`: String - Design constraints and limitations
- `tags`: Array - System design tags
- `estimated_time`: Integer - Estimated time in minutes

## 3. Behavioral Questions Schema

When preprocessing your Behavioral dataset:

```json
{
  "title": "Tell me about a time you faced a difficult challenge",
  "scenario": "Describe a situation where you encountered a significant challenge at work or in a project. Explain how you approached the problem, what actions you took, and what the outcome was.",
  "key_points": [
    "Problem identification and analysis",
    "Strategic thinking and planning",
    "Collaboration and communication",
    "Persistence and adaptability",
    "Results and learning outcomes"
  ],
  "follow_up_questions": [
    "What would you do differently if you faced a similar challenge?",
    "How did this experience help you grow professionally?",
    "What support did you receive from your team or manager?"
  ],
  "difficulty": "medium",
  "tags": ["leadership", "problem-solving", "communication"],
  "estimated_time": 5,
  "category_name": "Leadership and Problem Solving"
}
```

### Required Fields:
- `title`: String - Question title
- `scenario`: String - The behavioral scenario or question
- `difficulty`: String - "easy", "medium", or "hard"
- `category_name`: String - Category for grouping questions

### Optional Fields:
- `key_points`: Array - Key evaluation points to look for
- `follow_up_questions`: Array - Potential follow-up questions
- `tags`: Array - Behavioral question tags
- `estimated_time`: Integer - Estimated time in minutes

## 4. Batch Import Format

For each question type, create a batch import file with this structure:

### LeetCode Batch Import:
```json
{
  "questions": [
    {
      // LeetCode question object (see schema above)
    },
    {
      // Another LeetCode question object
    }
  ]
}
```

### System Design Batch Import:
```json
{
  "questions": [
    {
      // System Design question object (see schema above)
    },
    {
      // Another System Design question object
    }
  ]
}
```

### Behavioral Batch Import:
```json
{
  "questions": [
    {
      // Behavioral question object (see schema above)
    },
    {
      // Another Behavioral question object
    }
  ]
}
```

## 5. API Endpoints for Import

Use these endpoints to import your preprocessed data:

- **LeetCode Questions**: `POST /questions/import/leetcode/`
- **System Design Questions**: `POST /questions/import/system-design/`
- **Behavioral Questions**: `POST /questions/import/behavioral/`

## 6. Example Preprocessing Script

Here's a Python script template to help you preprocess your datasets:

```python
import json
from typing import List, Dict, Any

def preprocess_leetcode_data(raw_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Preprocess raw LeetCode data into the required format"""
    processed_questions = []
    
    for item in raw_data:
        question = {
            "title": item.get("title", ""),
            "problem_statement": item.get("description", ""),
            "constraints": item.get("constraints", ""),
            "examples": item.get("examples", []),
            "test_cases": item.get("test_cases", []),
            "expected_output": item.get("expected_output", ""),
            "difficulty": item.get("difficulty", "medium").lower(),
            "tags": item.get("tags", []),
            "estimated_time": item.get("estimated_time", 15),
            "category_name": item.get("category", "General")
        }
        processed_questions.append(question)
    
    return {"questions": processed_questions}

def preprocess_system_design_data(raw_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Preprocess raw System Design data into the required format"""
    processed_questions = []
    
    for item in raw_data:
        question = {
            "title": item.get("title", ""),
            "system_requirements": item.get("requirements", ""),
            "scale_requirements": item.get("scale", ""),
            "design_constraints": item.get("constraints", ""),
            "difficulty": item.get("difficulty", "medium").lower(),
            "tags": item.get("tags", []),
            "estimated_time": item.get("estimated_time", 45),
            "category_name": item.get("category", "System Design")
        }
        processed_questions.append(question)
    
    return {"questions": processed_questions}

def preprocess_behavioral_data(raw_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Preprocess raw Behavioral data into the required format"""
    processed_questions = []
    
    for item in raw_data:
        question = {
            "title": item.get("title", ""),
            "scenario": item.get("question", ""),
            "key_points": item.get("evaluation_points", []),
            "follow_up_questions": item.get("follow_ups", []),
            "difficulty": item.get("difficulty", "medium").lower(),
            "tags": item.get("tags", []),
            "estimated_time": item.get("estimated_time", 5),
            "category_name": item.get("category", "Behavioral")
        }
        processed_questions.append(question)
    
    return {"questions": processed_questions}

# Example usage:
if __name__ == "__main__":
    # Load your raw data
    with open("raw_leetcode_data.json", "r") as f:
        raw_leetcode = json.load(f)
    
    # Preprocess
    processed_leetcode = preprocess_leetcode_data(raw_leetcode)
    
    # Save processed data
    with open("processed_leetcode_data.json", "w") as f:
        json.dump(processed_leetcode, f, indent=2)
```

## 7. Validation Checklist

Before importing your data, ensure:

- [ ] All required fields are present
- [ ] Difficulty levels are: "easy", "medium", or "hard"
- [ ] Category names are consistent
- [ ] JSON format is valid
- [ ] File sizes are reasonable (under 10MB per batch)
- [ ] No special characters that might cause encoding issues
- [ ] Test cases are properly formatted
- [ ] Tags are relevant and consistent

## 8. Common Issues and Solutions

1. **Encoding Issues**: Ensure your JSON files are UTF-8 encoded
2. **Large Files**: Split large datasets into smaller batches
3. **Missing Fields**: Use empty strings or null for optional fields
4. **Invalid JSON**: Validate your JSON before importing
5. **Duplicate Categories**: The system will automatically handle duplicate category names

This schema ensures your data will be properly imported and used by the AI Interviewer system.
