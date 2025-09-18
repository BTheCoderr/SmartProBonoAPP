#!/usr/bin/env ts-node
import 'dotenv/config'
import { buildGraph } from '../graph/index.js'
import { createBranch, commitChanges } from '../tools/git.js'

async function main() {
  const goal = process.argv.slice(2).join(' ') || 'Add a /health endpoint to the backend with tests'
  
  console.log('🚀 SmartProBono AI Development Agent Starting...')
  console.log(`🎯 Goal: ${goal}`)
  console.log('=' .repeat(60))
  
  const startTime = Date.now()
  
  try {
    // Create a new branch for this work
    const branchName = await createBranch()
    console.log(`🌿 Created branch: ${branchName}`)
    
    // Run the agent graph
    const graph = buildGraph()
    const finalState = await graph.invoke({ goal })
    
    console.log('=' .repeat(60))
    console.log('🏁 FINAL RESULT:')
    console.log(`✅ Done: ${finalState.done}`)
    console.log(`📝 Files changed: ${finalState.diffs?.length || 0}`)
    console.log(`🔄 Iterations: ${finalState.iteration || 0}`)
    console.log(`💬 Final feedback: ${finalState.feedback}`)
    
    if (finalState.diffs && finalState.diffs.length > 0) {
      // Commit the changes
      const commitMsg = `AI: ${goal}\n\nFiles modified: ${finalState.diffs.map(d => d.file).join(', ')}`
      await commitChanges(commitMsg)
      console.log('📦 Changes committed!')
      console.log('🔄 Run `git push origin HEAD` to create PR')
    } else {
      console.log('📝 No changes were made')
    }
    
  } catch (error) {
    console.error('💥 Agent failed:', error)
    process.exit(1)
  }
  
  const duration = (Date.now() - startTime) / 1000
  console.log(`⏱️  Total time: ${duration}s`)
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error)
}
