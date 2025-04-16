/**
 * Script to fix unused variables warnings
 * 
 * This script identifies and removes unused imports and variables
 * based on ESLint warnings.
 *
 * Run with: node scripts/fix-unused-vars.js [file-path]
 * Example: node scripts/fix-unused-vars.js src/components/MyComponent.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Function to run ESLint on a file and extract unused variable warnings
const getUnusedVarWarnings = (filePath) => {
  try {
    // Run ESLint and capture the output
    const eslintOutput = execSync(`npx eslint ${filePath} --format json`).toString();
    const eslintResults = JSON.parse(eslintOutput);
    
    if (!eslintResults || !eslintResults.length || !eslintResults[0].messages) {
      return [];
    }
    
    // Filter for no-unused-vars rule warnings
    const unusedVarWarnings = eslintResults[0].messages.filter(msg => 
      msg.ruleId === 'no-unused-vars'
    );
    
    return unusedVarWarnings.map(warning => {
      return {
        line: warning.line,
        column: warning.column,
        endLine: warning.endLine,
        endColumn: warning.endColumn,
        message: warning.message,
        varName: warning.message.match(/'([^']+)'/)?.[1] || ''
      };
    });
  } catch (error) {
    console.error(`❌ Error getting unused variable warnings: ${error.message}`);
    return [];
  }
};

// Function to remove unused imports
const removeUnusedImports = (fileContent, warnings) => {
  let lines = fileContent.split('\n');
  const importLines = [];
  
  // Find all import lines and their line numbers
  lines.forEach((line, index) => {
    if (line.trim().startsWith('import ')) {
      importLines.push({ lineNumber: index, content: line });
    }
  });
  
  // Process each warning for unused imports
  for (const warning of warnings) {
    const { varName, line } = warning;
    
    if (!varName) continue;
    
    // Check if the warning is about an import
    const importLine = importLines.find(imp => imp.lineNumber === line - 1);
    if (!importLine) continue;
    
    const importContent = importLine.content;
    
    // Handle different import formats
    if (importContent.includes('{ ') && importContent.includes(' }')) {
      // Named imports like: import { Component1, Component2 } from 'module';
      let namedImports = importContent.match(/\{\s*(.*?)\s*\}/)[1].split(',').map(i => i.trim());
      
      // Remove the unused variable
      namedImports = namedImports.filter(imp => imp !== varName);
      
      if (namedImports.length === 0) {
        // Remove the entire import if no named imports remain
        lines[importLine.lineNumber] = '';
      } else {
        // Update the import with remaining named imports
        const newImport = importContent.replace(/\{\s*(.*?)\s*\}/, `{ ${namedImports.join(', ')} }`);
        lines[importLine.lineNumber] = newImport;
      }
    } else if (importContent.match(new RegExp(`import\\s+${varName}\\s+from`))) {
      // Default import: import Component from 'module';
      lines[importLine.lineNumber] = '';
    }
  }
  
  // Remove empty lines and return the updated content
  return lines.filter(line => line !== '').join('\n');
};

// Function to remove unused variables from the rest of the code
const removeUnusedVariables = (fileContent, warnings) => {
  // This is more complex and may require an AST parser for proper implementation
  // For now, we'll just log the unused variables that aren't imports
  const nonImportWarnings = warnings.filter(warning => {
    const line = fileContent.split('\n')[warning.line - 1];
    return !line.trim().startsWith('import ');
  });
  
  if (nonImportWarnings.length > 0) {
    console.log('\nDetected unused variables (non-imports):');
    nonImportWarnings.forEach(warning => {
      console.log(`- ${warning.varName} at line ${warning.line}`);
    });
    console.log('These require manual inspection as they cannot be safely removed automatically.\n');
  }
  
  return fileContent;
};

// Main function to fix unused variables in a file
const fixUnusedVars = (filePath) => {
  try {
    // Get unused variable warnings
    const warnings = getUnusedVarWarnings(filePath);
    
    if (warnings.length === 0) {
      console.log(`✅ No unused variable warnings in ${filePath}`);
      return;
    }
    
    console.log(`Found ${warnings.length} unused variable warnings in ${filePath}`);
    
    // Read the file content
    let fileContent = fs.readFileSync(filePath, 'utf8');
    
    // Fix unused imports
    fileContent = removeUnusedImports(fileContent, warnings);
    
    // Try to fix unused variables in the rest of the code
    fileContent = removeUnusedVariables(fileContent, warnings);
    
    // Write the updated content back to the file
    fs.writeFileSync(filePath, fileContent);
    
    console.log(`✅ Fixed unused variables in ${filePath}`);
  } catch (error) {
    console.error(`❌ Error fixing unused variables: ${error.message}`);
  }
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
  
  fixUnusedVars(filePath);
  console.log('Unused variables fixing completed');
};

main(); 