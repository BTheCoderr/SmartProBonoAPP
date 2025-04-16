#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Path to the AIResponseMetadata component
const filePath = 'frontend/src/components/AIResponseMetadata.js';

// Read the component file
try {
  const code = fs.readFileSync(filePath, 'utf8');
  const updatedCode = updatePropTypes(code);
  fs.writeFileSync(filePath, updatedCode);
  console.log(`Updated PropTypes for AIResponseMetadata successfully!`);
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}

function updatePropTypes(code) {
  // Find the PropTypes section
  const propTypesRegex = /AIResponseMetadata\.propTypes\s*=\s*{[\s\S]*?};/;
  
  // Define the new PropTypes object with proper validations and descriptions
  const newPropTypes = `AIResponseMetadata.propTypes = {
  /** Confidence score percentage (0-100) indicating the AI's confidence in the response */
  confidenceScore: PropTypes.number.isRequired,
  /** Array of citation objects with source information */
  citations: PropTypes.arrayOf(
    PropTypes.shape({
      text: PropTypes.string.isRequired,
      url: PropTypes.string,
      type: PropTypes.string.isRequired,
      year: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired
    })
  ),
  /** Detailed explanation of the AI's reasoning process */
  reasoningDetails: PropTypes.string,
  /** Array of relevant legal jurisdictions */
  jurisdictions: PropTypes.arrayOf(PropTypes.string),
  /** ISO date string of when the information was last updated */
  lastUpdated: PropTypes.string,
};`;

  // Replace the old PropTypes section with the new one
  return code.replace(propTypesRegex, newPropTypes);
} 