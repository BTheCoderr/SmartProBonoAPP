/**
 * Voice Service for Mobile App
 * Handles voice input/output and speech processing
 */

import Voice from 'react-native-voice';
import Tts from 'react-native-tts';
import { PermissionsAndroid, Platform } from 'react-native';

export class VoiceService {
  private static instance: VoiceService;
  private isListening = false;
  private isSpeaking = false;
  private onResult?: (text: string) => void;
  private onError?: (error: string) => void;

  static getInstance(): VoiceService {
    if (!VoiceService.instance) {
      VoiceService.instance = new VoiceService();
    }
    return VoiceService.instance;
  }

  async initialize(): Promise<void> {
    try {
      // Request microphone permission
      if (Platform.OS === 'android') {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
          {
            title: 'Microphone Permission',
            message: 'SmartProBono needs access to your microphone for voice features.',
            buttonNeutral: 'Ask Me Later',
            buttonNegative: 'Cancel',
            buttonPositive: 'OK',
          }
        );
        if (granted !== PermissionsAndroid.RESULTS.GRANTED) {
          throw new Error('Microphone permission denied');
        }
      }

      // Initialize TTS
      await Tts.setDefaultLanguage('en-US');
      await Tts.setDefaultRate(0.5);
      await Tts.setDefaultPitch(1.0);

      // Set up voice recognition event handlers
      Voice.onSpeechStart = this.onSpeechStart;
      Voice.onSpeechEnd = this.onSpeechEnd;
      Voice.onSpeechResults = this.onSpeechResults;
      Voice.onSpeechError = this.onSpeechError;

    } catch (error) {
      console.error('Voice service initialization error:', error);
      throw error;
    }
  }

  private onSpeechStart = () => {
    this.isListening = true;
    console.log('Speech recognition started');
  };

  private onSpeechEnd = () => {
    this.isListening = false;
    console.log('Speech recognition ended');
  };

  private onSpeechResults = (e: any) => {
    if (e.value && e.value.length > 0) {
      const text = e.value[0];
      this.onResult?.(text);
    }
  };

  private onSpeechError = (e: any) => {
    this.isListening = false;
    const error = e.error?.message || 'Speech recognition error';
    this.onError?.(error);
  };

  async startListening(
    onResult: (text: string) => void,
    onError: (error: string) => void
  ): Promise<void> {
    try {
      this.onResult = onResult;
      this.onError = onError;
      
      await Voice.start('en-US');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      onError(errorMessage);
    }
  }

  async stopListening(): Promise<void> {
    try {
      await Voice.stop();
      this.isListening = false;
    } catch (error) {
      console.error('Error stopping voice recognition:', error);
    }
  }

  async speak(text: string, options?: {
    language?: string;
    rate?: number;
    pitch?: number;
  }): Promise<void> {
    try {
      if (options?.language) {
        await Tts.setDefaultLanguage(options.language);
      }
      if (options?.rate) {
        await Tts.setDefaultRate(options.rate);
      }
      if (options?.pitch) {
        await Tts.setDefaultPitch(options.pitch);
      }

      await Tts.speak(text);
      this.isSpeaking = true;

      // Set up completion handler
      Tts.addEventListener('tts-finish', () => {
        this.isSpeaking = false;
      });

    } catch (error) {
      console.error('Error speaking text:', error);
      throw error;
    }
  }

  async stopSpeaking(): Promise<void> {
    try {
      await Tts.stop();
      this.isSpeaking = false;
    } catch (error) {
      console.error('Error stopping speech:', error);
    }
  }

  isCurrentlyListening(): boolean {
    return this.isListening;
  }

  isCurrentlySpeaking(): boolean {
    return this.isSpeaking;
  }

  async getAvailableLanguages(): Promise<string[]> {
    try {
      const languages = await Voice.getSupportedLanguages();
      return languages || [];
    } catch (error) {
      console.error('Error getting available languages:', error);
      return [];
    }
  }

  async getAvailableVoices(): Promise<any[]> {
    try {
      const voices = await Tts.voices();
      return voices || [];
    } catch (error) {
      console.error('Error getting available voices:', error);
      return [];
    }
  }

  async setVoice(voiceId: string): Promise<void> {
    try {
      await Tts.setDefaultVoice(voiceId);
    } catch (error) {
      console.error('Error setting voice:', error);
    }
  }

  async setLanguage(language: string): Promise<void> {
    try {
      await Tts.setDefaultLanguage(language);
    } catch (error) {
      console.error('Error setting language:', error);
    }
  }

  async setRate(rate: number): Promise<void> {
    try {
      await Tts.setDefaultRate(rate);
    } catch (error) {
      console.error('Error setting rate:', error);
    }
  }

  async setPitch(pitch: number): Promise<void> {
    try {
      await Tts.setDefaultPitch(pitch);
    } catch (error) {
      console.error('Error setting pitch:', error);
    }
  }

  // Process voice command with AI backend
  async processVoiceCommand(text: string): Promise<any> {
    try {
      const response = await fetch('http://localhost:3001/api/voice/command', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          user_id: 'mobile_user'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error processing voice command:', error);
      throw error;
    }
  }

  // Analyze voice input with AI
  async analyzeVoiceInput(text: string, context?: any): Promise<any> {
    try {
      const response = await fetch('http://localhost:3001/api/voice/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          context: context || {}
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error analyzing voice input:', error);
      throw error;
    }
  }

  // Convert text to speech with backend
  async synthesizeSpeech(text: string, options?: {
    language?: string;
    voice?: string;
    speed?: number;
    pitch?: number;
    volume?: number;
  }): Promise<string> {
    try {
      const response = await fetch('http://localhost:3001/api/voice/text-to-speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          language: options?.language || 'en-US',
          voice: options?.voice || 'default',
          speed: options?.speed || 1.0,
          pitch: options?.pitch || 1.0,
          volume: options?.volume || 0.8
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.audio_data; // Base64 encoded audio
    } catch (error) {
      console.error('Error synthesizing speech:', error);
      throw error;
    }
  }

  // Cleanup
  destroy(): void {
    Voice.destroy();
    Tts.stop();
  }
}
