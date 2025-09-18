import simpleGit from 'simple-git'

const git = simpleGit()

export async function createBranch(): Promise<string> {
  const prefix = process.env.BRANCH_PREFIX || 'ai/smartprobono'
  const timestamp = Date.now()
  const branchName = `${prefix}-${timestamp}`
  
  try {
    await git.checkoutLocalBranch(branchName)
    return branchName
  } catch (error) {
    throw new Error(`Failed to create branch ${branchName}: ${error.message}`)
  }
}

export async function commitChanges(message: string): Promise<void> {
  try {
    await git.add('.')
    await git.commit(message, {
      '--author': `${process.env.GIT_AUTHOR_NAME || 'SmartProBono-AI'} <${process.env.GIT_AUTHOR_EMAIL || 'ai@smartprobono.dev'}>`
    })
  } catch (error) {
    throw new Error(`Failed to commit changes: ${error.message}`)
  }
}

export async function getCurrentBranch(): Promise<string> {
  try {
    const status = await git.status()
    return status.current || 'main'
  } catch (error) {
    throw new Error(`Failed to get current branch: ${error.message}`)
  }
}

export async function switchToMain(): Promise<void> {
  try {
    await git.checkout('main')
  } catch (error) {
    throw new Error(`Failed to switch to main: ${error.message}`)
  }
}
