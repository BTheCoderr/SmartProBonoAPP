import React from 'react';
import ReactDOM from 'react-dom/client';

function MinimalApp() {
  return (
    <div>
      <h1>Minimal App</h1>
      <p>This is a minimal React app to test if React is working.</p>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<MinimalApp />);
