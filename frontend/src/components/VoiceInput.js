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
    if ('webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = document.documentElement.lang || 'en-US';

      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('');
        onTranscript(transcript);
      };

      recognition.onerror = (event) => {
        setError(event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      setRecognition(recognition);
    }

    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, [onTranscript, setIsListening, recognition]);

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