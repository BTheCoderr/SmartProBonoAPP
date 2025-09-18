import fs from 'fs/promises'
import path from 'path'
import { glob } from 'glob'

export async function repoMap(root = process.cwd()): Promise<string> {
  const targets = [
    'README.md',
    'frontend/package.json',
    'frontend/src/routes.js',
    'frontend/src/components/**/*.js',
    'frontend/src/pages/**/*.js',
    'backend/app.py',
    'backend/combined_server.py',
    'backend/routes/**/*.py',
    'backend/services/**/*.py',
    'backend/models/**/*.py'
  ]
  
  const chunks: string[] = []
  
  for (const pattern of targets) {
    try {
      const files = await glob(pattern, { cwd: root, ignore: ['**/node_modules/**', '**/__pycache__/**'] })
      
      for (const file of files.slice(0, 10)) { // Limit to prevent huge context
        const fullPath = path.join(root, file)
        try {
          const stat = await fs.stat(fullPath)
          if (stat.size > 50000) continue // Skip large files
          
          const content = await fs.readFile(fullPath, 'utf8')
          chunks.push(`FILE: ${file}
${content.slice(0, 3000)}${content.length > 3000 ? '\n... (truncated)' : ''}`)
        } catch (e) {
          // Skip files we can't read
        }
      }
    } catch (e) {
      // Skip patterns that don't match
    }
  }
  
  return chunks.join('\n\n---\n\n')
}

export async function readFile(filePath: string): Promise<string> {
  try {
    return await fs.readFile(filePath, 'utf8')
  } catch (error) {
    throw new Error(`Failed to read ${filePath}: ${error.message}`)
  }
}

export async function writeFile(filePath: string, content: string): Promise<void> {
  try {
    // Ensure directory exists
    await fs.mkdir(path.dirname(filePath), { recursive: true })
    await fs.writeFile(filePath, content, 'utf8')
  } catch (error) {
    throw new Error(`Failed to write ${filePath}: ${error.message}`)
  }
}

export async function fileExists(filePath: string): Promise<boolean> {
  try {
    await fs.access(filePath)
    return true
  } catch {
    return false
  }
}
