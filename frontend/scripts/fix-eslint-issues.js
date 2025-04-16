/**
 * Script to automatically fix common ESLint issues across the codebase
 * 
 * Run with: node scripts/fix-eslint-issues.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Define directories to process
const dirs = [
  'src/components',
  'src/pages',
  'src/contexts',
  'src/utils'
];

// Function to fix ESLint issues in files
const fixEslintIssues = (filePath) => {
  try {
    // Run ESLint fix command
    execSync(`npx eslint --fix ${filePath}`);
    console.log(`✅ Fixed ESLint issues in ${filePath}`);
  } catch (error) {
    console.error(`❌ Error fixing ESLint issues in ${filePath}: ${error.message}`);
  }
};

// Function to recursively process directory
const processDirectory = (dir) => {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stats = fs.statSync(filePath);
    
    if (stats.isDirectory()) {
      processDirectory(filePath);
    } else if (file.endsWith('.js') || file.endsWith('.jsx')) {
      fixEslintIssues(filePath);
    }
  });
};

// Main function
const main = () => {
  console.log('Starting ESLint auto-fix script...');
  
  dirs.forEach(dir => {
    const dirPath = path.join(process.cwd(), dir);
    if (fs.existsSync(dirPath)) {
      console.log(`Processing directory: ${dir}`);
      processDirectory(dirPath);
    } else {
      console.warn(`⚠️ Directory not found: ${dirPath}`);
    }
  });
  
  console.log('ESLint auto-fix script completed');
};

main(); 