/**
 * Script to fix missing dependencies in useEffect hooks
 * 
 * This script identifies useEffect hooks that have ESLint warnings about
 * missing dependencies and suggests fixes by adding missing variables to 
 * the dependency array.
 *
 * Run with: node scripts/fix-hooks-deps.js [file-path]
 * Example: node scripts/fix-hooks-deps.js src/components/MyComponent.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Function to run ESLint on a file and extract dependency warnings
const getHooksDependencyWarnings = (filePath) => {
  try {
    // Run ESLint and capture the output
    const eslintOutput = execSync(`npx eslint ${filePath} --format json`).toString();
    const eslintResults = JSON.parse(eslintOutput);
    
    if (!eslintResults || !eslintResults.length || !eslintResults[0].messages) {
      return [];
    }
    
    // Filter for react-hooks/exhaustive-deps rule warnings
    const hooksWarnings = eslintResults[0].messages.filter(msg => 
      msg.ruleId === 'react-hooks/exhaustive-deps'
    );
    
    return hooksWarnings.map(warning => {
      // Extract the missing dependencies from the warning message
      const matches = warning.message.match(/(?:'([^']+)')/g);
      let missingDeps = [];
      
      if (matches) {
        missingDeps = matches.map(match => match.slice(1, -1));
      }
      
      return {
        line: warning.line,
        missingDeps,
        message: warning.message
      };
    });
  } catch (error) {
    console.error(`❌ Error getting hooks warnings: ${error.message}`);
    return [];
  }
};

// Function to fix missing dependencies in a file
const fixHooksDependencies = (filePath, warnings) => {
  if (!warnings.length) {
    console.log(`✅ No React Hooks dependency warnings in ${filePath}`);
    return;
  }
  
  console.log(`Found ${warnings.length} React Hooks dependency warnings in ${filePath}`);
  
  // Read the file content
  const fileContent = fs.readFileSync(filePath, 'utf8');
  const lines = fileContent.split('\n');
  
  // Process each warning from the bottom of the file to the top
  // (to avoid changing line numbers for subsequent fixes)
  const sortedWarnings = [...warnings].sort((a, b) => b.line - a.line);
  
  // For each warning, find the dependency array line and add missing dependencies
  for (const warning of sortedWarnings) {
    const lineIndex = warning.line - 1;
    
    // Search for the dependency array in the line and surrounding lines
    let depArrayLine = lines[lineIndex];
    let depArrayLineIndex = lineIndex;
    
    // If the line doesn't contain a dependency array, look a few lines down
    if (!depArrayLine.includes('}, [') && !depArrayLine.includes(']')) {
      for (let i = 1; i <= 5; i++) {
        if (lineIndex + i < lines.length) {
          if (lines[lineIndex + i].includes('}, [') || lines[lineIndex + i].includes(']')) {
            depArrayLine = lines[lineIndex + i];
            depArrayLineIndex = lineIndex + i;
            break;
          }
        }
      }
    }
    
    // Extract and modify the dependency array
    if (depArrayLine.includes('}, [') || depArrayLine.includes(']')) {
      const depArrayStart = depArrayLine.indexOf('[');
      const depArrayEnd = depArrayLine.indexOf(']', depArrayStart);
      
      if (depArrayStart !== -1 && depArrayEnd !== -1) {
        // Extract existing dependencies
        const existingDepsStr = depArrayLine.substring(depArrayStart + 1, depArrayEnd).trim();
        const existingDeps = existingDepsStr ? existingDepsStr.split(',').map(dep => dep.trim()) : [];
        
        // Add missing dependencies
        for (const missingDep of warning.missingDeps) {
          if (!existingDeps.includes(missingDep)) {
            existingDeps.push(missingDep);
          }
        }
        
        // Rebuild the dependency array line
        const newDepsStr = existingDeps.join(', ');
        const newDepArrayLine = depArrayLine.substring(0, depArrayStart + 1) + 
                                newDepsStr + 
                                depArrayLine.substring(depArrayEnd);
        
        lines[depArrayLineIndex] = newDepArrayLine;
        
        console.log(`✅ Added missing dependencies ${warning.missingDeps.join(', ')} at line ${depArrayLineIndex + 1}`);
      }
    }
  }
  
  // Write the updated content back to the file
  fs.writeFileSync(filePath, lines.join('\n'));
  console.log(`✅ Fixed React Hooks dependencies in ${filePath}`);
};

// Main function
const main = () => {
  const targetPath = process.argv[2];
  
  if (!targetPath) {
    console.error('Please provide a file path');
    process.exit(1);
  }
  
  const filePath = path.resolve(process.cwd(), targetPath);
  
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    process.exit(1);
  }
  
  const warnings = getHooksDependencyWarnings(filePath);
  fixHooksDependencies(filePath, warnings);
  
  console.log('React Hooks dependency fixing completed');
};

main(); 