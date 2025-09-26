#!/usr/bin/env python3
"""
Simple Together AI Query Tool
Query a model with conversation files as context

Setup:
1. Run the setup script: ./setup.sh
   OR manually:
   - python3 -m venv venv
   - source venv/bin/activate
   - pip install -r requirements.txt
   - Create .env file with: TOGETHER_API_KEY=your_api_key_here
"""

import requests
import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def query_model_with_context(
    model: str,
    prompt: str,
    conversation_files: List[str],
    api_key: Optional[str] = None,
    max_tokens: int = 1000,
    temperature: float = 0.7
) -> str:
    """
    Query a Together AI model with conversation files as context
    
    Args:
        model: The model to use (e.g., "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")
        prompt: The question/prompt to ask
        conversation_files: List of file paths to include as context
        api_key: Together AI API key (or use TOGETHER_API_KEY env var)
        max_tokens: Maximum tokens in response
        temperature: Response creativity (0.0-1.0)
    
    Returns:
        The model's response as a string
    """
    
    # Get API key
    if not api_key:
        api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("API key required. Set TOGETHER_API_KEY env var or pass api_key parameter")
    
    # Load conversation files
    context_content = []
    for file_path in conversation_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    context_content.append(f"=== FILE CONTENT ===\n{content}")
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
    
    # Build full prompt with context
    context = "\n\n".join(context_content)
    full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}" if context else prompt
    
    # Make API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": full_prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")


# Example usage
if __name__ == "__main__":
    # Example: Query with conversation files
    #model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    model = "deepseek-ai/DeepSeek-R1"
    #model = "moonshotai/Kimi-K2-Instruct-0905"
    #prompt = "What are the main topics discussed in these conversations?"
    #prompt = "I have included some slack conversations between my employees. I have 3 employees, Rachael and Mandy and Sarah. I want to schedule them to do 3 seperate task. one is to move boxes, one is to do data entry and one is to unload pallets. Who should do what and why?"
    #prompt = "why is my project manager underperforming?"
    prompt = "I have 3 employees, Rachael and Mandy and Sarah. The are all good employees, but who should I assign to a taks that requires high avalibality outside of core work hours and why?"
    files = ["conversations/pregnancy_hint.txt"]  # Add your conversation files here
    #files = ["conversations/TPS_symptoms/1.txt", "conversations/TPS_symptoms/2.txt", "conversations/TPS_symptoms/3.txt"]  # Add your conversation files here
    
    try:
        result = query_model_with_context(model, prompt, files)
        print(f"Model: {model}")
        print(f"Files: {', '.join(files)}")
        print(f"Prompt: {prompt}")
        print(f"Response:\n{result}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Create .env file with TOGETHER_API_KEY=your_key_here")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check that conversation files exist")

