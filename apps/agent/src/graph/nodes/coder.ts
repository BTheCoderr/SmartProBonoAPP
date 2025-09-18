import { callModel } from '../../llm.js'
import { AgentState } from '../index.js'
import { repoMap, readFile, writeFile } from '../../tools/files.js'
import { allowWrite } from '../../tools/policy.js'

export const coderNode = async (state: AgentState): Promise<Partial<AgentState>> => {
  console.log(`💻 CODER: Working on iteration ${state.iteration || 1}...`)
  
  if (!state.plan || state.plan.length === 0) {
    return { 
      ...state, 
      feedback: 'No plan available for coding',
      done: true 
    }
  }

  try {
    // Get current repo context
    const context = await repoMap()
    const currentStep = state.plan[(state.iteration || 1) - 1]
    
    const prompt = `You are a senior full-stack engineer working on SmartProBono.

CURRENT STEP: ${currentStep}
FULL PLAN: ${state.plan.join('\n')}

REPO CONTEXT:
${context}

PREVIOUS FEEDBACK: ${state.feedback || 'None'}

Instructions:
1. Implement ONLY the current step
2. Return file changes in this format:
   FILE: path/to/file.ext
   CONTENT:
   [full file content here]
   
3. Focus on SmartProBono's existing patterns
4. Add proper error handling and TypeScript types
5. Keep changes minimal and focused
6. Include any necessary imports

Return only the file changes, nothing else.`

    const response = await callModel(prompt, 6000)
    const diffs = parseFileChanges(response)
    
    // Apply changes with safety checks
    const appliedDiffs = []
    for (const diff of diffs) {
      if (!allowWrite(diff.file)) {
        console.log(`⚠️  Skipping ${diff.file} (not in allowlist)`)
        continue
      }
      
      console.log(`✏️  Writing ${diff.file}`)
      await writeFile(diff.file, diff.content || '')
      appliedDiffs.push(diff)
    }
    
    console.log(`📝 Applied ${appliedDiffs.length} file changes`)
    
    return { 
      ...state, 
      diffs: appliedDiffs,
      iteration: (state.iteration || 1) + 1
    }
    
  } catch (error) {
    console.error('❌ Coder failed:', error)
    return { 
      ...state, 
      feedback: `Coding failed: ${error.message}`,
      done: true 
    }
  }
}

function parseFileChanges(response: string): Array<{file: string; content: string}> {
  const changes = []
  const sections = response.split('FILE:').slice(1)
  
  for (const section of sections) {
    const lines = section.trim().split('\n')
    const file = lines[0].trim()
    const contentStart = lines.findIndex(line => line.trim() === 'CONTENT:')
    
    if (contentStart >= 0) {
      const content = lines.slice(contentStart + 1).join('\n')
      changes.push({ file, content })
    }
  }
  
  return changes
}
