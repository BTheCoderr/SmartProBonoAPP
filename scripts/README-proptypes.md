# PropTypes Fixing Scripts

This directory contains scripts to help improve React component PropTypes definitions.

## Available Scripts

### 1. `fix-component-proptypes.js`

This script automatically updates PropTypes for React components. It can fix PropTypes for specific components or all components in the project.

**Usage:**
```bash
# Fix specific components
node scripts/fix-component-proptypes.js ComponentName1 ComponentName2

# Fix all components
node scripts/fix-component-proptypes.js
```

**Features:**
- Automatically updates PropTypes with more specific types (string, number, bool, etc.) instead of `PropTypes.any`
- Adds descriptive JSDoc comments for each prop
- Adds `.isRequired` where appropriate
- Uses predefined PropTypes definitions for key components

### 2. `fix-ai-response-metadata-proptypes.js`

This script specifically fixes PropTypes for the AIResponseMetadata component.

**Usage:**
```bash
node scripts/fix-ai-response-metadata-proptypes.js
```

### 3. `fix-proptypes.js`

This script uses AST (Abstract Syntax Tree) to analyze a component and generate appropriate PropTypes.

**Usage:**
```bash
node scripts/fix-proptypes.js path/to/component.js
```

## Adding Support for New Components

To add predefined PropTypes for a new component, edit the `componentPropTypes` object in `fix-component-proptypes.js`:

```javascript
const componentPropTypes = {
  'NewComponent': {
    propName: { 
      type: 'string', 
      isRequired: true, 
      description: 'Description of the prop' 
    }
    // Add more props...
  }
};
```

## Common PropTypes Reference

| Prop Type | When to Use |
|-----------|-------------|
| `string` | For text values |
| `number` | For numeric values |
| `bool` | For boolean flags |
| `func` | For function callbacks (e.g., `onClick`) |
| `node` | For React nodes (components, elements, strings) |
| `element` | For React elements only |
| `array` | For array values |
| `object` | For object values |
| `arrayOf(PropTypes.type)` | For arrays of a specific type |
| `shape({key: PropTypes.type})` | For objects with a specific structure |
| `oneOf(['option1', 'option2'])` | For props with predefined values |
| `oneOfType([PropTypes.string, PropTypes.number])` | For props that can be multiple types |

## Best Practices

1. Always define PropTypes for components that accept props
2. Use the most specific PropType validator possible
3. Mark required props with `.isRequired`
4. Add JSDoc comments to describe each prop's purpose
5. Consider using TypeScript for even better type-checking 