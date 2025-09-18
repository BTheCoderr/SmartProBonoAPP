import Anthropic from '@anthropic-ai/sdk'

const client = new Anthropic({ 
  apiKey: process.env.ANTHROPIC_API_KEY 
})

export async function callModel(prompt: string, maxTokens = 4000): Promise<string> {
  try {
    const response = await client.messages.create({
      model: process.env.MODEL_NAME || 'claude-3-5-sonnet-20240620',
      max_tokens: maxTokens,
      messages: [{ 
        role: 'user', 
        content: prompt 
      }]
    })
    
    // Extract text content from response
    const content = response.content
    if (Array.isArray(content)) {
      return content
        .filter(block => block.type === 'text')
        .map(block => (block as any).text)
        .join('\n')
    }
    
    return ''
  } catch (error) {
    console.error('LLM call failed:', error)
    throw error
  }
}

export function estimateCost(tokens: number, model = 'claude-3-5-sonnet'): number {
  // Rough cost estimates (per 1M tokens)
  const costs = {
    'claude-3-5-sonnet': 15, // $15 per 1M tokens
    'gpt-4o': 10,
    'llama-3.1-70b': 0.8
  }
  
  const costPer1M = costs[model as keyof typeof costs] || 15
  return (tokens / 1000000) * costPer1M
}
