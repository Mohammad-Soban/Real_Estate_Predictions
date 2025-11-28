"""
Quick Setup and Test for Local Ollama
This script helps you set up and test Ollama (local LLM - no API key needed!)
"""

import os
import requests
import subprocess
import sys

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, version
        return False, None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, None

def check_ollama_running():
    """Check if Ollama server is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        return response.status_code == 200
    except:
        return False

def list_ollama_models():
    """List installed Ollama models"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout
        return None
    except:
        return None

def test_ollama_generate():
    """Test Ollama text generation"""
    try:
        API_URL = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama2",
            "prompt": "Write a one-sentence description of a 3 BHK apartment in Ahmedabad.",
            "stream": False
        }
        
        print("🔄 Testing text generation with Ollama...")
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('response', '')
            return True, content
        return False, f"Error: Status {response.status_code}"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("🏠 OLLAMA LOCAL LLM SETUP & TEST")
    print("=" * 80)
    print()
    
    # Step 1: Check if Ollama is installed
    print("📦 Step 1: Checking Ollama installation...")
    installed, version = check_ollama_installed()
    
    if not installed:
        print("❌ Ollama is NOT installed")
        print()
        print("📥 To install Ollama:")
        print("   1. Visit: https://ollama.ai/download")
        print("   2. Download Windows installer")
        print("   3. Install and restart this script")
        print()
        return False
    
    print(f"✅ Ollama installed: {version}")
    print()
    
    # Step 2: Check if Ollama is running
    print("🔄 Step 2: Checking if Ollama is running...")
    running = check_ollama_running()
    
    if not running:
        print("⚠️  Ollama server is not running")
        print()
        print("🚀 Starting Ollama server...")
        print("   Run this in a separate PowerShell window:")
        print("   > ollama serve")
        print()
        print("   Then run this script again!")
        return False
    
    print("✅ Ollama server is running")
    print()
    
    # Step 3: List available models
    print("📋 Step 3: Checking installed models...")
    models = list_ollama_models()
    
    if models:
        print(models)
    else:
        print("⚠️  No models found")
    
    # Check if llama2 is installed
    if models and 'llama2' not in models.lower():
        print()
        print("📥 Recommended: Install llama2 model")
        print("   Run: ollama pull llama2")
        print()
        choice = input("Would you like to install llama2 now? (y/n): ").lower()
        if choice == 'y':
            print("⏳ Downloading llama2 (this may take 5-10 minutes)...")
            try:
                subprocess.run(['ollama', 'pull', 'llama2'], check=True)
                print("✅ llama2 installed successfully!")
            except:
                print("❌ Failed to install llama2. Try manually: ollama pull llama2")
                return False
    
    print()
    
    # Step 4: Test generation
    print("🧪 Step 4: Testing text generation...")
    success, result = test_ollama_generate()
    
    if success:
        print("✅ SUCCESS! Ollama is working!")
        print()
        print("Generated Content:")
        print("-" * 80)
        print(result)
        print("-" * 80)
        print()
        print("✨ You're ready to use Ollama with main_phase2.py!")
        print()
        print("🚀 Next steps:")
        print("   1. Keep Ollama running (ollama serve)")
        print("   2. Run: python main_phase2.py")
        print("   3. Process your properties with LOCAL AI!")
        print()
        print("💡 Benefits:")
        print("   - No API key needed")
        print("   - Works offline")
        print("   - Unlimited usage")
        print("   - 100% private")
        return True
    else:
        print(f"❌ Test failed: {result}")
        print()
        print("🔧 Troubleshooting:")
        print("   1. Make sure llama2 is installed: ollama pull llama2")
        print("   2. Restart Ollama: ollama serve")
        print("   3. Check if port 11434 is available")
        return False

if __name__ == "__main__":
    print()
    success = main()
    print()
    print("=" * 80)
    
    if success:
        print("✅ Ollama Setup Complete!")
        print()
        print("Available Models:")
        print("  - llama2 (4GB) - Good quality, fast")
        print("  - llama3.1 (7GB) - Best quality (run: ollama pull llama3.1)")
        print("  - mistral (4GB) - Alternative (run: ollama pull mistral)")
        print()
        print("To switch models, edit src/nlp/brochure_generator.py line ~117")
        print('Change: "model": "llama2" to your preferred model')
    else:
        print("❌ Setup incomplete. Follow steps above.")
    
    print("=" * 80)
