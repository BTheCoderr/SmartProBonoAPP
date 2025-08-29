import React, { useState } from 'react';
import { langGraphAPI } from '../api/langgraph';

const LangGraphIntake = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [healthStatus, setHealthStatus] = useState(null);

  const checkHealth = async () => {
    try {
      const isHealthy = await langGraphAPI.healthCheck();
      setHealthStatus(isHealthy ? '✅ Healthy' : '❌ Unhealthy');
    } catch (err) {
      setHealthStatus('❌ Error');
      console.error('Health check failed:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await langGraphAPI.runIntake({
        user_id: null,
        full_text: text,
        meta: { source: 'react-frontend' }
      });
      setResult(response.result);
    } catch (err) {
      setError(err.message || 'Failed to process intake');
      console.error('Intake failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">
        🧠 LangGraph Case Intake
      </h2>
      
      {/* Health Check */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center gap-4">
          <button
            onClick={checkHealth}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Check LangGraph Health
          </button>
          {healthStatus && (
            <span className="text-sm font-medium">{healthStatus}</span>
          )}
        </div>
      </div>

      {/* Intake Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="intake-text" className="block text-sm font-medium text-gray-700 mb-2">
            Case Description
          </label>
          <textarea
            id="intake-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Describe your legal issue... (e.g., 'I live in RI. Landlord kept my deposit. Need help filing small claims.')"
            className="w-full h-32 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !text.trim()}
          className="w-full px-6 py-3 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? '🔄 Processing...' : '🚀 Process with LangGraph'}
        </button>
      </form>

      {/* Error Display */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-800 font-medium">Error:</p>
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Result Display */}
      {result && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
          <h3 className="text-lg font-semibold text-green-800 mb-3">
            ✅ Intake Processed Successfully
          </h3>
          
          <div className="space-y-3">
            <div>
              <span className="font-medium text-gray-700">Intake ID:</span>
              <span className="ml-2 font-mono text-sm bg-gray-100 px-2 py-1 rounded">
                {result.intake_id}
              </span>
            </div>
            
            <div>
              <span className="font-medium text-gray-700">Status:</span>
              <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                {result.status}
              </span>
            </div>

            {result.summary && (
              <div>
                <span className="font-medium text-gray-700">AI Summary:</span>
                <div className="mt-2 p-3 bg-white border rounded-md">
                  <p className="text-gray-800 whitespace-pre-wrap">{result.summary}</p>
                </div>
              </div>
            )}

            <div>
              <span className="font-medium text-gray-700">Raw Text:</span>
              <div className="mt-2 p-3 bg-gray-50 border rounded-md">
                <p className="text-gray-600 text-sm whitespace-pre-wrap">{result.raw_text}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-md">
        <h4 className="font-medium text-blue-800 mb-2">How to test:</h4>
        <ol className="text-sm text-blue-700 space-y-1 list-decimal list-inside">
          <li>Make sure the LangGraph service is running on port 8010</li>
          <li>Click "Check LangGraph Health" to verify the service</li>
          <li>Enter a legal case description in the text area</li>
          <li>Click "Process with LangGraph" to see the AI summarization</li>
          <li>Check your Supabase database for the stored intake record</li>
        </ol>
      </div>
    </div>
  );
};

export default LangGraphIntake;
