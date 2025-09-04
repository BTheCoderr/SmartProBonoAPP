import React, { useState, useEffect } from 'react';
import {
  IconButton,
  Tooltip,
  CircularProgress,
  Alert,
  Snackbar,
} from '@mui/material';
import { Mic as MicIcon, MicOff as MicOffIcon } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

const VoiceInput = ({ onTranscript, isListening, setIsListening }) => {
  const { t } = useTranslation();
  const [error, setError] = useState(null);
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    let recognitionInstance = null;
    
    if ('webkitSpeechRecognition' in window) {
      recognitionInstance = new window.webkitSpeechRecognition();
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = document.documentElement.lang || 'en-US';

      recognitionInstance.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('');
        onTranscript(transcript);
      };

      recognitionInstance.onerror = (event) => {
        setError(event.error);
        setIsListening(false);
      };

      recognitionInstance.onend = () => {
        setIsListening(false);
      };

      setRecognition(recognitionInstance);
    }

    return () => {
      if (recognitionInstance) {
        recognitionInstance.stop();
      }
    };
  }, [onTranscript, setIsListening]);

  const toggleListening = () => {
    if (!recognition) {
      setError('browser_unsupported');
      return;
    }

    if (isListening) {
      recognition.stop();
    } else {
      setError(null);
      recognition.start();
      setIsListening(true);
    }
  };

  return (
    <>
      <Tooltip title={isListening ? t('accessibility.voiceInput.stop') : t('accessibility.voiceInput.start')}>
        <IconButton
          onClick={toggleListening}
          color={isListening ? 'error' : 'primary'}
          aria-label={isListening ? t('accessibility.voiceInput.stop') : t('accessibility.voiceInput.start')}
        >
          {isListening ? (
            <>
              <MicIcon />
              <CircularProgress
                size={48}
                thickness={2}
                sx={{
                  position: 'absolute',
                  color: 'error.main',
                }}
              />
            </>
          ) : (
            <MicOffIcon />
          )}
        </IconButton>
      </Tooltip>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError(null)}
      >
        <Alert
          onClose={() => setError(null)}
          severity="error"
          sx={{ width: '100%' }}
        >
          {error === 'browser_unsupported'
            ? t('accessibility.voiceInput.error')
            : t('common.error')}
        </Alert>
      </Snackbar>
    </>
  );
};

export default VoiceInput; 