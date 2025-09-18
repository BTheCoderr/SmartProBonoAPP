import 'dotenv/config'
import { StateGraph, END } from '@langchain/langgraph'
import { plannerNode } from './nodes/planner.js'
import { coderNode } from './nodes/coder.js'
import { runnerNode } from './nodes/runner.js'
import { criticNode } from './nodes/critic.js'

export type AgentState = {
  goal: string
  plan?: string[]
  diffs?: Array<{file: string; patch: string; content?: string}>
  runReport?: string
  feedback?: string
  done?: boolean
  iteration?: number
  cost?: number
}

export function buildGraph() {
  const channels = {
    goal: null,
    plan: null, 
    diffs: null,
    runReport: null,
    feedback: null,
    done: null,
    iteration: null,
    cost: null
  }

  const graph = new StateGraph({ channels })
    .addNode('planner', plannerNode)
    .addNode('coder', coderNode)
    .addNode('runner', runnerNode)
    .addNode('critic', criticNode)
    .addEdge('planner', 'coder')
    .addEdge('coder', 'runner')
    .addEdge('runner', 'critic')
    .addConditionalEdges('critic', (state: AgentState) => {
      // Stop if done or max iterations reached
      if (state.done || (state.iteration && state.iteration >= 5)) {
        return END
      }
      return 'coder'
    })
    .setEntryPoint('planner')
    
  return graph.compile()
}
