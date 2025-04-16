#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const generate = require('@babel/generator').default;
const t = require('@babel/types');

// Check if a file path was provided
if (process.argv.length < 3) {
  console.error('Please provide a file path to the component');
  process.exit(1);
}

const filePath = process.argv[2];

// Read the component file
try {
  const code = fs.readFileSync(filePath, 'utf8');
  processComponent(code, filePath);
} catch (error) {
  console.error(`Error reading file: ${error.message}`);
  process.exit(1);
}

function processComponent(code, filePath) {
  try {
    // Parse the code into an AST
    const ast = parser.parse(code, {
      sourceType: 'module',
      plugins: ['jsx', 'typescript', 'classProperties']
    });

    // Keep track of prop types to update
    let propsInfo = {};
    let componentName = path.basename(filePath, path.extname(filePath));
    let propTypesFound = false;

    // Analyze the component to identify props and types
    traverse(ast, {
      // Find functional component declarations
      FunctionDeclaration(path) {
        if (path.node.id) {
          const name = path.node.id.name;
          if (name === componentName || name.endsWith('Component')) {
            componentName = name;
            // Extract props from function params
            if (path.node.params.length > 0) {
              extractFunctionProps(path.node.params[0], propsInfo);
            }
          }
        }
      },
      // Find functional component expressions (const MyComponent = () => {})
      VariableDeclarator(path) {
        if (path.node.id && path.node.id.name && 
            (path.node.id.name === componentName || path.node.id.name.endsWith('Component'))) {
          componentName = path.node.id.name;
          
          // Arrow function or function expression
          if (t.isArrowFunctionExpression(path.node.init) || t.isFunctionExpression(path.node.init)) {
            if (path.node.init.params.length > 0) {
              extractFunctionProps(path.node.init.params[0], propsInfo);
            }
          }
        }
      },
      // Find class components
      ClassDeclaration(path) {
        if (path.node.id && path.node.id.name === componentName) {
          // For class components, we need to look at this.props usage
          componentName = path.node.id.name;
        }
      },
      // Find existing propTypes
      AssignmentExpression(path) {
        if (
          t.isMemberExpression(path.node.left) &&
          path.node.left.property.name === 'propTypes' &&
          path.node.left.object.name === componentName
        ) {
          propTypesFound = true;
          // Update the existing propTypes
          path.node.right = buildPropTypesObject(propsInfo);
        }
      },
      // Find prop usage in JSX
      JSXAttribute(path) {
        if (t.isJSXIdentifier(path.node.name)) {
          const propName = path.node.name.name;
          if (!propsInfo[propName]) {
            propsInfo[propName] = { type: 'any', isRequired: false };
          }
        }
      }
    });

    // If propTypes weren't found but we have props, add propTypes declaration
    if (!propTypesFound && Object.keys(propsInfo).length > 0) {
      traverse(ast, {
        Program: {
          exit(path) {
            const exportStatement = path.node.body.find(node => 
              t.isExportDefaultDeclaration(node) || 
              (t.isExportNamedDeclaration(node) && node.declaration && 
               node.declaration.id && node.declaration.id.name === componentName)
            );
            
            if (exportStatement) {
              const exportIndex = path.node.body.indexOf(exportStatement);
              
              // Create propTypes declaration
              const propTypesDeclaration = t.expressionStatement(
                t.assignmentExpression(
                  '=',
                  t.memberExpression(
                    t.identifier(componentName),
                    t.identifier('propTypes')
                  ),
                  buildPropTypesObject(propsInfo)
                )
              );
              
              // Insert propTypes before export
              path.node.body.splice(exportIndex, 0, propTypesDeclaration);
            }
          }
        }
      });
    }

    // Generate updated code
    const output = generate(ast, { retainLines: true }, code);
    
    // Write updated code back to file
    fs.writeFileSync(filePath, output.code);
    console.log(`PropTypes updated successfully for ${componentName} in ${filePath}`);
    
  } catch (error) {
    console.error(`Error processing component: ${error.message}`);
    console.error(error.stack);
    process.exit(1);
  }
}

// Extract props from function parameters (handles destructuring)
function extractFunctionProps(param, propsInfo) {
  if (t.isObjectPattern(param)) {
    // Handle destructured props ({ name, age, items = [] })
    param.properties.forEach(prop => {
      if (t.isObjectProperty(prop) || t.isRestElement(prop)) {
        const propName = prop.key.name;
        let type = 'any';
        let isRequired = !prop.value || !prop.value.right; // If it has a default value, it's not required
        
        // Infer type from default value if possible
        if (prop.value && prop.value.right) {
          type = inferTypeFromValue(prop.value.right);
        }
        
        propsInfo[propName] = { type, isRequired };
      }
    });
  } else if (t.isIdentifier(param)) {
    // Handle props as a single object (props)
    // In this case, we need to analyze usage in the function body
    // This is a simplified approach
    propsInfo['props'] = { type: 'object', isRequired: true };
  }
}

// Infer prop type from default value
function inferTypeFromValue(node) {
  if (t.isStringLiteral(node)) return 'string';
  if (t.isNumericLiteral(node)) return 'number';
  if (t.isBooleanLiteral(node)) return 'bool';
  if (t.isNullLiteral(node)) return 'any';
  if (t.isArrayExpression(node)) return 'array';
  if (t.isObjectExpression(node)) return 'object';
  if (t.isFunctionExpression(node) || t.isArrowFunctionExpression(node)) return 'func';
  return 'any';
}

// Build the PropTypes object expression
function buildPropTypesObject(propsInfo) {
  const properties = [];
  
  Object.entries(propsInfo).forEach(([propName, info]) => {
    // Create the PropTypes validation expression
    let propTypeExpr = t.memberExpression(
      t.identifier('PropTypes'),
      t.identifier(info.type)
    );
    
    // Add isRequired if needed
    if (info.isRequired) {
      propTypeExpr = t.memberExpression(propTypeExpr, t.identifier('isRequired'));
    }
    
    // Create the property with comment
    const property = t.objectProperty(
      t.identifier(propName),
      propTypeExpr
    );
    
    // Add description comment
    property.leadingComments = [
      {
        type: 'CommentBlock',
        value: ` ${propName}: ${info.type}${info.isRequired ? ' (required)' : ''} - Description of ${propName} `
      }
    ];
    
    properties.push(property);
  });
  
  return t.objectExpression(properties);
} 