import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Simple test component
const TestComponent = () => {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Test Component</h1>
      <p>This is a simple test component to verify React is working.</p>
    </div>
  );
};

// AI Virtual Paralegal component
const AIVirtualParalegal = () => {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>AI Virtual Paralegal</h1>
      <p>This is the AI Virtual Paralegal page. The route is working!</p>
      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f0f0f0', borderRadius: '5px' }}>
        <h3>Features:</h3>
        <ul>
          <li>Autonomous workflow management</li>
          <li>Client case processing</li>
          <li>Document generation</li>
          <li>Task scheduling</li>
          <li>Deadline monitoring</li>
        </ul>
      </div>
    </div>
  );
};

function SimpleApp() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<TestComponent />} />
        <Route path="/ai-virtual-paralegal" element={<AIVirtualParalegal />} />
        <Route path="/test" element={<TestComponent />} />
      </Routes>
    </Router>
  );
}

export default SimpleApp;
