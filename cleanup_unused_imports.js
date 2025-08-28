/**
 * Script to identify and list files with unused imports
 * Run with: node cleanup_unused_imports.js
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// Directories to scan
const dirsToScan = [
  'frontend/src/components',
  'frontend/src/pages',
  'frontend/src/services',
  'frontend/src/context'
];

// Function to get all JS files in directories
function getJSFiles(dirs) {
  let files = [];
  
  for (const dir of dirs) {
    try {
      const dirFiles = fs.readdirSync(dir)
        .filter(file => file.endsWith('.js') || file.endsWith('.jsx'))
        .map(file => path.join(dir, file));
      
      files = [...files, ...dirFiles];
    } catch (err) {
      console.error(`Error reading directory ${dir}:`, err.message);
    }
  }
  
  return files;
}

// Main function to run ESLint and collect results
async function findUnusedImports() {
  const files = getJSFiles(dirsToScan);
  console.log(`Found ${files.length} JavaScript files to check`);
  
  // Run ESLint with the no-unused-vars rule
  const command = `npx eslint ${files.join(' ')} --rule "no-unused-vars: error" --format json`;
  
  exec(command, (error, stdout) => {
    if (error && !stdout) {
      console.error('Error running ESLint:', error);
      return;
    }
    
    try {
      const results = JSON.parse(stdout);
      
      // Group issues by file
      const fileIssues = {};
      let totalUnusedImports = 0;
      
      results.forEach(result => {
        const filePath = result.filePath;
        const unusedImports = result.messages.filter(msg => 
          msg.ruleId === 'no-unused-vars' && 
          msg.message.includes('is defined but never used')
        );
        
        if (unusedImports.length > 0) {
          fileIssues[filePath] = unusedImports;
          totalUnusedImports += unusedImports.length;
        }
      });
      
      console.log(`\nFound ${totalUnusedImports} unused imports across ${Object.keys(fileIssues).length} files\n`);
      
      // Print report
      for (const [file, issues] of Object.entries(fileIssues)) {
        console.log(`\n${file.replace(process.cwd(), '')}:`);
        issues.forEach(issue => {
          console.log(`  Line ${issue.line}: ${issue.message}`);
        });
      }
      
      // Instructions for fixing
      console.log('\n\nTo fix these issues:');
      console.log('1. Open each file and remove the unused imports');
      console.log('2. Run the following command to automatically fix simple cases:');
      console.log('   npx eslint --fix frontend/src/');
      
    } catch (err) {
      console.error('Error parsing ESLint results:', err);
    }
  });
}

// Run the script
findUnusedImports(); 