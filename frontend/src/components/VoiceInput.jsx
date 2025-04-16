import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { IconButton } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import MicOffIcon from '@mui/icons-material/MicOff';

const VoiceInput = ({ onTranscript, isListening, setIsListening }) => {
  const recognition = useRef(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window) {
      recognition.current = new window.webkitSpeechRecognition();
      recognition.current.continuous = true;
      recognition.current.interimResults = true;

      recognition.current.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0].transcript)
          .join('');
        onTranscript(transcript);
      };

      recognition.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      return () => {
        if (recognition.current) {
          recognition.current.stop();
        }
      };
    }
  }, [onTranscript, setIsListening]);

  const toggleListening = () => {
    if (isListening) {
      recognition.current?.stop();
    } else {
      recognition.current?.start();
    }
    setIsListening(!isListening);
  };

  if (!('webkitSpeechRecognition' in window)) {
    return null;
  }

  return (
    <IconButton onClick={toggleListening} color={isListening ? 'primary' : 'default'}>
      {isListening ? <MicIcon /> : <MicOffIcon />}
    </IconButton>
  );
};

VoiceInput.propTypes = {
  onTranscript: PropTypes.func.isRequired,
  isListening: PropTypes.bool.isRequired,
  setIsListening: PropTypes.func.isRequired
};

export default VoiceInput; 