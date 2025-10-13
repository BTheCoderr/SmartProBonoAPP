# Saul Legal AI Integration Guide

## Overview

SmartProBono now integrates with **Saul-7B-Instruct-v1**, a specialized legal language model from Equall. This model is specifically trained for legal text comprehension and generation, making it ideal for legal assistance tasks.

## What is Saul?

Saul-7B-Instruct-v1 is:
- **Base Model**: Mistral-7B (7 billion parameters)
- **Specialization**: Legal domain training with 30+ billion legal tokens
- **License**: MIT License (open source)
- **Company**: Equall (https://equall.com/)
- **Research Paper**: [SaulLM-7B: A pioneering Large Language Model for Law](https://arxiv.org/abs/2403.03883)

## Features

### 🎯 Legal Specialization
- Trained specifically on legal texts and documents
- Better understanding of legal terminology and concepts
- Improved performance on legal reasoning tasks

### 🔄 Intelligent Fallbacks
- Automatically falls back to Ollama models if Saul is unavailable
- Maintains service reliability even with model issues
- Multiple AI service layers for redundancy

### 🎛️ Flexible Integration
- Works with existing SmartProBono chat interfaces
- Supports multiple task types (chat, research, analysis, etc.)
- Configurable parameters (temperature, max tokens)

## API Endpoints

### 1. Enhanced AI Chat (Recommended)
```
POST /api/v1/ai/chat
```
Uses Saul as primary model with intelligent fallbacks.

**Payload:**
```json
{
  "message": "What is contract law?",
  "task_type": "legal",
  "model": "auto",
  "conversation_id": "optional",
  "history": []
}
```

### 2. Direct Saul Chat
```
POST /api/v1/ai/saul/chat
```
Direct access to Saul model only.

**Payload:**
```json
{
  "message": "How do I file for bankruptcy?",
  "task_type": "legal",
  "max_tokens": 200,
  "temperature": 0.7
}
```

### 3. Model Information
```
GET /api/v1/ai/saul/info
```
Get Saul model information and health status.

### 4. Available Models
```
GET /api/v1/ai/models/available
```
Get information about all available AI models.

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

The following new dependencies are included:
- `transformers>=4.44.0,<5.0.0`
- `torch>=2.0.0,<3.0.0`
- `accelerate>=0.30.0,<1.0.0`
- `safetensors>=0.4.0,<1.0.0`

### 2. Test Integration
```bash
python test_saul_integration.py
```

### 3. Start Server
```bash
cd backend
python combined_server.py
```

## Usage Examples

### Python API Usage

```python
import requests

# Using enhanced AI chat (recommended)
response = requests.post("http://localhost:3001/api/v1/ai/chat", json={
    "message": "What are my rights as a tenant?",
    "task_type": "legal",
    "model": "auto"
})

# Using direct Saul chat
response = requests.post("http://localhost:3001/api/v1/ai/saul/chat", json={
    "message": "How do I draft a will?",
    "task_type": "legal",
    "max_tokens": 300,
    "temperature": 0.6
})
```

### Frontend Integration

The existing legal chat components will automatically use Saul when available. No frontend changes required!

## Model Selection Logic

The system intelligently selects models based on:

1. **User Role**: Lawyers/attorneys get Saul priority
2. **Task Type**: Legal tasks (research, analysis) use Saul
3. **Explicit Requests**: Respects user model preferences
4. **Availability**: Falls back if Saul is unavailable

### Task Types
- `legal` - Uses Saul for specialized legal responses
- `research` - Saul for legal research tasks
- `analysis` - Saul for document analysis
- `chat` - Saul for general legal chat
- `default` - Saul for general tasks

## Performance Considerations

### System Requirements
- **GPU**: Recommended for faster inference (CUDA compatible)
- **CPU**: Fallback option, slower but functional
- **RAM**: 8GB+ recommended for model loading
- **Storage**: ~15GB for model files (downloaded on first use)

### Optimization
- Model loads on first use (cached afterward)
- Automatic device detection (GPU/CPU)
- Configurable token limits for response length
- Temperature control for response creativity

## Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Check internet connection for model download
   - Verify sufficient disk space (~15GB)
   - Ensure proper Python dependencies

2. **Memory Issues**
   - Reduce `max_tokens` parameter
   - Use CPU instead of GPU if limited VRAM
   - Close other applications to free RAM

3. **Slow Responses**
   - Normal for first-time model loading
   - Subsequent requests should be faster
   - Consider using smaller `max_tokens`

### Health Checks

```bash
# Check model status
curl http://localhost:3001/api/v1/ai/saul/info

# Check all available models
curl http://localhost:3001/api/v1/ai/models/available
```

## Legal Disclaimer

⚠️ **Important**: Saul provides general legal information, not legal advice. Always consult with a qualified attorney for specific legal matters.

## Support

- **Saul Model**: [Hugging Face Model Page](https://huggingface.co/Equall/Saul-7B-Instruct-v1)
- **Equall Company**: [https://equall.com/](https://equall.com/)
- **Research Paper**: [arXiv:2403.03883](https://arxiv.org/abs/2403.03883)
- **SmartProBono Issues**: Check project documentation or create an issue

## Changelog

### v1.0.0 - Initial Integration
- Added Saul-7B-Instruct-v1 model integration
- Created Saul Legal AI Service
- Added Saul Enhanced AI Service with fallbacks
- Updated API endpoints for Saul access
- Added comprehensive testing suite
- Updated requirements.txt with new dependencies
