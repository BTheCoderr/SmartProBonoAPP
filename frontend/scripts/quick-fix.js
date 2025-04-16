/**
 * Quick Fix script for critical ESLint issues
 * 
 * This script focuses only on fixing the most critical issues:
 * - React Hooks dependency warnings (exhaustive-deps)
 * - Unescaped entities in JSX
 *
 * Run with: node scripts/quick-fix.js [file-path]
 * Examples:
 * - For a single file: node scripts/quick-fix.js src/components/MyComponent.js
 * - For a directory: node scripts/quick-fix.js src/components
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Function to fix React Hooks dependency warnings in a file
const fixHooksDependencies = (filePath) => {
  try {
    console.log(`\nFixing React Hooks dependencies in ${filePath}`);
    execSync(`node scripts/fix-hooks-deps.js ${filePath}`, { stdio: 'pipe' });
    return true;
  } catch (error) {
    console.error(`Error fixing React Hooks dependencies in ${filePath}`);
    return false;
  }
};

// Function to fix unescaped entities (like apostrophes) in JSX
const fixUnescapedEntities = (filePath) => {
  try {
    console.log(`Fixing unescaped entities in ${filePath}`);
    
    // Read file content
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Replace common unescaped entities
    const fixed = content
      // Fix apostrophes in JSX (but not in regular strings or comments)
      .replace(/(\{.*?\}|<[^>]*>)([^<{]*?)'/g, (match, jsx, text) => {
        return jsx + text.replace(/'/g, '&apos;');
      });
    
    // Only write if changes were made
    if (content !== fixed) {
      fs.writeFileSync(filePath, fixed);
      console.log(`✅ Fixed unescaped entities in ${filePath}`);
    } else {
      console.log(`No unescaped entities found in ${filePath}`);
    }
    
    return true;
  } catch (error) {
    console.error(`Error fixing unescaped entities in ${filePath}: ${error.message}`);
    return false;
  }
};

// Function to process a single file
const processFile = (filePath) => {
  if (filePath.endsWith('.js') || filePath.endsWith('.jsx')) {
    fixHooksDependencies(filePath);
    fixUnescapedEntities(filePath);
  } else {
    console.warn(`Skipping non-JavaScript file: ${filePath}`);
  }
};

// Function to recursively process a directory
const processDirectory = (dirPath) => {
  console.log(`\nProcessing directory: ${dirPath}`);
  
  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      
      if (entry.isDirectory()) {
        processDirectory(fullPath);
      } else if (entry.isFile() && (entry.name.endsWith('.js') || entry.name.endsWith('.jsx'))) {
        processFile(fullPath);
      }
    }
  } catch (error) {
    console.error(`Error processing directory ${dirPath}: ${error.message}`);
  }
};

// Main function
const main = () => {
  const targetPath = process.argv[2];
  
  if (!targetPath) {
    console.error('Please provide a file or directory path');
    process.exit(1);
  }
  
  const fullPath = path.resolve(process.cwd(), targetPath);
  
  if (!fs.existsSync(fullPath)) {
    console.error(`Path does not exist: ${fullPath}`);
    process.exit(1);
  }
  
  if (fs.statSync(fullPath).isDirectory()) {
    processDirectory(fullPath);
  } else {
    processFile(fullPath);
  }
  
  console.log('\nQuick fixes completed');
};

main(); 