const allowedPaths = (process.env.ALLOWLIST_PATHS || '').split(',').map(s => s.trim()).filter(Boolean)

export function allowWrite(file: string): boolean {
  if (allowedPaths.length === 0) {
    console.warn('⚠️  No ALLOWLIST_PATHS configured - allowing all writes')
    return true
  }
  
  const allowed = allowedPaths.some(prefix => file.startsWith(prefix))
  
  if (!allowed) {
    console.log(`🚫 Blocked write to ${file} (not in allowlist: ${allowedPaths.join(', ')})`)
  }
  
  return allowed
}

export function checkCostLimit(currentCost: number): boolean {
  const limit = Number(process.env.AGENT_COST_LIMIT_USD || 10)
  if (currentCost > limit) {
    console.error(`💰 Cost limit exceeded: $${currentCost} > $${limit}`)
    return false
  }
  return true
}

export function checkTimeLimit(startTime: number): boolean {
  const limit = Number(process.env.AGENT_TIME_LIMIT_MIN || 30) * 60 * 1000
  const elapsed = Date.now() - startTime
  if (elapsed > limit) {
    console.error(`⏰ Time limit exceeded: ${elapsed/1000/60}min > ${limit/1000/60}min`)
    return false
  }
  return true
}
