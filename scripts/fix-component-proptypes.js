#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Define component-specific PropTypes mappings
const componentPropTypes = {
  'AIResponseMetadata': {
    confidenceScore: { type: 'number', isRequired: true, description: 'Confidence score percentage (0-100) indicating the AI\'s confidence in the response' },
    citations: { 
      type: 'arrayOf(PropTypes.shape({text: PropTypes.string.isRequired, url: PropTypes.string, type: PropTypes.string.isRequired, year: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired}))', 
      isRequired: false, 
      description: 'Array of citation objects with source information' 
    },
    reasoningDetails: { type: 'string', isRequired: false, description: 'Detailed explanation of the AI\'s reasoning process' },
    jurisdictions: { type: 'arrayOf(PropTypes.string)', isRequired: false, description: 'Array of relevant legal jurisdictions' },
    lastUpdated: { type: 'string', isRequired: false, description: 'ISO date string of when the information was last updated' }
  },
  'ErrorBoundary': {
    children: { type: 'node', isRequired: true, description: 'React children to be rendered within the error boundary' }
  },
  'ChatRoom': {
    roomId: { type: 'string.isRequired', isRequired: true, description: 'Unique identifier for the chat room' },
    userId: { type: 'string.isRequired', isRequired: true, description: 'Current user identifier' },
    userName: { type: 'string', isRequired: false, description: 'Display name of the current user' }
  },
  'WebSocketTestComponent': {
    url: { type: 'string', isRequired: false, description: 'WebSocket server URL to connect to' },
    autoConnect: { type: 'bool', isRequired: false, description: 'Whether to connect automatically on component mount' }
  },
  'LegalAIChat': {
    userId: { type: 'string', isRequired: true, description: 'Current user identifier' },
    caseId: { type: 'string', isRequired: false, description: 'Case identifier if the chat is associated with a case' },
    initialPrompt: { type: 'string', isRequired: false, description: 'Initial message to send to the AI' }
  }
};

// Check if component names are provided as arguments
const componentNames = process.argv.slice(2);
if (componentNames.length === 0) {
  console.log('Usage: node fix-component-proptypes.js [componentName1] [componentName2] ...');
  console.log('If no component names are provided, all components will be processed.');
}

// Function to process a component file
function processComponentFile(filePath) {
  try {
    const componentName = path.basename(filePath, path.extname(filePath));
    
    // Skip if specific components were requested and this isn't one of them
    if (componentNames.length > 0 && !componentNames.includes(componentName)) {
      return;
    }
    
    console.log(`Processing ${componentName}...`);
    
    // Read file content
    const code = fs.readFileSync(filePath, 'utf8');
    
    // Skip if file doesn't contain React or PropTypes
    if (!code.includes('import React') || !code.includes('PropTypes')) {
      console.log(`Skipping ${componentName}: Not a React component or missing PropTypes import`);
      return;
    }
    
    let updatedCode;
    
    // If we have predefined PropTypes for this component, use them
    if (componentPropTypes[componentName]) {
      updatedCode = updateSpecificPropTypes(code, componentName, componentPropTypes[componentName]);
    } else {
      // Otherwise, try to improve the existing PropTypes
      updatedCode = improveGenericPropTypes(code, componentName);
    }
    
    // Write the updated code back to the file
    fs.writeFileSync(filePath, updatedCode);
    console.log(`Updated PropTypes for ${componentName} successfully!`);
  } catch (error) {
    console.error(`Error processing ${filePath}: ${error.message}`);
  }
}

