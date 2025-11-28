"""Quick Ollama Test"""
import requests

print("Testing Ollama connection...")

try:
    # Test if Ollama is running
    response = requests.get('http://localhost:11434/api/tags', timeout=5)
    
    if response.status_code == 200:
        print("✅ Ollama is running!")
        
        # Test text generation
        print("\nTesting text generation...")
        gen_response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama2',
                'prompt': 'Write one sentence about a 3 BHK apartment.',
                'stream': False
            },
            timeout=60
        )
        
        if gen_response.status_code == 200:
            result = gen_response.json()
            content = result.get('response', '')
            print(f"✅ SUCCESS!\n\nGenerated: {content}")
            print("\n🎉 Ollama is ready for your property analysis!")
        else:
            print(f"❌ Generation failed: {gen_response.status_code}")
    else:
        print(f"❌ Ollama not responding: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure Ollama is running!")
