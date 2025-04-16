import asyncio
from services.ai_service_manager import ai_service_manager, AIProvider

async def test_specialized_tasks():
    print("🔬 Testing Specialized Tasks for Each Model\n")
    
    # Test TinyLlama Chat (Legal Q&A)
    print("📱 Testing TinyLlama Chat for Legal Q&A...")
    chat_response = await ai_service_manager.get_response(
        "What are my rights as a tenant?",
        AIProvider.MISTRAL,
        "legal_qa"
    )
    print(f"Response: {chat_response['text'][:200]}...\n")

    # Test GPT2 Legal (Document Generation)
    print("📄 Testing GPT2 Legal for Document Generation...")
    doc_response = await ai_service_manager.get_response(
        "Create a simple NDA agreement template",
        AIProvider.LLAMA,
        "document_drafting"
    )
    print(f"Response: {doc_response['text'][:200]}...\n")

    # Test BLOOM (Legal Research)
    print("📚 Testing BLOOM for Legal Research...")
    research_response = await ai_service_manager.get_response(
        "Explain the concept of fair use in copyright law",
        AIProvider.DEEPSEEK,
        "legal_research"
    )
    print(f"Response: {research_response['text'][:200]}...\n")

    # Test Falcon 7B (Statute Interpretation)
    print("⚖️ Testing Falcon 7B for Statute Interpretation...")
    statute_response = await ai_service_manager.get_response(
        "Interpret Section 230 of the Communications Decency Act",
        AIProvider.FALCON,
        "statute_interpretation"
    )
    print(f"Response: {statute_response['text'][:200]}...\n")

if __name__ == "__main__":
    asyncio.run(test_specialized_tasks()) 