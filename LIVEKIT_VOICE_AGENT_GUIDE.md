# 🎤 SmartProBono LiveKit Voice Agent Integration Guide

## 🚀 Complete Real-Time Voice AI System

This guide covers the complete integration of LiveKit voice agents with the SmartProBono platform, creating a sophisticated real-time voice AI system for legal professionals.

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Voice Agents](#voice-agents)
4. [Installation & Setup](#installation--setup)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Integration with SmartProBono](#integration-with-smartprobono)
8. [Deployment](#deployment)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

## 🎯 System Overview

The LiveKit Voice Agent system provides:

- **Real-time voice conversations** with AI agents
- **Multi-agent routing** between specialists
- **Context-aware responses** using SmartProBono data
- **Professional voice interactions** optimized for legal professionals
- **Seamless integration** with existing SmartProBono platform

### Key Features

- 🎤 **Voice-First Interface**: Natural speech interactions
- 🤖 **Multi-Agent System**: Sales, Technical, and Pricing specialists
- 🧠 **AI-Powered**: Cerebras LLaMA 3.3 70B for real-time responses
- 🔄 **Smart Transfers**: Automatic routing based on user intent
- 📞 **LiveKit Integration**: Enterprise-grade real-time communication
- ⚖️ **Legal Domain**: Specialized for legal professionals

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SmartProBono Platform                    │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React)  │  Backend (Flask)  │  Database (SQLite) │
├─────────────────────────────────────────────────────────────┤
│              Multi-Model AI System                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Legal AI    │  │ SmartProBono│  │ LiveKit Voice Agent │ │
│  │ (Ollama)    │  │ Agent       │  │ (Cerebras)          │ │
│  │             │  │ (Gemini)    │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│              Voice AI Components                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Deepgram    │  │ Silero VAD  │  │ LiveKit Real-time   │ │
│  │ STT/TTS     │  │             │  │ Communication       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🤖 Voice Agents

### 1. Sales Agent 🏷️
- **Purpose**: General inquiries and platform overview
- **Capabilities**: Lead qualification, benefit explanation, initial consultation
- **Transfer Triggers**: Technical questions, pricing discussions
- **Voice**: Professional, welcoming tone

### 2. Technical Agent 💻
- **Purpose**: Technical specifications and implementation
- **Capabilities**: AI model details, integrations, security, architecture
- **Transfer Triggers**: Sales questions, pricing discussions
- **Voice**: Technical, detailed explanations

### 3. Pricing Agent 💰
- **Purpose**: Pricing tiers and ROI discussions
- **Capabilities**: Cost analysis, value proposition, ROI calculations
- **Transfer Triggers**: Technical questions, general sales
- **Voice**: Professional, value-focused

## 📦 Installation & Setup

### Prerequisites

```bash
# Ensure you're in the SmartProBono directory
cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main

# Activate virtual environment
source .venv/bin/activate
```

### Install LiveKit Packages

```bash
# Install LiveKit agents with all plugins
pip install "livekit-agents[deepgram,silero,openai]"

# Verify installation
python -c "import livekit.agents; print('✅ LiveKit installed successfully')"
```

### Required API Keys

```bash
# Set environment variables
export DEEPGRAM_API_KEY="56a34725a43e0999b9e3159545be8ff94948fc56"
export CEREBRAS_API_KEY="csk-yfmevnrjp54jfmym4h2cynte6vec6f6er5v383xtc3txk4km"
export LIVEKIT_API_KEY="APIDfFD86iZa6mQ"
export LIVEKIT_API_SECRET="OPatlk2JCTKKtzLeocVgce0Af5XfldXO0lL8aMDv9qbA"
export LIVEKIT_WS_URL="wss://smartprobono-lr9wv8ch.livekit.cloud"
```

## ⚙️ Configuration

### Context Files

The system loads context from the `context/` directory:

```bash
# Context directory structure
context/
└── products.json    # SmartProBono product information, pricing, features
```

### Agent Configuration

Each agent is configured with:

- **LLM**: Cerebras LLaMA 3.3 70B for real-time responses
- **STT**: Deepgram speech-to-text
- **TTS**: Deepgram text-to-speech
- **VAD**: Silero voice activity detection
- **Context**: SmartProBono-specific information

## 🎯 Usage

### Starting the Voice Agent

```bash
# Start the LiveKit voice agent
python livekit_voice_agent.py
```

### Connecting to LiveKit

1. **Web Interface**: Connect via LiveKit web interface
2. **Room Connection**: Agent connects to specified LiveKit room
3. **Voice Chat**: Start speaking naturally with the agent

### Agent Transfers

During conversation, users can request transfers:

- **"I need technical details"** → Technical Agent
- **"Let's discuss pricing"** → Pricing Agent
- **"Back to sales"** → Sales Agent

### Sample Conversation Flow

```
User: "Hello, I'm interested in SmartProBono for my law firm"
Sales Agent: "Welcome! I'd be happy to tell you about our AI-powered legal platform..."

User: "What AI models do you use?"
Sales Agent: "Let me transfer you to our technical specialist for detailed information."
Technical Agent: "Hi, I'm the technical specialist. We use multiple AI models including..."

User: "How much does this cost?"
Technical Agent: "Let me connect you with our pricing specialist."
Pricing Agent: "Hello, I'm the pricing specialist. We offer three tiers starting at $199/month..."
```

## 🔗 Integration with SmartProBono

### Existing Integration Points

The LiveKit voice agent integrates with the existing SmartProBono system:

1. **Multi-Model AI System**: Works alongside Ollama and Gemini models
2. **Context Sharing**: Uses the same SmartProBono product information
3. **API Endpoints**: Can be called from existing Flask backend
4. **Frontend Components**: Integrates with React frontend

### API Integration

```python
# Example: Call voice agent from SmartProBono backend
from livekit_voice_agent import SalesAgent

# Initialize agent
agent = SalesAgent()

# Process voice input
response = await agent.process_voice_input(user_message)
```

### Frontend Integration

```javascript
// Example: React component for voice chat
import { VoiceChat } from './components/VoiceChat';

function SmartProBonoVoice() {
  return (
    <VoiceChat
      livekitUrl="wss://smartprobono-lr9wv8ch.livekit.cloud"
      apiKey="APIDfFD86iZa6mQ"
      room="smartprobono-voice"
    />
  );
}
```

## 🚀 Deployment

### Development Environment

```bash
# Test the system
python test_livekit_agent.py

# Run demo
python livekit_demo.py

# Start voice agent
python livekit_voice_agent.py
```

### Production Deployment

1. **LiveKit Cloud**: Deploy to LiveKit cloud infrastructure
2. **Environment Variables**: Set production API keys
3. **SSL Certificates**: Configure HTTPS for production
4. **Load Balancing**: Scale for multiple concurrent users
5. **Monitoring**: Set up logging and monitoring

### Docker Deployment

```dockerfile
# Dockerfile for LiveKit voice agent
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "livekit_voice_agent.py"]
```

## 🧪 Testing

### Test Suite

```bash
# Run comprehensive tests
python test_livekit_agent.py
```

### Test Coverage

- ✅ **Import Tests**: Verify all packages are installed
- ✅ **Context Loading**: Test context file loading
- ✅ **Agent Classes**: Test agent instantiation
- ✅ **API Keys**: Verify configuration
- ✅ **Context Files**: Check file existence and content

### Manual Testing

1. **Voice Input**: Test speech-to-text accuracy
2. **Agent Responses**: Verify context-aware responses
3. **Transfers**: Test agent-to-agent transfers
4. **Voice Output**: Check text-to-speech quality
5. **Context Accuracy**: Verify SmartProBono information

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'livekit'
# Solution: Install LiveKit packages
pip install "livekit-agents[deepgram,silero,openai]"
```

#### 2. API Key Issues
```bash
# Error: Invalid API key
# Solution: Verify API keys are set correctly
echo $CEREBRAS_API_KEY
echo $DEEPGRAM_API_KEY
```

#### 3. Context Loading Issues
```bash
# Error: No context files found
# Solution: Ensure context directory exists
mkdir -p context
# Add products.json file
```

#### 4. LiveKit Connection Issues
```bash
# Error: Cannot connect to LiveKit
# Solution: Verify LiveKit configuration
echo $LIVEKIT_WS_URL
echo $LIVEKIT_API_KEY
```

### Debug Mode

```bash
# Enable debug logging
export LIVEKIT_LOG_LEVEL=debug
python livekit_voice_agent.py
```

### Logs

Check logs for detailed error information:

```bash
# View agent logs
tail -f livekit_agent.log

# View LiveKit logs
tail -f livekit.log
```

## 📊 Performance Metrics

### Expected Performance

- **Voice Latency**: < 500ms for responses
- **Transfer Time**: < 1s for agent switches
- **Context Loading**: < 100ms for initialization
- **Concurrent Users**: 50+ simultaneous conversations

### Monitoring

- **Response Time**: Track voice response latency
- **Transfer Success**: Monitor agent transfer success rate
- **Context Accuracy**: Verify response relevance
- **User Satisfaction**: Collect feedback on voice quality

## 🎉 Success Metrics

### Technical Success

- ✅ All tests passing (5/5)
- ✅ Voice agents responding correctly
- ✅ Multi-agent transfers working
- ✅ Context-aware responses
- ✅ LiveKit integration functional

### Business Success

- 🎯 **Lead Qualification**: Improved sales conversion
- 💬 **User Engagement**: Higher interaction rates
- ⚡ **Response Time**: Faster customer service
- 🎤 **Voice Quality**: Professional communication
- 🔄 **Agent Efficiency**: Seamless transfers

## 🔮 Future Enhancements

### Planned Features

1. **Custom Voices**: Brand-specific voice personalities
2. **Multi-Language**: Support for multiple languages
3. **Sentiment Analysis**: Real-time emotion detection
4. **Call Recording**: Conversation analytics
5. **CRM Integration**: Direct lead capture
6. **Mobile App**: Native mobile voice interface

### Advanced Capabilities

- **Predictive Routing**: AI-powered agent selection
- **Context Memory**: Long-term conversation memory
- **Custom Training**: Firm-specific AI training
- **Analytics Dashboard**: Real-time performance metrics
- **A/B Testing**: Voice and response optimization

---

## 🎯 Quick Start Checklist

- [ ] Install LiveKit packages
- [ ] Configure API keys
- [ ] Create context files
- [ ] Test agent setup
- [ ] Start voice agent
- [ ] Connect via LiveKit
- [ ] Test voice conversations
- [ ] Verify agent transfers
- [ ] Deploy to production

## 📞 Support

For technical support or questions:

1. **Documentation**: Check this guide first
2. **Test Suite**: Run `python test_livekit_agent.py`
3. **Demo**: Run `python livekit_demo.py`
4. **Logs**: Check console output and log files
5. **Community**: LiveKit Discord for technical issues

---

**🎉 Congratulations! You now have a complete real-time voice AI system integrated with SmartProBono!**
