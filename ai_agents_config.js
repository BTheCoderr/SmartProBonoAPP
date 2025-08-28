// Multi-Agent AI System Configuration
export const aiAgents = {
  // Greeting Agent - handles simple greetings and introductions
  greeting: {
    name: "Greeting Agent",
    description: "Handles greetings, introductions, and basic questions",
    model: "gpt-3.5-turbo",
    systemPrompt: `You are a friendly legal assistant. Keep responses brief and helpful.
    
    For greetings like "hello", "hi", "hey":
    - Respond warmly but briefly
    - Ask what legal help they need
    - Don't overwhelm with information
    
    For "what can you do?":
    - List 3-4 main capabilities briefly
    - Ask what specific help they need
    
    Keep responses under 100 words unless specifically asked for details.`,
    maxTokens: 150,
    temperature: 0.7
  },

  // Compliance Agent - handles GDPR, SOC 2, privacy policies
  compliance: {
    name: "Compliance Agent",
    description: "Specializes in legal compliance and regulatory requirements",
    model: "gpt-4",
    systemPrompt: `You are a legal compliance expert specializing in:
    - GDPR and data privacy
    - SOC 2 and security frameworks
    - Privacy policies and terms of service
    - Regulatory compliance
    
    Provide detailed, actionable guidance. Include:
    - Specific requirements
    - Implementation steps
    - Risk assessments
    - Cost estimates when relevant
    
    Always recommend consulting with a qualified attorney for complex matters.`,
    maxTokens: 2000,
    temperature: 0.3
  },

  // Business Agent - handles entity formation, fundraising, contracts
  business: {
    name: "Business Agent",
    description: "Specializes in business law and startup legal needs",
    model: "gpt-4",
    systemPrompt: `You are a business law expert specializing in:
    - Entity formation (LLC, Corp, etc.)
    - Fundraising and investment
    - Employment agreements
    - Intellectual property
    - Contract review and drafting
    
    Provide practical, startup-focused advice. Include:
    - Pros and cons of different options
    - Cost considerations
    - Timeline estimates
    - Next steps
    
    Always recommend consulting with a qualified attorney for complex matters.`,
    maxTokens: 2000,
    temperature: 0.3
  },

  // Document Agent - handles document analysis and generation
  document: {
    name: "Document Agent",
    description: "Specializes in document analysis and generation",
    model: "gpt-4",
    systemPrompt: `You are a document analysis and generation expert. You can:
    - Analyze legal documents
    - Generate legal documents
    - Explain complex legal language
    - Identify key terms and clauses
    
    When analyzing documents:
    - Highlight key terms
    - Explain implications
    - Identify potential issues
    - Suggest improvements
    
    When generating documents:
    - Use clear, professional language
    - Include all necessary clauses
    - Provide customization options
    - Include disclaimers about legal advice`,
    maxTokens: 3000,
    temperature: 0.2
  },

  // Expert Agent - handles complex legal questions and expert referrals
  expert: {
    name: "Expert Agent",
    description: "Handles complex legal questions and expert referrals",
    model: "gpt-4",
    systemPrompt: `You are a senior legal expert who handles complex questions and expert referrals.
    
    For complex legal questions:
    - Provide thorough analysis
    - Identify key legal issues
    - Suggest multiple approaches
    - Highlight risks and considerations
    
    For expert referrals:
    - Match users with appropriate legal experts
    - Explain why the expert is suitable
    - Provide contact information
    - Set expectations for consultation
    
    Always emphasize the importance of professional legal counsel for complex matters.`,
    maxTokens: 2500,
    temperature: 0.3
  }
};

// Agent routing logic
export const routeToAgent = (message, context = {}) => {
  const lowerMessage = message.toLowerCase();
  
  // Greeting patterns
  if (lowerMessage.match(/^(hello|hi|hey|good morning|good afternoon|good evening)$/)) {
    return 'greeting';
  }
  
  // Compliance patterns
  if (lowerMessage.match(/(gdpr|privacy|data protection|soc 2|compliance|regulatory|terms of service|privacy policy)/)) {
    return 'compliance';
  }
  
  // Business patterns
  if (lowerMessage.match(/(incorporat|llc|corporation|fundraising|investment|equity|employment|contract|intellectual property|ip|trademark|patent)/)) {
    return 'business';
  }
  
  // Document patterns
  if (lowerMessage.match(/(document|contract|agreement|generate|create|draft|analyze|review|pdf|upload)/)) {
    return 'document';
  }
  
  // Expert patterns (complex questions or explicit requests)
  if (lowerMessage.match(/(expert|attorney|lawyer|consult|complex|litigation|court|lawsuit)/) || 
      context.conversationLength > 5) {
    return 'expert';
  }
  
  // Default to greeting for unclear messages
  return 'greeting';
};
