"""
Test AI Connection - Supports Groq, Mistral, Ollama, and HuggingFace
This script tests which AI options are available and working.
"""

import os
import requests
import json

def test_groq_api():
    """Test Groq AI API"""
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        return False, "No API key"
    
    try:
        API_URL = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-70b-versatile",
            "messages": [{"role": "user", "content": "Write one sentence about a 3 BHK apartment."}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            return True, content
        return False, f"Status {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_ollama():
    """Test local Ollama"""
    try:
        # Check if Ollama is running
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code != 200:
            return False, "Ollama not running"
        
        # Test generation
        API_URL = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama2",
            "prompt": "Write one sentence about a 3 BHK apartment.",
            "stream": False
        }
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('response', '')
            return True, content
        return False, f"Status {response.status_code}"
    except:
        return False, "Ollama not available"

def test_mistral_api():
    """Test Mistral API"""
    api_key = os.environ.get('MISTRAL_API_KEY')
    if not api_key:
        return False, "No API key"
    
    try:
        API_URL = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": "Write one sentence about a 3 BHK apartment."}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            return True, content
        return False, f"Status {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_huggingface_api():
    """Test HuggingFace API"""
    api_key = os.environ.get('HUGGINGFACE_API_KEY')
    if not api_key:
        return False, "No API key"
    
    return False, "HuggingFace inference API has reliability issues"

def main():
    """Test all available AI options"""
    
    print("=" * 80)
    print("🧪 AI CONNECTION TEST - ALL OPTIONS")
    print("=" * 80)
    print()
    
    working_ai = None
    
    # Test Groq
    print("🌟 Testing Groq AI (RECOMMENDED)...")
    api_key = os.environ.get('GROQ_API_KEY')
    
    if api_key:
        print(f"   API Key: {api_key[:8]}...{api_key[-4:]}")
        success, result = test_groq_api()
        if success:
            print("   ✅ SUCCESS!")
            print(f"   Generated: {result[:80]}...")
            working_ai = "Groq"
        else:
            print(f"   ❌ Failed: {result}")
    else:
        print("   ⚠️  No API key set")
        print("   Setup: $env:GROQ_API_KEY='your_key'")
        print("   Get key: https://console.groq.com/")
    print()
    
    # Test Ollama
    print("🏠 Testing Local Ollama...")
    success, result = test_ollama()
    if success:
        print("   ✅ SUCCESS!")
        print(f"   Generated: {result[:80]}...")
        if not working_ai:
            working_ai = "Ollama"
    else:
        print(f"   ⚠️  {result}")
        print("   Setup: https://ollama.ai/download")
        print("   Then run: ollama pull llama2")
    print()
    
    # Test Mistral
    print("🤖 Testing Mistral AI...")
    api_key = os.environ.get('MISTRAL_API_KEY')
    if api_key:
        print(f"   API Key: {api_key[:8]}...{api_key[-4:]}")
        success, result = test_mistral_api()
        if success:
            print("   ✅ SUCCESS!")
            print(f"   Generated: {result[:80]}...")
            if not working_ai:
                working_ai = "Mistral"
        else:
            print(f"   ❌ Failed: {result}")
    else:
        print("   ⚠️  No API key set")
        print("   Setup: $env:MISTRAL_API_KEY='your_key'")
        print("   Get key: https://console.mistral.ai/")
    print()
    
    # Test HuggingFace
    print("🤗 Testing HuggingFace...")
    api_key = os.environ.get('HUGGINGFACE_API_KEY')
    if api_key:
        print(f"   API Key: {api_key[:8]}...{api_key[-4:]}")
        success, result = test_huggingface_api()
        if success:
            print("   ✅ SUCCESS!")
            if not working_ai:
                working_ai = "HuggingFace"
        else:
            print(f"   ⚠️  {result}")
    else:
        print("   ⚠️  No API key set")
    print()
    
    print("=" * 80)
    print()
    
    if working_ai:
        print(f"✅ READY TO GO! Using: {working_ai}")
        print()
        print("🚀 Next Steps:")
        print("   1. Run: python main_phase2.py")
        print("   2. Select option 1 to process dataset")
        print("   3. Check CSV 'Content_Source' column")
        print()
        print(f"💡 Your properties will be analyzed with {working_ai}!")
        return True
    else:
        print("❌ NO AI AVAILABLE")
        print()
        print("📋 Quick Setup Options:")
        print()
        print("🌟 FASTEST: Groq AI (2 minutes)")
        print("   $env:GROQ_API_KEY='your_key'")
        print("   Get key: https://console.groq.com/")
        print()
        print("🏠 NO API KEY: Ollama (10 minutes)")
        print("   Download: https://ollama.ai/download")
        print("   Then: ollama pull llama2")
        print()
        print("📖 Full Guide: Open AI_SETUP_OPTIONS.md")
        return False

if __name__ == "__main__":
    print()
    success = main()
    print()
    print("=" * 80)
