import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import { IconButton, Tooltip, CircularProgress, Alert, Snackbar } from '@mui/material';
import { Mic as MicIcon, MicOff as MicOffIcon } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

const VoiceInput = ({ onTranscript, isListening, setIsListening }) => {
  const { t } = useTranslation();
  const recognition = useRef(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window) {
      recognition.current = new window.webkitSpeechRecognition();
      recognition.current.continuous = true;
      recognition.current.interimResults = true;
      recognition.current.lang = document.documentElement.lang || 'en-US';

      recognition.current.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('');
        onTranscript(transcript);
      };

      recognition.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setError(event.error);
        setIsListening(false);
      };

      recognition.current.onend = () => {
        setIsListening(false);
      };
    }

    return () => {
      if (recognition.current) {
        recognition.current.stop();
      }
    };
  }, [onTranscript, setIsListening]);

  useEffect(() => {
    if (recognition.current) {
      if (isListening) {
        recognition.current.start();
      } else {
        recognition.current.stop();
      }
    }
  }, [isListening]);

  const handleToggle = () => {
    if (!recognition.current) {
      setError('browser_unsupported');
      return;
    }

    if (isListening) {
      recognition.current.stop();
    } else {
      setError(null);
      recognition.current.start();
      setIsListening(true);
    }
  };

  return (
    <>
      <Tooltip
        title={
          isListening ? t('accessibility.voiceInput.stop') : t('accessibility.voiceInput.start')
        }
      >
        <IconButton
          onClick={handleToggle}
          color={isListening ? 'error' : 'primary'}
          aria-label={
            isListening ? t('accessibility.voiceInput.stop') : t('accessibility.voiceInput.start')
          }
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

      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError(null)}>
        <Alert onClose={() => setError(null)} severity="error" sx={{ width: '100%' }}>
          {error === 'browser_unsupported'
            ? t('accessibility.voiceInput.error')
            : t('common.error')}
        </Alert>
      </Snackbar>
    </>
  );
};

VoiceInput.propTypes = {
  onTranscript: PropTypes.func.isRequired,
  isListening: PropTypes.bool.isRequired,
  setIsListening: PropTypes.func.isRequired,
};

export default VoiceInput;
