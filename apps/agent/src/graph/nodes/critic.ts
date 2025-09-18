import { callModel } from '../../llm.js'
import { AgentState } from '../index.js'

export const criticNode = async (state: AgentState): Promise<Partial<AgentState>> => {
  console.log('🔍 CRITIC: Evaluating results...')
  
  const prompt = `You are a senior code reviewer for SmartProBono.

GOAL: ${state.goal}
PLAN STEP: ${state.plan?.[state.iteration! - 1] || 'Unknown'}
TEST RESULTS:
${state.runReport}

PREVIOUS FEEDBACK: ${state.feedback || 'None'}

Evaluate if:
1. Tests are passing
2. The current plan step is complete
3. The overall goal is satisfied

If tests fail or step incomplete:
- Provide specific, actionable feedback
- Set done=false

If tests pass AND goal is fully satisfied:
- Set done=true
- Congratulate on completion

Response format:
FEEDBACK: [your feedback]
DONE: [true/false]`

  try {
    const response = await callModel(prompt)
    
    const feedbackMatch = response.match(/FEEDBACK:\s*(.+?)(?=\nDONE:|$)/s)
    const doneMatch = response.match(/DONE:\s*(true|false)/i)
    
    const feedback = feedbackMatch?.[1]?.trim() || 'No feedback provided'
    const done = doneMatch?.[1]?.toLowerCase() === 'true'
    
    console.log(`🎯 Critic decision: ${done ? 'DONE' : 'CONTINUE'}`)
    console.log(`💬 Feedback: ${feedback.slice(0, 100)}...`)
    
    return { 
      ...state, 
      feedback,
      done 
    }
    
  } catch (error) {
    console.error('❌ Critic failed:', error)
    return { 
      ...state, 
      feedback: `Critic evaluation failed: ${error.message}`,
      done: true 
    }
  }
}
