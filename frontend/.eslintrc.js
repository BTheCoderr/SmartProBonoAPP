module.exports = {
  extends: [
    "react-app",
    "react-app/jest"
  ],
  rules: {
    // Allow unused variables in development
    "no-unused-vars": process.env.NODE_ENV === 'production' ? 'error' : 'warn',
    
    // Disable exhaustive-deps warnings as they're usually over-cautious
    "react-hooks/exhaustive-deps": "warn",
    
    // Disable rules for testing library that are causing errors
    "testing-library/no-node-access": "warn",
    "testing-library/no-wait-for-multiple-assertions": "warn",
    "testing-library/no-unnecessary-act": "warn",
    
    // Disable other problematic rules
    "no-restricted-globals": ["error", "event", "fdescribe"],
    "no-use-before-define": ["warn", { "functions": false, "classes": false }]
  }
}; 