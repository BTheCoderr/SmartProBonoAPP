/**
 * Combined script to run all ESLint and React code quality fixes
 * 
 * This script combines multiple automation scripts to fix common issues:
 * - Fix ESLint issues (fix-eslint-issues.js)
 * - Fix React Hooks dependency warnings (fix-hooks-deps.js)
 * - Remove unused variables and imports (fix-unused-vars.js)
 * - Add PropTypes to React components (add-prop-types.js)
 *
 * Run with: node scripts/auto-fix-all.js [path]
 * Example for a single file: node scripts/auto-fix-all.js src/components/MyComponent.js
 * Example for a directory: node scripts/auto-fix-all.js src/components
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Default directories to process if no argument is provided
const DEFAULT_DIRS = [
  'src/components',
  'src/pages',
  'src/contexts',
  'src/utils'
];

// Function to fix ESLint issues in a file
const fixEslintIssues = (filePath) => {
  try {
    console.log(`Running ESLint fix on ${filePath}...`);
    execSync(`npx eslint --fix ${filePath}`, { stdio: 'inherit' });
    return true;
  } catch (error) {
    console.error(`Error fixing ESLint issues in ${filePath}`);
    return false;
  }
};

// Function to fix React Hooks dependency warnings
const fixHooksDependencies = (filePath) => {
  try {
    console.log(`Running Hooks dependency fixes on ${filePath}...`);
    execSync(`node scripts/fix-hooks-deps.js ${filePath}`, { stdio: 'inherit' });
    return true;
  } catch (error) {
    console.error(`Error fixing Hooks dependencies in ${filePath}`);
    return false;
  }
};

// Function to remove unused variables and imports
const fixUnusedVars = (filePath) => {
  try {
    console.log(`Removing unused variables in ${filePath}...`);
    execSync(`node scripts/fix-unused-vars.js ${filePath}`, { stdio: 'inherit' });
    return true;
  } catch (error) {
    console.error(`Error removing unused variables in ${filePath}`);
    return false;
  }
};

// Function to add PropTypes to a React component
const addPropTypes = (filePath) => {
  // Only run on React components (conventionally named with PascalCase)
  const fileName = path.basename(filePath);
  const isPascalCase = fileName.charAt(0) === fileName.charAt(0).toUpperCase();
  
  if (!isPascalCase) return false;
  
  try {
    console.log(`Adding PropTypes to ${filePath}...`);
    execSync(`node scripts/add-prop-types.js ${filePath}`, { stdio: 'inherit' });
    return true;
  } catch (error) {
    console.error(`Error adding PropTypes to ${filePath}`);
    return false;
  }
};

// Function to process a single file
const processFile = (filePath) => {
  console.log(`\nProcessing file: ${filePath}`);
  
  if (filePath.endsWith('.js') || filePath.endsWith('.jsx')) {
    fixEslintIssues(filePath);
    fixHooksDependencies(filePath);
    fixUnusedVars(filePath);
    addPropTypes(filePath);
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
  
  if (targetPath) {
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
  } else {
    console.log('No target path provided, processing default directories');
    
    DEFAULT_DIRS.forEach(dirPath => {
      const fullPath = path.join(process.cwd(), dirPath);
      if (fs.existsSync(fullPath)) {
        processDirectory(fullPath);
      } else {
        console.warn(`Directory not found: ${fullPath}`);
      }
    });
  }
  
  console.log('\nCode quality fixes completed');
};

main(); 