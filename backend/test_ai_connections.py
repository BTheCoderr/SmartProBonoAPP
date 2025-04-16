import asyncio
from services.ai_service_manager import ai_service_manager, AIProvider
import time

async def test_model_connection(provider: AIProvider, task_type: str, test_prompt: str):
    print(f"\n🔍 Testing {provider.value} for {task_type}...")
    start_time = time.time()
    try:
        response = await ai_service_manager.get_response(
            prompt=test_prompt,
            provider=provider,
            task_type=task_type
        )
        duration = time.time() - start_time
        print(f"✅ Success! ({duration:.2f}s)")
        print(f"🤖 Model: {response['model']}")
        print(f"📝 Sample response: {response['text'][:150]}...")
        print(f"🔢 Tokens: {response['tokens']}")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

async def main():
    print("🚀 Starting API Connection Tests\n")
    
    test_cases = [
        # Basic legal Q&A with Mistral
        (AIProvider.MISTRAL, "chat", "What are the basic tenant rights?"),
        
        # Simple document task with Llama
        (AIProvider.LLAMA, "document_drafting", "Create a basic NDA template"),
        
        # Legal research with DeepSeek
        (AIProvider.DEEPSEEK, "legal_research", "Explain fair use in copyright law"),
        
        # Analysis with Falcon
        (AIProvider.FALCON, "statute_interpretation", "Explain Section 230 basics")
    ]
    
    results = []
    for provider, task, prompt in test_cases:
        success = await test_model_connection(provider, task, prompt)
        results.append((provider.value, success))
    
    print("\n📊 Test Summary:")
    for model, success in results:
        status = "✅ Working" if success else "❌ Failed"
        print(f"{model}: {status}")

if __name__ == "__main__":
    print("🔑 Using Hugging Face API for inference")
    asyncio.run(main()) 