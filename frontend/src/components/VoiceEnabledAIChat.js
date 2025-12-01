/**
 * Voice-Enabled AI Chat Component
 * Provides voice input and output for AI chat interactions
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  TextField,
  Typography,
  IconButton,
  Button,
  Chip,
  CircularProgress,
  Alert,
  Tooltip,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Card,
  CardContent
} from '@mui/material';
import {
  Mic as MicIcon,
  MicOff as MicOffIcon,
  VolumeUp as VolumeUpIcon,
  VolumeOff as VolumeOffIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Settings as SettingsIcon,
  RecordVoiceOver as RecordIcon,
  Hearing as HearingIcon,
  SmartToy as AIIcon
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

const VoiceEnabledAIChat = () => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [voiceSettings, setVoiceSettings] = useState({
    language: 'en-US',
    voice: 'default',
    speed: 1.0,
    pitch: 1.0,
    volume: 0.8
  });
  const [showSettings, setShowSettings] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [synthesis, setSynthesis] = useState(null);
  
  const messagesEndRef = useRef(null);
  const audioRef = useRef(null);

  // Check for browser support
  useEffect(() => {
    const checkSupport = () => {
      const speechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const speechSynthesis = window.speechSynthesis;
      
      if (speechRecognition && speechSynthesis) {
        setIsSupported(true);
        
        // Initialize speech recognition
        const recognitionInstance = new speechRecognition();
        recognitionInstance.continuous = false;
        recognitionInstance.interimResults = true;
        recognitionInstance.lang = voiceSettings.language;
        
        recognitionInstance.onstart = () => {
          setIsListening(true);
          setError(null);
        };
        
        recognitionInstance.onresult = (event) => {
          let finalTranscript = '';
          let interimTranscript = '';
          
          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
              finalTranscript += transcript;
            } else {
              interimTranscript += transcript;
            }
          }
          
          if (finalTranscript) {
            setInput(finalTranscript);
            handleSubmit(finalTranscript);
          } else {
            setInput(interimTranscript);
          }
        };
        
        recognitionInstance.onerror = (event) => {
          console.error('Speech recognition error:', event.error);
          setError(`Speech recognition error: ${event.error}`);
          setIsListening(false);
        };
        
        recognitionInstance.onend = () => {
          setIsListening(false);
        };
        
        setRecognition(recognitionInstance);
        setSynthesis(speechSynthesis);
      } else {
        setIsSupported(false);
        setError('Voice features not supported in this browser');
      }
    };
    
    checkSupport();
  }, [voiceSettings.language]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const startListening = () => {
    if (recognition && !isListening) {
      setInput('');
      recognition.start();
    }
  };

  const stopListening = () => {
    if (recognition && isListening) {
      recognition.stop();
    }
  };

  const handleSubmit = async (text = input) => {
    if (!text.trim() || isProcessing) return;

    const userMessage = {
      id: Date.now(),
      text: text,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString(),
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);
    setError(null);

    try {
      // Call AI backend
      const response = await fetch('http://localhost:3001/api/legal-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: text,
          jurisdiction: 'ri'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        const aiMessage = {
          id: Date.now() + 1,
          text: formatAIResponse(data),
          sender: 'assistant',
          timestamp: new Date().toLocaleTimeString(),
          type: 'text',
          analysis: data.analysis,
          disclaimers: data.disclaimers || [],
          warnings: data.warnings || [],
          recommendations: data.recommendations || []
        };

        setMessages(prev => [...prev, aiMessage]);
        
        // Speak the response
        speakText(aiMessage.text);
      } else {
        throw new Error(data.error || 'Analysis failed');
      }
    } catch (err) {
      console.error('Error calling AI backend:', err);
      setError(err.message);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: "I apologize, but I'm experiencing technical difficulties. Please try again or consult with a qualified attorney for immediate assistance.",
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
        type: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const speakText = (text) => {
    if (!synthesis || isSpeaking) return;

    // Stop any current speech
    synthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = voiceSettings.speed;
    utterance.pitch = voiceSettings.pitch;
    utterance.volume = voiceSettings.volume;
    utterance.lang = voiceSettings.language;

    utterance.onstart = () => {
      setIsSpeaking(true);
    };

    utterance.onend = () => {
      setIsSpeaking(false);
    };

    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event.error);
      setError(`Speech synthesis error: ${event.error}`);
      setIsSpeaking(false);
    };

    synthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    if (synthesis) {
      synthesis.cancel();
      setIsSpeaking(false);
    }
  };

  const formatAIResponse = (data) => {
    // Just return the text directly - no verbose formatting
    if (data.text) return data.text;
    if (data.response) return data.response;
    if (data.analysis?.text) return data.analysis.text;
    return data.message || 'I understand your question. How can I help you?';
  };

  const getAvailableVoices = () => {
    if (!synthesis) return [];
    return synthesis.getVoices().filter(voice => 
      voice.lang.startsWith(voiceSettings.language.split('-')[0])
    );
  };

  const handleVoiceChange = (event) => {
    setVoiceSettings(prev => ({
      ...prev,
      voice: event.target.value
    }));
  };

  const handleSpeedChange = (event, newValue) => {
    setVoiceSettings(prev => ({
      ...prev,
      speed: newValue
    }));
  };

  const handlePitchChange = (event, newValue) => {
    setVoiceSettings(prev => ({
      ...prev,
      pitch: newValue
    }));
  };

  const handleVolumeChange = (event, newValue) => {
    setVoiceSettings(prev => ({
      ...prev,
      volume: newValue
    }));
  };

  const handleLanguageChange = (event) => {
    setVoiceSettings(prev => ({
      ...prev,
      language: event.target.value
    }));
  };

  if (!isSupported) {
    return (
      <Alert severity="warning" sx={{ m: 2 }}>
        Voice features are not supported in this browser. Please use Chrome, Firefox, or Safari for the best experience.
      </Alert>
    );
  }

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Paper elevation={1} sx={{ p: 2, borderRadius: 0 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <AIIcon color="primary" />
            <Typography variant="h6">Voice-Enabled AI Legal Assistant</Typography>
            <Chip 
              label={isListening ? "Listening" : isSpeaking ? "Speaking" : "Ready"} 
              color={isListening ? "primary" : isSpeaking ? "secondary" : "default"}
              size="small"
            />
          </Box>
          
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Tooltip title="Voice Settings">
              <IconButton onClick={() => setShowSettings(!showSettings)}>
                <SettingsIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      </Paper>

      {/* Voice Settings Panel */}
      {showSettings && (
        <Paper elevation={1} sx={{ p: 2, m: 1 }}>
          <Typography variant="h6" gutterBottom>Voice Settings</Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Language</InputLabel>
              <Select
                value={voiceSettings.language}
                onChange={handleLanguageChange}
                label="Language"
              >
                <MenuItem value="en-US">English (US)</MenuItem>
                <MenuItem value="en-GB">English (UK)</MenuItem>
                <MenuItem value="es-ES">Spanish</MenuItem>
                <MenuItem value="fr-FR">French</MenuItem>
                <MenuItem value="de-DE">German</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Voice</InputLabel>
              <Select
                value={voiceSettings.voice}
                onChange={handleVoiceChange}
                label="Voice"
              >
                {getAvailableVoices().map((voice, index) => (
                  <MenuItem key={index} value={voice.name}>
                    {voice.name} ({voice.lang})
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
          
          <Box sx={{ mt: 2 }}>
            <Typography gutterBottom>Speed: {voiceSettings.speed.toFixed(1)}x</Typography>
            <Slider
              value={voiceSettings.speed}
              onChange={handleSpeedChange}
              min={0.5}
              max={2.0}
              step={0.1}
              marks={[
                { value: 0.5, label: '0.5x' },
                { value: 1.0, label: '1.0x' },
                { value: 2.0, label: '2.0x' }
              ]}
            />
          </Box>
          
          <Box sx={{ mt: 2 }}>
            <Typography gutterBottom>Pitch: {voiceSettings.pitch.toFixed(1)}</Typography>
            <Slider
              value={voiceSettings.pitch}
              onChange={handlePitchChange}
              min={0.5}
              max={2.0}
              step={0.1}
              marks={[
                { value: 0.5, label: 'Low' },
                { value: 1.0, label: 'Normal' },
                { value: 2.0, label: 'High' }
              ]}
            />
          </Box>
          
          <Box sx={{ mt: 2 }}>
            <Typography gutterBottom>Volume: {Math.round(voiceSettings.volume * 100)}%</Typography>
            <Slider
              value={voiceSettings.volume}
              onChange={handleVolumeChange}
              min={0}
              max={1}
              step={0.1}
              marks={[
                { value: 0, label: '0%' },
                { value: 0.5, label: '50%' },
                { value: 1, label: '100%' }
              ]}
            />
          </Box>
        </Paper>
      )}

      {/* Messages */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 1 }}>
        {messages.length === 0 ? (
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100%',
            flexDirection: 'column',
            gap: 2
          }}>
            <HearingIcon sx={{ fontSize: 64, color: 'primary.main', opacity: 0.7 }} />
            <Typography variant="h6" color="text.secondary">
              Start a conversation with your voice
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Click the microphone button or type your message
            </Typography>
          </Box>
        ) : (
          <List>
            {messages.map((message) => (
              <ListItem key={message.id} sx={{ 
                display: 'flex', 
                justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                alignItems: 'flex-start'
              }}>
                <Card sx={{ 
                  maxWidth: '70%',
                  bgcolor: message.sender === 'user' ? 'primary.main' : 'grey.100',
                  color: message.sender === 'user' ? 'primary.contrastText' : 'text.primary'
                }}>
                  <CardContent>
                    <Typography variant="body2" sx={{ wordBreak: 'break-word' }}>
                      {message.text}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 1 }}>
                      <Typography variant="caption" sx={{ opacity: 0.7 }}>
                        {message.timestamp}
                      </Typography>
                      {message.sender === 'assistant' && (
                        <Box>
                          <Tooltip title="Speak">
                            <IconButton 
                              size="small" 
                              onClick={() => speakText(message.text)}
                              disabled={isSpeaking}
                            >
                              <VolumeUpIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </ListItem>
            ))}
            <div ref={messagesEndRef} />
          </List>
        )}
      </Box>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ m: 1 }}>
          {error}
        </Alert>
      )}

      {/* Input Area */}
      <Paper elevation={1} sx={{ p: 2, borderRadius: 0 }}>
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message or use voice input..."
            variant="outlined"
            size="small"
            disabled={isProcessing}
          />
          
          {/* Voice Controls */}
          <Box sx={{ display: 'flex', gap: 1 }}>
            {isListening ? (
              <Tooltip title="Stop Listening">
                <IconButton 
                  color="error" 
                  onClick={stopListening}
                  sx={{ bgcolor: 'error.main', color: 'white' }}
                >
                  <MicOffIcon />
                </IconButton>
              </Tooltip>
            ) : (
              <Tooltip title="Start Voice Input">
                <IconButton 
                  color="primary" 
                  onClick={startListening}
                  disabled={isProcessing}
                >
                  <MicIcon />
                </IconButton>
              </Tooltip>
            )}
            
            {isSpeaking && (
              <Tooltip title="Stop Speaking">
                <IconButton 
                  color="error" 
                  onClick={stopSpeaking}
                >
                  <StopIcon />
                </IconButton>
              </Tooltip>
            )}
          </Box>
          
          {/* Send Button */}
          <Button
            variant="contained"
            onClick={() => handleSubmit()}
            disabled={!input.trim() || isProcessing}
            startIcon={isProcessing ? <CircularProgress size={20} /> : <RecordIcon />}
          >
            {isProcessing ? 'Processing...' : 'Send'}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default VoiceEnabledAIChat;
