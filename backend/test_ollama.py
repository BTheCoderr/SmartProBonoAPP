import requests
import os

def test_ollama():
    endpoint = os.environ.get('OLLAMA_ENDPOINT', 'http://localhost:11434')
    try:
        response = requests.post(
            f"{endpoint}/api/generate",
            json={
                "model": "mistral",
                "prompt": "Hello, are you working?",
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            print("✅ Ollama is running and responding")
            data = response.json()
            print("Response:", data['response'])
        else:
            print("❌ Ollama returned status:", response.status_code)
    except Exception as e:
        print("❌ Error connecting to Ollama:", str(e))

if __name__ == "__main__":
    test_ollama() 