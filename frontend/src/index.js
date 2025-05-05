import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Register service worker for offline support
// Using try-catch to prevent errors breaking the app
try {
  serviceWorkerRegistration.register({
    onSuccess: () => console.log('Service Worker registered successfully'),
    onUpdate: () => console.log('Service Worker update available'),
    onError: (error) => console.error('Service Worker registration failed:', error)
  });
} catch (error) {
  console.error('Failed to register service worker:', error);
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
