import React from 'react';
import LangGraphIntake from '../components/LangGraphIntake';

const LangGraphDemo = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            SmartProBono LangGraph Demo
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Test the new LangGraph-powered case intake system. This demonstrates 
            AI-powered legal case summarization and orchestration.
          </p>
        </div>

        <LangGraphIntake />

        <div className="mt-12 max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">
              🏗️ Architecture Overview
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-blue-600">What's New</h3>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li>• <strong>LangGraph Service:</strong> Orchestrates AI workflows</li>
                  <li>• <strong>Case Intake:</strong> Automated legal case processing</li>
                  <li>• <strong>AI Summarization:</strong> Extracts key legal details</li>
                  <li>• <strong>Supabase Integration:</strong> Persistent case storage</li>
                  <li>• <strong>FastAPI Backend:</strong> High-performance API</li>
                </ul>
              </div>
              
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-green-600">Next Steps</h3>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li>• <strong>Lawyer Matching:</strong> AI-powered case assignment</li>
                  <li>• <strong>Conflict Checking:</strong> Automated conflict detection</li>
                  <li>• <strong>Human Review:</strong> Pause for admin approval</li>
                  <li>• <strong>Notifications:</strong> Email/SMS case updates</li>
                  <li>• <strong>Streaming:</strong> Real-time progress updates</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LangGraphDemo;