// Update PropTypes for a component using predefined mappings
function updateSpecificPropTypes(code, componentName, propTypesMap) {
  // Find the PropTypes section
  const propTypesRegex = new RegExp(`${componentName}\\.propTypes\\s*=\\s*{[\\s\\S]*?};`);
  
  // Create the new PropTypes object
  let propTypesStr = `${componentName}.propTypes = {\n`;
  
  // Add each prop type definition
  Object.entries(propTypesMap).forEach(([propName, propInfo]) => {
    propTypesStr += `  /** ${propInfo.description} */\n`;
    propTypesStr += `  ${propName}: PropTypes.${propInfo.type}`;
    if (propInfo.isRequired) {
      // Only add .isRequired if not already in the type
      if (!propInfo.type.includes('.isRequired')) {
        propTypesStr += '.isRequired';
      }
    }
    propTypesStr += ',\n';
  });
  
  propTypesStr += '};';
  
  // If PropTypes section exists, replace it
  if (code.match(propTypesRegex)) {
    return code.replace(propTypesRegex, propTypesStr);
  } else {
    // Otherwise, add it before the export
    const exportRegex = /export\s+default\s+/;
    const exportMatch = code.match(exportRegex);
    
    if (exportMatch) {
      const position = exportMatch.index;
      return code.slice(0, position) + '\n' + propTypesStr + '\n\n' + code.slice(position);
    } else {
      // If no export is found, append to the end
      return code + '\n\n' + propTypesStr + '\n';
    }
  }
}

// Improve existing PropTypes by replacing 'any' with better types
function improveGenericPropTypes(code, componentName) {
  // Find the PropTypes section
  const propTypesRegex = new RegExp(`${componentName}\\.propTypes\\s*=\\s*{([\\s\\S]*?)};`);
  const propTypesMatch = code.match(propTypesRegex);
  
  if (!propTypesMatch) {
    console.log(`No PropTypes found for ${componentName}`);
    return code;
  }
  
  // Find all "PropTypes.any" and replace with better types where possible
  let propTypesContent = propTypesMatch[1];
  
  // Replace common any types with better types based on prop names
  propTypesContent = propTypesContent.replace(/(\w+):\s*PropTypes\.any/g, (match, propName) => {
    // Determine better type based on prop name
    if (propName.toLowerCase().includes('id')) {
      return `${propName}: PropTypes.string`;
    } else if (propName.toLowerCase().includes('count') || propName.toLowerCase().includes('index') || 
               propName.toLowerCase().includes('score')) {
      return `${propName}: PropTypes.number`;
    } else if (propName.toLowerCase().includes('is') || propName.toLowerCase().includes('has') || 
               propName.toLowerCase().includes('can') || propName.toLowerCase().includes('should')) {
      return `${propName}: PropTypes.bool`;
    } else if (propName.toLowerCase().includes('items') || propName.toLowerCase().includes('list') || 
               propName.toLowerCase().includes('array')) {
      return `${propName}: PropTypes.array`;
    } else if (propName.toLowerCase().includes('on') && propName.length > 2) {
      return `${propName}: PropTypes.func`;
    } else if (propName.toLowerCase().includes('children')) {
      return `${propName}: PropTypes.node`;
    } else if (propName.toLowerCase().includes('style') || propName.toLowerCase().includes('options')) {
      return `${propName}: PropTypes.object`;
    } else {
      return match; // Keep as any if we can't infer a better type
    }
  });
  
  // Add comments if missing
  propTypesContent = propTypesContent.replace(/(\n\s+)(\w+):\s*PropTypes/g, (match, space, propName) => {
    // If there's no comment before this line, add one
    if (!match.includes('/**')) {
      return `${space}/** ${propName} property */\n${space}${propName}: PropTypes`;
    }
    return match;
  });
  
  // Reconstruct the PropTypes section
  const updatedPropTypes = `${componentName}.propTypes = {${propTypesContent}};`;
  
  // Replace in the original code
  return code.replace(propTypesRegex, updatedPropTypes);
}

// Find all React component files in the src directory
const componentFiles = glob.sync('frontend/src/components/**/*.{js,jsx}');

// Process each file
if (componentNames.length > 0) {
  console.log(`Processing specified components: ${componentNames.join(', ')}`);
  componentFiles.forEach(processComponentFile);
} else {
  console.log(`Processing all components in frontend/src/components/`);
  componentFiles.forEach(processComponentFile);
} 