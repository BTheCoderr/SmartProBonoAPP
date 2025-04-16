/**
 * Script to scaffold PropTypes for React components
 * 
 * Run with: node scripts/add-prop-types.js [component-path]
 * Example: node scripts/add-prop-types.js src/components/LegalAIChat.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PROP_TYPES_IMPORT = "import PropTypes from 'prop-types';";

// Function to parse the component's props from the component definition
const parseComponentProps = (code) => {
  // Find component definition using regex
  const componentDefRegex = /(?:function|const)\s+(\w+)\s*=\s*\((?:{([^}]*)})?\)/;
  const match = code.match(componentDefRegex);
  
  if (!match) return { componentName: null, props: [] };
  
  const componentName = match[1];
  const propsStr = match[2] || '';
  
  // Extract props from destructured object
  const props = propsStr
    .split(',')
    .map(prop => prop.trim())
    .filter(Boolean)
    .map(prop => {
      // Handle default values and type annotations
      const [propName] = prop.split('=');
      return propName.trim();
    });
  
  return { componentName, props };
};

// Function to generate PropTypes based on props
const generatePropTypes = (componentName, props) => {
  if (!props.length) return '';
  
  let propTypesCode = `\n// Define PropTypes\n${componentName}.propTypes = {\n`;
  
  props.forEach(prop => {
    propTypesCode += `  /** TODO: Add description */\n  ${prop}: PropTypes.any,\n`;
  });
  
  propTypesCode += '};\n';
  
  return propTypesCode;
};

// Function to add PropTypes to a component file
const addPropTypes = (filePath) => {
  try {
    console.log(`Processing file: ${filePath}`);
    
    // Read file content
    const code = fs.readFileSync(filePath, 'utf8');
    
    // Check if PropTypes is already imported
    const hasPropTypesImport = code.includes(PROP_TYPES_IMPORT) || code.includes("from 'prop-types'");
    
    // Parse component props
    const { componentName, props } = parseComponentProps(code);
    
    if (!componentName) {
      console.warn(`⚠️ Could not identify component in ${filePath}`);
      return;
    }
    
    // Check if PropTypes are already defined
    const hasPropTypesDef = code.includes(`${componentName}.propTypes`);
    
    if (hasPropTypesDef) {
      console.log(`✅ PropTypes already defined for ${componentName}`);
      return;
    }
    
    // Generate PropTypes code
    const propTypesCode = generatePropTypes(componentName, props);
    
    // Add import if needed
    let updatedCode = code;
    if (!hasPropTypesImport && props.length > 0) {
      // Find the last import statement
      const lastImportIndex = code.lastIndexOf('import');
      const lastImportEndIndex = code.indexOf('\n', lastImportIndex);
      
      if (lastImportIndex !== -1) {
        updatedCode = 
          code.slice(0, lastImportEndIndex + 1) + 
          PROP_TYPES_IMPORT + '\n' + 
          code.slice(lastImportEndIndex + 1);
      }
    }
    
    // Add PropTypes definition before the export statement
    if (props.length > 0) {
      const exportIndex = updatedCode.lastIndexOf('export default');
      if (exportIndex !== -1) {
        updatedCode = 
          updatedCode.slice(0, exportIndex) + 
          propTypesCode + '\n' + 
          updatedCode.slice(exportIndex);
      }
    }
    
    // Write updated code back to file
    fs.writeFileSync(filePath, updatedCode);
    console.log(`✅ Added PropTypes to ${componentName} in ${filePath}`);
    
  } catch (error) {
    console.error(`❌ Error adding PropTypes to ${filePath}: ${error.message}`);
  }
};

// Main function
const main = () => {
  const targetPath = process.argv[2];
  
  if (!targetPath) {
    console.error('Please provide a component file path');
    process.exit(1);
  }
  
  const filePath = path.resolve(process.cwd(), targetPath);
  
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    process.exit(1);
  }
  
  addPropTypes(filePath);
  console.log('PropTypes scaffolding completed');
};

main(); 