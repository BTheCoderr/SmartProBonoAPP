import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  Card,
  CardContent,
  Grid,
  Alert,
  CircularProgress,
  IconButton,
  Chip,
  Container,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import CallIcon from '@mui/icons-material/Call';
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver';
import SecurityIcon from '@mui/icons-material/Security';
import WarningIcon from '@mui/icons-material/Warning';
import InfoIcon from '@mui/icons-material/Info';
import MicIcon from '@mui/icons-material/Mic';
import VideocamIcon from '@mui/icons-material/Videocam';
import VideocamOffIcon from '@mui/icons-material/VideocamOff';
import MicOffIcon from '@mui/icons-material/MicOff';
import EmergencyLegalCallButton from '../components/EmergencyLegalCallButton';
import EmergencyLegalTriage from '../components/EmergencyLegalTriage';
import EmergencyLegalService from '../services/EmergencyLegalService';
import PhoneIcon from '@mui/icons-material/Phone';
import EmailIcon from '@mui/icons-material/Email';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import AccessTimeIcon from '@mui/icons-material/AccessTime';

const EmergencyLegalSupportPage = () => {
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState('start'); // start, triage, connecting, inCall
  const [isRecording, setIsRecording] = useState(false);
  const [triageData, setTriageData] = useState(null);
  const [callMetadata, setCallMetadata] = useState({
    startTime: null,
    duration: 0,
    caseNumber: null,
    initialized: false,
    error: null,
  });
  const [isMicEnabled, setIsMicEnabled] = useState(true);
  const [isCameraEnabled, setIsCameraEnabled] = useState(false);
  const jitsiContainerRef = useRef(null);
  const [jitsiApi, setJitsiApi] = useState(null);
  const [waitTimes, setWaitTimes] = useState({
    high: '1-3 minutes',
    medium: '5-10 minutes',
    low: '15-30 minutes',
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const emergencyContacts = [
    {
      title: 'Legal Aid Hotline',
      phone: '1-800-123-4567',
      hours: '24/7',
      description: 'Free legal advice for emergencies',
    },
    {
      title: 'Domestic Violence Support',
      phone: '1-800-799-7233',
      hours: '24/7',
      description: 'National Domestic Violence Hotline',
    },
    {
      title: 'Immigration Crisis Line',
      phone: '1-800-898-7180',
      hours: '9:00 AM - 5:00 PM EST',
      description: 'Emergency immigration assistance',
    },
  ];

  const legalResourceCenters = [
    {
      name: 'Downtown Legal Aid Center',
      address: '123 Main St, City, State 12345',
      phone: '(555) 123-4567',
      email: 'help@legalaid.org',
    },
    {
      name: 'Community Law Office',
      address: '456 Park Ave, City, State 12345',
      phone: '(555) 987-6543',
      email: 'support@communitylaw.org',
    },
  ];

  // Fetch availability data when the component mounts
  useEffect(() => {
    const fetchAvailability = async () => {
      try {
        setIsLoading(true);
        const availabilityData = await EmergencyLegalService.getAvailability();
        setWaitTimes(availabilityData.wait_times);
        setIsLoading(false);
      } catch (err) {
        console.error('Failed to fetch availability data:', err);
        setError('Failed to load current wait times. Please try again later.');
        setIsLoading(false);
      }
    };

    fetchAvailability();
  }, []);

  // Simulated data for urgency levels - in production this would come from a real service
  const urgencyLevels = {
    high: { waitTime: waitTimes.high, availableLawyers: 3 },
    medium: { waitTime: waitTimes.medium, availableLawyers: 5 },
    low: { waitTime: waitTimes.low, availableLawyers: 12 },
  };

  // When triageData is submitted, move to connecting state
  useEffect(() => {
    if (triageData) {
      const submitTriageData = async () => {
        setActiveStep('connecting');
        try {
          // Submit the triage data to the backend
          const response = await EmergencyLegalService.submitTriage(triageData);

          // Initialize the Jitsi Meet room with the data returned from the API
          setTimeout(() => {
            initializeJitsiMeet(response.room_info.room_name);
            setActiveStep('inCall');
            setCallMetadata(prev => ({
              ...prev,
              startTime: new Date(),
              caseNumber: response.case_id,
              initialized: true,
            }));
          }, 3000); // Simulate a brief connection delay
        } catch (err) {
          setError('Failed to connect to legal support. Please try again.');
          setActiveStep('start');
        }
      };

      submitTriageData();
    }
  }, [triageData, initializeJitsiMeet]);

  const handleCallEnd = useCallback(async () => {
    try {
      if (callMetadata.caseNumber) {
        await EmergencyLegalService.endCall(callMetadata.caseNumber);
      }

      if (jitsiApi) {
        jitsiApi.dispose();
      }

      const endTime = new Date();
      const duration = Math.floor((endTime - callMetadata.startTime) / 1000);

      setCallMetadata(prev => ({
        ...prev,
        duration,
      }));

      setActiveStep('summary');
    } catch (err) {
      setActiveStep('summary');
    }
  }, [callMetadata.caseNumber, callMetadata.startTime, jitsiApi]);

  // Wrap initializeJitsiMeet in useCallback
  const initializeJitsiMeet = useCallback(async (roomName) => {
    if (!jitsiContainerRef.current) {
      setCallMetadata(prev => ({
        ...prev,
        error: 'Video container not initialized'
      }));
      return;
    }

    try {
      const loadJitsiScript = () => {
        return new Promise((resolve, reject) => {
          const script = document.createElement('script');
          script.src = 'https://meet.jit.si/external_api.js';
          script.async = true;
          script.onload = () => resolve();
          script.onerror = () => reject(new Error('Failed to load Jitsi script'));
          document.body.appendChild(script);
        });
      };

      await loadJitsiScript();
      const domain = 'meet.jit.si';
      const options = {
        roomName: roomName,
        width: '100%',
        height: '600px',
        parentNode: jitsiContainerRef.current,
        interfaceConfigOverwrite: {
          TOOLBAR_BUTTONS: [
            'microphone', 'camera', 'closedcaptions', 'desktop', 
            'fullscreen', 'fodeviceselection', 'chat', 'recording',
            'livestreaming', 'etherpad', 'settings', 'raisehand',
            'videoquality', 'filmstrip', 'feedback', 'stats', 
            'shortcuts', 'tileview', 'download', 'help'
          ],
          SHOW_JITSI_WATERMARK: false,
          SHOW_WATERMARK_FOR_GUESTS: false,
        },
      };

      // @ts-ignore
      const api = new window.JitsiMeetExternalAPI(domain, options);
      setJitsiApi(api);
      setIsLoading(false);

      if (api) {
        api.addEventListeners({
          readyToClose: handleCallEnd,
          audioMuteStatusChanged: ({ muted }) => setIsMicEnabled(!muted),
          videoMuteStatusChanged: ({ muted }) => setIsCameraEnabled(!muted),
        });
      }
    } catch (err) {
      setCallMetadata(prev => ({
        ...prev,
        error: 'Failed to initialize video call. Please ensure you have granted necessary permissions.'
      }));
      setIsLoading(false);
    }
  }, [jitsiContainerRef, handleCallEnd]);

  const initCall = useCallback(async () => {
    if (!callMetadata.initialized) {
      await initializeJitsiMeet();
      setCallMetadata(prev => ({
        ...prev,
        initialized: true
      }));
    }
  }, [callMetadata.initialized, initializeJitsiMeet]);

  useEffect(() => {
    if (!callMetadata.initialized) {
      initCall();
    }
  }, [callMetadata.initialized, initCall]);

  const startEmergencyProcess = () => {
    setActiveStep('triage');
  };

  const handleMicToggle = () => {
    setIsMicEnabled(!isMicEnabled);
    if (jitsiApi) {
      jitsiApi.executeCommand('toggleAudio');
    }
  };

  const handleCameraToggle = () => {
    setIsCameraEnabled(!isCameraEnabled);
    if (jitsiApi) {
      jitsiApi.executeCommand('toggleVideo');
    }
  };

  const handleRecordingToggle = async () => {
    try {
      if (callMetadata.caseNumber) {
        // Toggle recording state via the API
        const action = isRecording ? 'stop' : 'start';
        await EmergencyLegalService.toggleRecording(callMetadata.caseNumber, action);
        setIsRecording(!isRecording);
      }
    } catch (err) {
      console.error('Error toggling recording:', err);
      // Maybe show an error toast/alert here
    }
  };

  const renderContent = () => {
    switch (activeStep) {
      case 'start':
        return (
          <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                {t('24/7 Emergency Legal Support')}
              </Typography>

              <Alert severity="warning" sx={{ mb: 3 }}>
                <Typography variant="body1">
                  {t(
                    'This service is for urgent legal situations only. For non-urgent matters, please use our regular legal chat.'
                  )}
                </Typography>
              </Alert>

              <Typography variant="body1" paragraph>
                {t('Use this service if you are:')}
              </Typography>

              <Box component="ul" sx={{ pl: 2 }}>
                <Typography component="li" variant="body1" paragraph>
                  {t('Currently being detained or questioned by police')}
                </Typography>
                <Typography component="li" variant="body1" paragraph>
                  {t('Facing an immediate eviction or housing emergency')}
                </Typography>
                <Typography component="li" variant="body1" paragraph>
                  {t('Experiencing an urgent immigration situation')}
                </Typography>
                <Typography component="li" variant="body1" paragraph>
                  {t('In any situation where immediate legal advice is needed')}
                </Typography>
              </Box>

              <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
                <EmergencyLegalCallButton onClick={startEmergencyProcess} />
              </Box>

              <Box sx={{ mt: 4 }}>
                <Typography variant="body2" color="text.secondary" align="center">
                  {isLoading ? (
                    <CircularProgress size={16} sx={{ mr: 1 }} />
                  ) : error ? (
                    t('Current wait time information unavailable')
                  ) : (
                    t('Current wait times:')
                  )}
                </Typography>
                {!isLoading && !error && (
                  <Box sx={{ display: 'flex', justifyContent: 'space-around', mt: 1 }}>
                    <Chip
                      label={`${t('High Priority')}: ${urgencyLevels.high.waitTime}`}
                      color="error"
                      size="small"
                    />
                    <Chip
                      label={`${t('Medium Priority')}: ${urgencyLevels.medium.waitTime}`}
                      color="warning"
                      size="small"
                    />
                    <Chip
                      label={`${t('Low Priority')}: ${urgencyLevels.low.waitTime}`}
                      color="success"
                      size="small"
                    />
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        );

      case 'triage':
        return <EmergencyLegalTriage onComplete={setTriageData} />;

      case 'connecting':
        return (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 3 }}>
              {t('Connecting you to an available legal advocate...')}
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
              {t('Based on your situation, your estimated wait time is')}{' '}
              {triageData?.urgency ? waitTimes[triageData.urgency] : '5-10 minutes'}
            </Typography>
            <Alert severity="info" sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
              <Typography variant="body2">
                {t(
                  'Please stay on this screen. You will be connected as soon as an advocate is available.'
                )}
              </Typography>
            </Alert>
          </Box>
        );

      case 'inCall':
        return (
          <Box sx={{ maxWidth: 800, mx: 'auto' }}>
            <Paper elevation={3} sx={{ mb: 2, p: 2 }}>
              <Grid container spacing={2} alignItems="center">
                <Grid item>
                  <Chip icon={<CallIcon />} label={t('Live Call')} color="error" />
                </Grid>
                <Grid item>
                  <Chip
                    icon={isRecording ? <RecordVoiceOverIcon /> : <InfoIcon />}
                    label={isRecording ? t('Recording') : t('Not Recording')}
                    color={isRecording ? 'error' : 'default'}
                  />
                </Grid>
                <Grid item>
                  <Chip icon={<SecurityIcon />} label={t('Encrypted')} color="primary" />
                </Grid>
                <Grid item xs />
                <Grid item>
                  <Typography variant="body2" color="text.secondary">
                    {t('Case')}: {callMetadata.caseNumber}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>

            <Paper
              elevation={3}
              sx={{
                height: 500,
                width: '100%',
                bgcolor: 'black',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
              ref={jitsiContainerRef}
            >
              {/* Jitsi Meet will be initialized here */}
              <Typography variant="h6" color="white">
                {callMetadata.error || t('Call in progress... Video feed would appear here in production.')}
              </Typography>
            </Paper>

            <Paper elevation={3} sx={{ mt: 2, p: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Box>
                  <IconButton
                    onClick={handleMicToggle}
                    color={isMicEnabled ? 'primary' : 'default'}
                  >
                    {isMicEnabled ? <MicIcon /> : <MicOffIcon />}
                  </IconButton>
                  <IconButton
                    onClick={handleCameraToggle}
                    color={isCameraEnabled ? 'primary' : 'default'}
                  >
                    {isCameraEnabled ? <VideocamIcon /> : <VideocamOffIcon />}
                  </IconButton>
                  <IconButton
                    onClick={handleRecordingToggle}
                    color={isRecording ? 'error' : 'default'}
                  >
                    <RecordVoiceOverIcon />
                  </IconButton>
                </Box>
                <Button
                  variant="contained"
                  color="error"
                  onClick={handleCallEnd}
                  startIcon={<CallIcon />}
                >
                  {t('End Call')}
                </Button>
              </Box>
            </Paper>
          </Box>
        );

      case 'summary':
        return (
          <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                {t('Call Summary')}
              </Typography>

              <Box sx={{ my: 3 }}>
                <Typography variant="body1">
                  {t('Case Number')}: {callMetadata.caseNumber}
                </Typography>
                <Typography variant="body1">
                  {t('Duration')}: {Math.floor(callMetadata.duration / 60)}m{' '}
                  {callMetadata.duration % 60}s
                </Typography>
                <Typography variant="body1">
                  {t('Recording')}: {isRecording ? t('Yes') : t('No')}
                </Typography>
              </Box>

              <Alert severity="info" sx={{ mb: 3 }}>
                <Typography variant="body1">
                  {t('A summary of this call has been saved to your case history.')}
                </Typography>
              </Alert>

              <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
                <Button variant="outlined" href="/profile/cases">
                  {t('View My Cases')}
                </Button>
                <Button variant="contained" color="primary" href="/legal-chat">
                  {t('Chat with Legal AI')}
                </Button>
              </Box>
            </CardContent>
          </Card>
        );

      default:
        return <Typography>{t('Unknown step')}</Typography>;
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Typography color="error" gutterBottom>
          {t('errors.videoConference')}
        </Typography>
        <Button variant="contained" onClick={() => window.location.reload()}>
          {t('common.retry')}
        </Button>
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Emergency Legal Support
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          Get immediate assistance for urgent legal matters
        </Typography>
      </Box>

      <Alert severity="warning" sx={{ mb: 4 }}>
        If you are in immediate danger, please call 911 or your local emergency number.
      </Alert>

      <Grid container spacing={4}>
        {/* Emergency Contacts Section */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                Emergency Contacts
              </Typography>
              <List>
                {emergencyContacts.map((contact, index) => (
                  <React.Fragment key={contact.title}>
                    <ListItem>
                      <ListItemIcon>
                        <PhoneIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={contact.title}
                        secondary={
                          <>
                            <Typography component="span" variant="body2" color="text.primary">
                              {contact.phone}
                            </Typography>
                            <br />
                            <Typography component="span" variant="body2">
                              <AccessTimeIcon sx={{ fontSize: 'small', mr: 0.5, verticalAlign: 'middle' }} />
                              {contact.hours}
                            </Typography>
                            <br />
                            {contact.description}
                          </>
                        }
                      />
                    </ListItem>
                    {index < emergencyContacts.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Legal Resource Centers Section */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                Legal Resource Centers
              </Typography>
              <List>
                {legalResourceCenters.map((center, index) => (
                  <React.Fragment key={center.name}>
                    <ListItem>
                      <ListItemText
                        primary={center.name}
                        secondary={
                          <Box>
                            <Typography component="div" variant="body2">
                              <LocationOnIcon sx={{ fontSize: 'small', mr: 0.5, verticalAlign: 'middle' }} />
                              {center.address}
                            </Typography>
                            <Typography component="div" variant="body2">
                              <PhoneIcon sx={{ fontSize: 'small', mr: 0.5, verticalAlign: 'middle' }} />
                              {center.phone}
                            </Typography>
                            <Typography component="div" variant="body2">
                              <EmailIcon sx={{ fontSize: 'small', mr: 0.5, verticalAlign: 'middle' }} />
                              {center.email}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < legalResourceCenters.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Additional Resources Section */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                Additional Resources
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Button
                    variant="contained"
                    color="primary"
                    fullWidth
                    href="/legal-chat"
                    startIcon={<WarningIcon />}
                  >
                    Start Emergency Chat
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Button
                    variant="outlined"
                    color="primary"
                    fullWidth
                    href="/resources/rights"
                  >
                    Know Your Rights
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ maxWidth: 1200, mx: 'auto', px: 2, py: 4 }}>{renderContent()}</Box>
    </Container>
  );
};

export default EmergencyLegalSupportPage;
