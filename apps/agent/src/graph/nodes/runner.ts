import { execa } from 'execa'
import { AgentState } from '../index.js'

export const runnerNode = async (state: AgentState): Promise<Partial<AgentState>> => {
  console.log('🏃 RUNNER: Testing changes...')
  
  let runReport = ''
  
  try {
    // Test frontend if changes were made
    const frontendChanged = state.diffs?.some(d => d.file.startsWith('frontend/'))
    if (frontendChanged) {
      console.log('🧪 Testing frontend...')
      try {
        const result = await execa('npm', ['test', '--', '--watchAll=false', '--passWithNoTests'], {
          cwd: 'frontend',
          env: { CI: 'true' },
          timeout: 60000
        })
        runReport += `✅ Frontend tests passed\n${result.stdout}\n\n`
      } catch (error) {
        runReport += `❌ Frontend tests failed\n${error.stdout || error.message}\n\n`
      }
    }
    
    // Test backend if changes were made  
    const backendChanged = state.diffs?.some(d => d.file.startsWith('backend/'))
    if (backendChanged) {
      console.log('🧪 Testing backend...')
      try {
        const result = await execa('python', ['-m', 'pytest', '-v', '--tb=short'], {
          cwd: 'backend',
          timeout: 60000
        })
        runReport += `✅ Backend tests passed\n${result.stdout}\n\n`
      } catch (error) {
        runReport += `❌ Backend tests failed\n${error.stdout || error.message}\n\n`
      }
    }
    
    // Basic syntax check
    if (!frontendChanged && !backendChanged) {
      runReport += '✅ No tests needed - changes are documentation or config only\n'
    }
    
  } catch (error) {
    runReport += `❌ Test runner error: ${error.message}\n`
  }
  
  console.log('📊 Test results:', runReport.slice(0, 200) + '...')
  
  return { 
    ...state, 
    runReport 
  }
}
