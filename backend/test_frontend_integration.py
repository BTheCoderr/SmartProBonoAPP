import asyncio
from services.ai_service_manager import ai_service_manager, AIProvider

async def test_frontend_components():
    print("🌐 Testing Frontend Component Integration\n")

    # 1. Legal Chat Component (TinyLlama)
    print("💬 Testing Legal Chat Component...")
    chat_queries = [
        "My landlord hasn't fixed my heating for 2 weeks and it's winter. What are my rights?",
        "I was fired without any warning or explanation after working for 3 years. What can I do?",
        "How do I file a small claims case for an unpaid invoice of $2,500?",
        "My neighbor's tree branches are hanging over my property and damaging my roof. What are my options?"
    ]
    for query in chat_queries:
        response = await ai_service_manager.get_response(
            query,
            AIProvider.MISTRAL,
            "chat"
        )
        print(f"\nQ: {query}")
        print(f"A: {response['text'][:150]}...")

    # 2. Document Generator Component (GPT2)
    print("\n📄 Testing Document Generator Component...")
    doc_requests = [
        {
            "type": "NDA",
            "prompt": "Create a mutual NDA for a web development project. The parties are TechCorp Inc. and John Smith Consulting LLC. Include standard confidentiality terms and a 2-year duration."
        },
        {
            "type": "Lease",
            "prompt": "Generate a 12-month residential lease agreement for a 2-bedroom apartment. Include standard terms for maintenance, utilities, security deposit, and pet policy."
        },
        {
            "type": "Demand Letter",
            "prompt": "Create a demand letter for unpaid freelance services. The amount owed is $3,500 for web design work completed on June 15, 2023. Payment is 60 days overdue."
        }
    ]
    for req in doc_requests:
        response = await ai_service_manager.get_response(
            req["prompt"],
            AIProvider.LLAMA,
            "document_drafting"
        )
        print(f"\nDocument Type: {req['type']}")
        print(f"Generated: {response['text'][:150]}...")

    # 3. Rights Explorer Component (BLOOM)
    print("\n📚 Testing Rights Explorer Component...")
    rights_queries = [
        "Explain tenant rights in California regarding security deposit return timelines and allowable deductions",
        "What are my rights as a pregnant employee in terms of maternity leave and workplace accommodations?",
        "What are my rights regarding overtime pay as a salaried employee in the tech industry?",
        "Explain my rights as a consumer when a product is defective and the store refuses to refund"
    ]
    for query in rights_queries:
        response = await ai_service_manager.get_response(
            query,
            AIProvider.DEEPSEEK,
            "rights_research"
        )
        print(f"\nQ: {query}")
        print(f"A: {response['text'][:150]}...")

    # 4. Legal Analysis Component (Falcon)
    print("\n⚖️ Testing Legal Analysis Component...")
    analysis_requests = [
        "Analyze the implications of GDPR for small US-based e-commerce businesses selling to EU customers",
        "Interpret recent changes to California's independent contractor laws (AB5) and their impact on gig economy workers",
        "Analyze the legal requirements and potential liability issues for collecting user data in a mobile health app",
        "Review the key provisions and compliance requirements of the Americans with Disabilities Act for small businesses"
    ]
    for query in analysis_requests:
        response = await ai_service_manager.get_response(
            query,
            AIProvider.FALCON,
            "complex_analysis"
        )
        print(f"\nAnalysis Request: {query}")
        print(f"Analysis: {response['text'][:150]}...")

if __name__ == "__main__":
    print("🔑 Testing Frontend Integration with Hugging Face Models")
    asyncio.run(test_frontend_components()) 