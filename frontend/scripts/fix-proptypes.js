/**
 * Script to fix basic PropTypes validation warnings
 * 
 * This script adds simple PropTypes to React components based on
 * common prop naming conventions (e.g., 'children', 'onClick', etc.)
 *
 * Run with: node scripts/fix-proptypes.js [file-path]
 * Example: node scripts/fix-proptypes.js src/components/LoadingSpinner.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Common prop names and their PropTypes
const COMMON_PROPTYPES = {
  children: 'PropTypes.node',
  className: 'PropTypes.string',
  style: 'PropTypes.object',
  id: 'PropTypes.string',
  onClick: 'PropTypes.func',
  onChange: 'PropTypes.func',
  onSubmit: 'PropTypes.func',
  onBlur: 'PropTypes.func',
  onFocus: 'PropTypes.func',
  onKeyPress: 'PropTypes.func',
  onKeyDown: 'PropTypes.func',
  onKeyUp: 'PropTypes.func',
  onMouseEnter: 'PropTypes.func',
  onMouseLeave: 'PropTypes.func',
  disabled: 'PropTypes.bool',
  required: 'PropTypes.bool',
  value: 'PropTypes.any',
  defaultValue: 'PropTypes.any',
  placeholder: 'PropTypes.string',
  title: 'PropTypes.string',
  label: 'PropTypes.string',
  name: 'PropTypes.string',
  type: 'PropTypes.string',
  data: 'PropTypes.object',
  items: 'PropTypes.array',
  options: 'PropTypes.array',
  selected: 'PropTypes.bool',
  checked: 'PropTypes.bool',
  loading: 'PropTypes.bool',
  error: 'PropTypes.any',
  success: 'PropTypes.bool',
  message: 'PropTypes.string',
  isOpen: 'PropTypes.bool',
  onClose: 'PropTypes.func',
  onOpen: 'PropTypes.func',
  size: 'PropTypes.oneOf(["small", "medium", "large"])',
  variant: 'PropTypes.string',
  color: 'PropTypes.string',
  icon: 'PropTypes.node',
  src: 'PropTypes.string',
  alt: 'PropTypes.string',
};

// Function to get ESLint prop type validation warnings
const getPropTypeWarnings = (filePath) => {
  try {
    // Run ESLint and capture the output
    const result = execSync(`npx eslint ${filePath} --format json`, { stdio: 'pipe' }).toString();
    const eslintResults = JSON.parse(result);
    
    if (!eslintResults.length || !eslintResults[0].messages) {
      return [];
    }
    
    // Filter for prop validation warnings
    const warnings = eslintResults[0].messages.filter(
      msg => msg.ruleId === 'react/prop-types'
    );
    
    // Extract prop names from warnings
    const props = [];
    for (const warning of warnings) {
      const match = warning.message.match(/'([^']+)' is missing in props validation/);
      if (match && match[1]) {
        let propName = match[1];
        
        // Handle nested props like 'user.name'
        if (propName.includes('.')) {
          propName = propName.split('.')[0];
        }
        
        if (!props.includes(propName)) {
          props.push(propName);
        }
      }
    }
    
    return props;
  } catch (error) {
    console.error(`Error getting PropType warnings: ${error.message}`);
    return [];
  }
};

// Function to find component definitions in a file
const findComponents = (fileContent) => {
  const components = [];
  
  // Look for component definitions like:
  // const ComponentName = ({ prop1, prop2 }) => { ... }
  // OR
  // function ComponentName({ prop1, prop2 }) { ... }
  const componentRegex = /(?:const|function)\s+([A-Z][a-zA-Z0-9]*)\s*=?\s*\(\s*(?:\{\s*(.*?)\s*\}|\s*props\s*)\s*\)/gs;
  
  let match;
  while ((match = componentRegex.exec(fileContent)) !== null) {
    const componentName = match[1];
    const propsString = match[2] || '';
    
    // Extract props from destructuring
    const props = propsString
      .split(',')
      .map(prop => prop.trim().split('=')[0].trim())
      .filter(Boolean);
    
    components.push({ name: componentName, props });
  }
  
  return components;
};

// Function to add PropTypes to a component
const addPropTypes = (filePath) => {
  try {
    console.log(`Processing ${filePath}...`);
    
    // Read file content
    const fileContent = fs.readFileSync(filePath, 'utf8');
    
    // Get ESLint prop validation warnings
    const missingProps = getPropTypeWarnings(filePath);
    
    if (missingProps.length === 0) {
      console.log(`✅ No PropTypes warnings in ${filePath}`);
      return;
    }
    
    console.log(`Found ${missingProps.length} props without validation`);
    
    // Find component definitions
    const components = findComponents(fileContent);
    
    if (components.length === 0) {
      console.warn(`⚠️ Could not identify components in ${filePath}`);
      return;
    }
    
    // Check if PropTypes is already imported
    const hasImport = fileContent.includes("import PropTypes from 'prop-types'");
    
    let updatedContent = fileContent;
    
    // Add PropTypes import if needed
    if (!hasImport) {
      // Find the last import line
      const lastImportIndex = fileContent.lastIndexOf('import');
      if (lastImportIndex !== -1) {
        const endOfImports = fileContent.indexOf('\n', lastImportIndex);
        updatedContent = 
          fileContent.slice(0, endOfImports + 1) + 
          "import PropTypes from 'prop-types';\n" + 
          fileContent.slice(endOfImports + 1);
      }
    }
    
    // For each component, add PropTypes validation
    for (const component of components) {
      // Check if PropTypes are already defined
      const propTypesExist = updatedContent.includes(`${component.name}.propTypes`);
      
      if (propTypesExist) {
        console.log(`✅ PropTypes already defined for ${component.name}`);
        continue;
      }
      
      // Create PropTypes object
      let propTypesCode = `\n\n// Define PropTypes\n${component.name}.propTypes = {\n`;
      
      // Add common props
      for (const prop of [...component.props, ...missingProps]) {
        if (COMMON_PROPTYPES[prop]) {
          propTypesCode += `  ${prop}: ${COMMON_PROPTYPES[prop]},\n`;
        } else if (prop.startsWith('on')) {
          // Assume event handler
          propTypesCode += `  ${prop}: PropTypes.func,\n`;
        } else if (prop.includes('id')) {
          // Assume ID
          propTypesCode += `  ${prop}: PropTypes.string,\n`;
        } else if (prop.includes('is') || prop.includes('has')) {
          // Assume boolean
          propTypesCode += `  ${prop}: PropTypes.bool,\n`;
        } else {
          // Default to any
          propTypesCode += `  ${prop}: PropTypes.any, // TODO: Add proper validation\n`;
        }
      }
      
      propTypesCode += '};\n';
      
      // Add PropTypes before export statement
      const exportRegex = new RegExp(`export\\s+default\\s+${component.name}`);
      const exportMatch = exportRegex.exec(updatedContent);
      
      if (exportMatch) {
        const exportIndex = exportMatch.index;
        updatedContent = 
          updatedContent.slice(0, exportIndex) + 
          propTypesCode + 
          updatedContent.slice(exportIndex);
      } else {
        // If no export found, add at the end of the file
        updatedContent += propTypesCode;
      }
      
      console.log(`✅ Added PropTypes to ${component.name}`);
    }
    
    // Write updated content back to file
    fs.writeFileSync(filePath, updatedContent);
    console.log(`✅ Successfully updated ${filePath}`);
    
  } catch (error) {
    console.error(`Error adding PropTypes: ${error.message}`);
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
  
  addPropTypes(filePath);
};

main(); 