import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ModelManagement.css';

const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001';

const ModelManagement = () => {
  const [models, setModels] = useState({
    pretrained: [],
    custom: []
  });
  const [selectedModel, setSelectedModel] = useState('saul');
  const [modelStatus, setModelStatus] = useState(null);
  const [testMessage, setTestMessage] = useState('');
  const [testResponse, setTestResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  // Training state
  const [trainingData, setTrainingData] = useState([
    { question: '', answer: '' }
  ]);
  const [modelName, setModelName] = useState('');
  const [trainingEpochs, setTrainingEpochs] = useState(3);
  const [isTraining, setIsTraining] = useState(false);
  const [trainingProgress, setTrainingProgress] = useState(null);

  useEffect(() => {
    loadModels();
    loadModelStatus();
  }, []);

  const loadModels = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/v1/models/available`);
      if (response.data.success) {
        setModels({
          pretrained: Object.entries(response.data.pretrained_models || {}).map(
            ([key, value]) => ({ id: key, ...value })
          ),
          custom: response.data.custom_models || []
        });
      }
    } catch (error) {
      console.error('Error loading models:', error);
    }
  };

  const loadModelStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/v1/models/status`);
      if (response.data.success) {
        setModelStatus(response.data.health);
      }
    } catch (error) {
      console.error('Error loading model status:', error);
    }
  };

  const testModel = async () => {
    if (!testMessage.trim()) {
      alert('Please enter a test message');
      return;
    }

    setIsLoading(true);
    setTestResponse(null);

    try {
      const response = await axios.post(
        `${API_BASE}/api/v1/models/test/${selectedModel}`,
        {
          message: testMessage,
          max_tokens: 150
        }
      );

      if (response.data.success) {
        setTestResponse(response.data.response);
      }
    } catch (error) {
      console.error('Error testing model:', error);
      setTestResponse({
        success: false,
        text: error.response?.data?.error || 'Error testing model'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const addTrainingExample = () => {
    setTrainingData([...trainingData, { question: '', answer: '' }]);
  };

  const removeTrainingExample = (index) => {
    const newData = trainingData.filter((_, i) => i !== index);
    setTrainingData(newData);
  };

  const updateTrainingExample = (index, field, value) => {
    const newData = [...trainingData];
    newData[index][field] = value;
    setTrainingData(newData);
  };

  const startTraining = async () => {
    // Validate training data
    const validData = trainingData.filter(
      item => item.question.trim() && item.answer.trim()
    );

    if (validData.length === 0) {
      alert('Please add at least one training example with both question and answer');
      return;
    }

    if (!modelName.trim()) {
      alert('Please enter a name for your custom model');
      return;
    }

    setIsTraining(true);
    setTrainingProgress({ status: 'preparing', message: 'Preparing training data...' });

    try {
      // Step 1: Prepare training data
      const prepareResponse = await axios.post(
        `${API_BASE}/api/v1/models/train/prepare-data`,
        {
          conversations: validData
        }
      );

      if (!prepareResponse.data.success) {
        throw new Error('Failed to prepare training data');
      }

      const trainingFile = prepareResponse.data.training_file;
      
      setTrainingProgress({ 
        status: 'training', 
        message: `Training model with ${validData.length} examples... This may take several minutes.` 
      });

      // Step 2: Start training
      const trainResponse = await axios.post(
        `${API_BASE}/api/v1/models/train/start`,
        {
          training_data_path: trainingFile,
          model_name: modelName,
          epochs: trainingEpochs
        }
      );

      if (trainResponse.data.success) {
        setTrainingProgress({
          status: 'completed',
          message: `Model "${modelName}" trained successfully!`,
          result: trainResponse.data
        });
        
        // Reload models list
        await loadModels();
      } else {
        throw new Error(trainResponse.data.error || 'Training failed');
      }

    } catch (error) {
      console.error('Training error:', error);
      setTrainingProgress({
        status: 'error',
        message: error.response?.data?.error || error.message || 'Training failed'
      });
    } finally {
      setIsTraining(false);
    }
  };

  return (
    <div className="model-management">
      <h1>🤖 AI Model Management</h1>

      {/* Model Status Dashboard */}
      <div className="model-status-section">
        <h2>Model Status</h2>
        {modelStatus ? (
          <div className="status-grid">
            <div className="status-card">
              <h3>Saul Legal AI</h3>
              <div className={`status-indicator ${modelStatus.saul_model?.status}`}>
                {modelStatus.saul_model?.status || 'unknown'}
              </div>
              <p>Model: {modelStatus.saul_model?.health_status?.model_loaded ? 'Loaded' : 'Not Loaded'}</p>
              <p>Device: {modelStatus.saul_model?.health_status?.device}</p>
            </div>
            <div className="status-card">
              <h3>Recommended Model</h3>
              <p className="recommended">{modelStatus.recommended_model || 'auto'}</p>
            </div>
          </div>
        ) : (
          <p>Loading model status...</p>
        )}
      </div>

      {/* Available Models */}
      <div className="available-models-section">
        <h2>Available Models</h2>
        
        <h3>Pre-trained Models</h3>
        <div className="models-grid">
          {models.pretrained.map(model => (
            <div key={model.id} className="model-card">
              <h4>{model.name}</h4>
              <p>{model.description}</p>
              <div className="model-info">
                <span>Status: {model.available ? '✅ Available' : '❌ Unavailable'}</span>
                <span>Device: {model.device}</span>
              </div>
              <button 
                onClick={() => setSelectedModel(model.id)}
                className={selectedModel === model.id ? 'selected' : ''}
              >
                {selectedModel === model.id ? '✓ Selected' : 'Select'}
              </button>
            </div>
          ))}
        </div>

        {models.custom.length > 0 && (
          <>
            <h3>Custom Trained Models</h3>
            <div className="models-grid">
              {models.custom.map(model => (
                <div key={model.name} className="model-card custom">
                  <h4>{model.name}</h4>
                  <div className="model-info">
                    <span>Created: {new Date(model.modified).toLocaleDateString()}</span>
                  </div>
                  <button onClick={() => setSelectedModel(model.name)}>
                    {selectedModel === model.name ? '✓ Selected' : 'Select'}
                  </button>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Model Testing */}
      <div className="model-testing-section">
        <h2>Test Selected Model: {selectedModel}</h2>
        <div className="test-area">
          <textarea
            value={testMessage}
            onChange={(e) => setTestMessage(e.target.value)}
            placeholder="Enter a test message or legal question..."
            rows={4}
          />
          <button 
            onClick={testModel}
            disabled={isLoading}
            className="primary-btn"
          >
            {isLoading ? 'Testing...' : 'Test Model'}
          </button>

          {testResponse && (
            <div className={`test-response ${testResponse.success ? 'success' : 'error'}`}>
              <h4>Response:</h4>
              <p>{testResponse.text}</p>
              {testResponse.success && (
                <div className="response-meta">
                  <span>Model: {testResponse.model}</span>
                  <span>Task: {testResponse.task_type}</span>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Custom Model Training */}
      <div className="model-training-section">
        <h2>Train Custom Legal Model</h2>
        <p className="training-description">
          Train a custom legal AI model on your specific data. Add question-answer pairs from your legal consultations.
        </p>

        <div className="training-form">
          <div className="form-group">
            <label>Model Name:</label>
            <input
              type="text"
              value={modelName}
              onChange={(e) => setModelName(e.target.value)}
              placeholder="e.g., my-family-law-model"
              disabled={isTraining}
            />
          </div>

          <div className="form-group">
            <label>Training Epochs:</label>
            <input
              type="number"
              value={trainingEpochs}
              onChange={(e) => setTrainingEpochs(parseInt(e.target.value))}
              min={1}
              max={10}
              disabled={isTraining}
            />
            <small>Higher epochs = better training but takes longer</small>
          </div>

          <h3>Training Data</h3>
          <div className="training-examples">
            {trainingData.map((example, index) => (
              <div key={index} className="training-example">
                <div className="example-header">
                  <h4>Example {index + 1}</h4>
                  {trainingData.length > 1 && (
                    <button
                      onClick={() => removeTrainingExample(index)}
                      className="remove-btn"
                      disabled={isTraining}
                    >
                      ✕
                    </button>
                  )}
                </div>
                <div className="example-fields">
                  <div className="field">
                    <label>Question:</label>
                    <textarea
                      value={example.question}
                      onChange={(e) => updateTrainingExample(index, 'question', e.target.value)}
                      placeholder="Legal question..."
                      rows={2}
                      disabled={isTraining}
                    />
                  </div>
                  <div className="field">
                    <label>Answer:</label>
                    <textarea
                      value={example.answer}
                      onChange={(e) => updateTrainingExample(index, 'answer', e.target.value)}
                      placeholder="Legal answer/response..."
                      rows={3}
                      disabled={isTraining}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="training-actions">
            <button
              onClick={addTrainingExample}
              className="secondary-btn"
              disabled={isTraining}
            >
              + Add Example
            </button>
            <button
              onClick={startTraining}
              className="primary-btn"
              disabled={isTraining}
            >
              {isTraining ? 'Training...' : 'Start Training'}
            </button>
          </div>

          {trainingProgress && (
            <div className={`training-progress ${trainingProgress.status}`}>
              <h4>Training Status: {trainingProgress.status}</h4>
              <p>{trainingProgress.message}</p>
              {trainingProgress.result && (
                <div className="training-result">
                  <p>✓ Model path: {trainingProgress.result.model_path}</p>
                  <p>✓ Training examples: {trainingProgress.result.training_examples}</p>
                  <p>✓ Final loss: {trainingProgress.result.final_loss?.toFixed(4)}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ModelManagement;

