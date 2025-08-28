# SmartProBono Linting Guide

## Current Linting Setup

The SmartProBono codebase uses ESLint for detecting potential issues in the JavaScript code. We've configured linting with the following rules:

- React app standard rules (`react-app`, `react-app/jest`)
- Custom rules to downgrade certain errors to warnings:
  - `no-unused-vars`: Warns about unused variables instead of throwing errors
  - `react-hooks/exhaustive-deps`: Warns about missing dependencies in hooks
  - `import/no-anonymous-default-export`: Warns about anonymous default exports

## Common Linting Issues and How to Fix Them

### 1. Unused Imports and Variables

**Problem:** The most common linting issues in the codebase are unused imports and variables. These can accumulate during development when components evolve but imports aren't cleaned up.

**Fix:**
- Remove unused imports at the top of the file
- Remove unused variable declarations
- If a variable might be used in the future, prefix it with an underscore: `const _unusedVar = ...`

Example:
```javascript
// BAD: Unused imports
import React, { useState, useEffect, useCallback } from 'react';
import { Box, Typography, Button } from '@mui/material';

// GOOD: Only imports what's used
import React, { useState } from 'react';
import { Box, Typography } from '@mui/material';
```

### 2. Missing Dependencies in useEffect and useCallback

**Problem:** React's hook dependency arrays should include all dependencies used in the hook function.

**Fix:**
- Add all variables used inside the hook to the dependency array
- If you intentionally want to exclude a dependency, use the `// eslint-disable-next-line react-hooks/exhaustive-deps` comment

Example:
```javascript
// BAD: Missing dependency
useEffect(() => {
  fetchData(userId);
}, []); // userId is missing in dependencies

// GOOD: All dependencies included
useEffect(() => {
  fetchData(userId);
}, [userId]);

// ACCEPTABLE: If intentional
// eslint-disable-next-line react-hooks/exhaustive-deps
useEffect(() => {
  fetchData(userId);
}, []); // Intentionally excluding userId
```

### 3. Anonymous Default Exports

**Problem:** Using anonymous functions as default exports makes debugging harder.

**Fix:**
- Name your functions before exporting them

Example:
```javascript
// BAD: Anonymous export
export default () => {
  return <div>Component</div>;
};

// GOOD: Named export
const MyComponent = () => {
  return <div>Component</div>;
};

export default MyComponent;
```

## Running Linting Checks

To check for linting issues:
```bash
cd frontend
npm run lint
```

To automatically fix some linting issues:
```bash
cd frontend
npm run lint:fix
```

## Maintenance Scripts

The repository includes several scripts to help manage linting issues:

1. `cleanup_unused_imports.js` - Identifies files with unused imports
2. `fix_frontend_linting.sh` - Automatically fixes common linting issues

## Best Practices for Clean Code

1. **Keep imports clean**: Remove unused imports when you're done with a component
2. **Name your functions and variables clearly**: Avoid anonymous functions for easier debugging
3. **Use consistent casing**: camelCase for variables/functions, PascalCase for components
4. **Document complex logic**: Add comments to explain non-obvious code
5. **Split large components**: If a component file exceeds 300 lines, consider splitting it
6. **Use TypeScript or PropTypes**: Define the expected types for component props

## Troubleshooting Common Issues

If you encounter the `arguments is not defined` error:
- Use named parameters instead of accessing the `arguments` object
- Pass parameters explicitly between functions

For "hook missing dependency" warnings:
- Carefully evaluate if the dependency should be included
- If excluding is intentional, use the eslint-disable comment

## Resources

- [ESLint Documentation](https://eslint.org/docs/user-guide/getting-started)
- [React Hooks ESLint Plugin](https://www.npmjs.com/package/eslint-plugin-react-hooks)
- [Clean Code JavaScript](https://github.com/ryanmcdermott/clean-code-javascript) 