import { callModel } from '../../llm.js'
import { AgentState } from '../index.js'

export const plannerNode = async (state: AgentState): Promise<Partial<AgentState>> => {
  console.log('🧠 PLANNER: Analyzing goal and creating plan...')
  
  const prompt = `You are a senior tech lead for SmartProBono, a legal tech platform.

GOAL: ${state.goal}

CONTEXT: SmartProBono has:
- React frontend (Material-UI, TypeScript)
- Python Flask backend (Supabase database)
- CRM systems for lawyers and bondsmen
- Document generation and scanning
- Real-time features with WebSocket

Create a numbered plan with minimal, atomic steps. Focus on:
1. What files need to be modified
2. What tests need to be added
3. What API endpoints might be needed
4. Keep changes focused and minimal

Return only the numbered plan steps, nothing else.`

  try {
    const planText = await callModel(prompt)
    const plan = planText
      .split('\n')
      .filter(line => line.trim() && /^\d+/.test(line.trim()))
      .map(line => line.trim())
    
    console.log(`📋 Plan created with ${plan.length} steps:`)
    plan.forEach((step, i) => console.log(`  ${i + 1}. ${step}`))
    
    return { 
      ...state, 
      plan,
      iteration: 1
    }
  } catch (error) {
    console.error('❌ Planner failed:', error)
    return { 
      ...state, 
      feedback: `Planning failed: ${error.message}`,
      done: true 
    }
  }
}
