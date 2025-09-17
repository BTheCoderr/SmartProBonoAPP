/**
 * Voice Chat Screen
 * Mobile voice-enabled AI chat interface
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Dimensions,
  Animated,
  Vibration
} from 'react-native';
import { Card, Button, IconButton, TextInput, Chip, FAB } from 'react-native-paper';
import { VoiceService } from '../services/VoiceService';
import { theme } from '../theme/theme';

const { width, height } = Dimensions.get('window');

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: string;
  type: 'text' | 'voice' | 'error';
}

export default function VoiceChatScreen({ navigation }: any) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const voiceService = VoiceService.getInstance();
  const scrollViewRef = useRef<ScrollView>(null);
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    // Initialize voice service
    voiceService.initialize().catch(console.error);
    
    // Add welcome message
    const welcomeMessage: Message = {
      id: '1',
      text: 'Hello! I\'m your AI legal assistant. You can speak to me or type your questions.',
      sender: 'assistant',
      timestamp: new Date().toLocaleTimeString(),
      type: 'text'
    };
    setMessages([welcomeMessage]);

    return () => {
      voiceService.destroy();
    };
  }, []);

  useEffect(() => {
    // Auto-scroll to bottom
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [messages]);

  useEffect(() => {
    // Pulse animation for listening state
    if (isListening) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.2,
            duration: 500,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 500,
            useNativeDriver: true,
          }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1);
    }
  }, [isListening]);

  const startListening = async () => {
    try {
      setError(null);
      await voiceService.startListening(
        (text) => {
          setInputText(text);
          handleSubmit(text);
        },
        (error) => {
          setError(error);
          setIsListening(false);
        }
      );
      setIsListening(true);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Unknown error');
    }
  };

  const stopListening = async () => {
    try {
      await voiceService.stopListening();
      setIsListening(false);
    } catch (error) {
      console.error('Error stopping listening:', error);
    }
  };

  const handleSubmit = async (text: string = inputText) => {
    if (!text.trim() || isProcessing) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: text,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString(),
      type: 'voice'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsProcessing(true);
    setError(null);

    try {
      // Process voice command
      const commandResult = await voiceService.processVoiceCommand(text);
      
      if (commandResult.success) {
        // Analyze with AI
        const analysisResult = await voiceService.analyzeVoiceInput(text);
        
        if (analysisResult.success) {
          const aiMessage: Message = {
            id: (Date.now() + 1).toString(),
            text: formatAIResponse(analysisResult.analysis),
            sender: 'assistant',
            timestamp: new Date().toLocaleTimeString(),
            type: 'text'
          };
          
          setMessages(prev => [...prev, aiMessage]);
          
          // Speak the response
          await speakText(aiMessage.text);
        } else {
          throw new Error(analysisResult.error || 'Analysis failed');
        }
      } else {
        throw new Error(commandResult.error || 'Command processing failed');
      }
    } catch (err) {
      console.error('Error processing message:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
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

  const speakText = async (text: string) => {
    try {
      await voiceService.speak(text);
      setIsSpeaking(true);
      
      // Set up completion handler
      setTimeout(() => {
        setIsSpeaking(false);
      }, text.length * 50); // Estimate speaking time
      
    } catch (error) {
      console.error('Error speaking text:', error);
    }
  };

  const stopSpeaking = async () => {
    try {
      await voiceService.stopSpeaking();
      setIsSpeaking(false);
    } catch (error) {
      console.error('Error stopping speech:', error);
    }
  };

  const formatAIResponse = (analysis: any): string => {
    if (!analysis) return 'I understand your question. How can I help you?';
    
    let response = '';
    
    if (analysis.case_summary) {
      response += `Analysis: ${analysis.case_summary}\n\n`;
    }
    
    if (analysis.key_facts && analysis.key_facts.length > 0) {
      response += `Key Facts:\n${analysis.key_facts.map((fact: string) => `• ${fact}`).join('\n')}\n\n`;
    }
    
    if (analysis.practical_advice && analysis.practical_advice.length > 0) {
      response += `Advice:\n${analysis.practical_advice.map((advice: string) => `• ${advice}`).join('\n')}\n\n`;
    }
    
    return response || 'I understand your question. Let me provide some guidance based on the information you\'ve shared.';
  };

  const clearChat = () => {
    Alert.alert(
      'Clear Chat',
      'Are you sure you want to clear the conversation?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Clear', 
          style: 'destructive',
          onPress: () => {
            setMessages([]);
            setError(null);
          }
        }
      ]
    );
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Voice Chat</Text>
        <View style={styles.headerControls}>
          <Chip 
            icon={isListening ? "mic" : isSpeaking ? "volume-up" : "mic-off"}
            mode="outlined"
            style={styles.statusChip}
          >
            {isListening ? "Listening" : isSpeaking ? "Speaking" : "Ready"}
          </Chip>
          <IconButton
            icon="delete"
            size={24}
            onPress={clearChat}
          />
        </View>
      </View>

      {/* Messages */}
      <ScrollView 
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
      >
        {messages.map((message) => (
          <View
            key={message.id}
            style={[
              styles.messageContainer,
              message.sender === 'user' ? styles.userMessage : styles.assistantMessage
            ]}
          >
            <Card style={[
              styles.messageCard,
              message.sender === 'user' ? styles.userCard : styles.assistantCard,
              message.type === 'error' && styles.errorCard
            ]}>
              <Card.Content>
                <Text style={[
                  styles.messageText,
                  message.sender === 'user' ? styles.userText : styles.assistantText
                ]}>
                  {message.text}
                </Text>
                <View style={styles.messageFooter}>
                  <Text style={styles.timestamp}>{message.timestamp}</Text>
                  {message.sender === 'assistant' && message.type !== 'error' && (
                    <TouchableOpacity
                      onPress={() => speakText(message.text)}
                      disabled={isSpeaking}
                    >
                      <IconButton
                        icon={isSpeaking ? "pause" : "volume-up"}
                        size={16}
                        iconColor={theme.colors.primary}
                      />
                    </TouchableOpacity>
                  )}
                </View>
              </Card.Content>
            </Card>
          </View>
        ))}
        
        {isProcessing && (
          <View style={styles.processingContainer}>
            <Card style={styles.processingCard}>
              <Card.Content>
                <Text style={styles.processingText}>AI is thinking...</Text>
              </Card.Content>
            </Card>
          </View>
        )}
      </ScrollView>

      {/* Error Display */}
      {error && (
        <Card style={styles.errorCard}>
          <Card.Content>
            <Text style={styles.errorText}>{error}</Text>
          </Card.Content>
        </Card>
      )}

      {/* Input Area */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.textInput}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type your message or use voice input..."
          multiline
          maxLength={500}
          disabled={isProcessing}
        />
        
        <View style={styles.inputControls}>
          {isListening ? (
            <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
              <IconButton
                icon="mic"
                size={32}
                iconColor="white"
                style={styles.listeningButton}
                onPress={stopListening}
              />
            </Animated.View>
          ) : (
            <IconButton
              icon="mic"
              size={32}
              iconColor="white"
              style={styles.micButton}
              onPress={startListening}
              disabled={isProcessing}
            />
          )}
          
          {isSpeaking && (
            <IconButton
              icon="stop"
              size={32}
              iconColor="white"
              style={styles.stopButton}
              onPress={stopSpeaking}
            />
          )}
          
          <Button
            mode="contained"
            onPress={() => handleSubmit()}
            disabled={!inputText.trim() || isProcessing}
            style={styles.sendButton}
          >
            Send
          </Button>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: theme.colors.primary,
    elevation: 4,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  headerControls: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusChip: {
    backgroundColor: 'white',
    marginRight: 8,
  },
  messagesContainer: {
    flex: 1,
    padding: 16,
  },
  messagesContent: {
    paddingBottom: 16,
  },
  messageContainer: {
    marginBottom: 12,
  },
  userMessage: {
    alignItems: 'flex-end',
  },
  assistantMessage: {
    alignItems: 'flex-start',
  },
  messageCard: {
    maxWidth: width * 0.8,
    elevation: 2,
  },
  userCard: {
    backgroundColor: theme.colors.primary,
  },
  assistantCard: {
    backgroundColor: theme.colors.surface,
  },
  errorCard: {
    backgroundColor: theme.colors.error,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 24,
  },
  userText: {
    color: 'white',
  },
  assistantText: {
    color: theme.colors.onSurface,
  },
  messageFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 8,
  },
  timestamp: {
    fontSize: 12,
    opacity: 0.7,
  },
  processingContainer: {
    alignItems: 'center',
    marginTop: 16,
  },
  processingCard: {
    backgroundColor: theme.colors.surface,
    elevation: 2,
  },
  processingText: {
    fontSize: 16,
    fontStyle: 'italic',
    color: theme.colors.onSurface,
  },
  errorText: {
    color: 'white',
    fontSize: 14,
  },
  inputContainer: {
    padding: 16,
    backgroundColor: theme.colors.surface,
    elevation: 8,
  },
  textInput: {
    marginBottom: 12,
    backgroundColor: 'white',
  },
  inputControls: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  micButton: {
    backgroundColor: theme.colors.primary,
    marginRight: 8,
  },
  listeningButton: {
    backgroundColor: theme.colors.error,
    marginRight: 8,
  },
  stopButton: {
    backgroundColor: theme.colors.error,
    marginRight: 8,
  },
  sendButton: {
    flex: 1,
  },
});
