import React, { useState } from 'react';
import { useThemeContext } from '../contexts/ThemeContext';
import { useTranslation } from 'react-i18next';
import {
  Box,
  Container,
  Typography,
  Paper,
  Divider,
  FormControl,
  FormControlLabel,
  FormLabel,
  RadioGroup,
  Radio,
  Switch,
  Slider,
  Button,
  Grid,
  Card,
  CardContent,
  CardHeader,
  IconButton,
  Tooltip,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import TextIncreaseIcon from '@mui/icons-material/TextIncrease';
import TextDecreaseIcon from '@mui/icons-material/TextDecrease';
import LanguageSelector from '../components/LanguageSelector';
import Navigation from '../components/Navigation';
import NotificationPreferences from '../components/NotificationPreferences';
import { useColorModeValue } from '@chakra-ui/react';
import {
  FaGlobe,
  FaLowVision,
  FaWifi,
  FaUserCog,
  FaBell,
  FaLock,
  FaPalette,
  FaSave,
  FaUndo,
} from 'react-icons/fa';
import { Flex, VStack, Heading, Text, SimpleGrid, Icon } from '@chakra-ui/react';
import BandwidthModeSelector from '../components/BandwidthModeSelector';
import { useToast } from '@chakra-ui/react';

const SettingsPage = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const toast = useToast();
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  // Get theme settings from context
  const { mode, setMode, highContrast, setHighContrast, fontSize, setFontSize } = useThemeContext();

  // State for accessibility settings
  const [screenReaderMode, setScreenReaderMode] = useState(false);
  const [highContrastMode, setHighContrastMode] = useState(false);
  const [textSize, setTextSize] = useState('medium');
  const [reducedMotion, setReducedMotion] = useState(false);

  // State for notification settings
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [pushNotifications, setPushNotifications] = useState(true);
  const [smsNotifications, setSmsNotifications] = useState(false);

  const handleModeChange = event => {
    setMode(event.target.value);
  };

  const handleContrastChange = event => {
    setHighContrast(event.target.checked);
  };

  const handleFontSizeChange = event => {
    setFontSize(event.target.value);
  };

  // Handler for saving settings
  const handleSaveSettings = () => {
    // In a real app, we'd save to backend here

    // Apply high contrast mode
    if (highContrastMode) {
      document.body.classList.add('high-contrast');
    } else {
      document.body.classList.remove('high-contrast');
    }

    // Apply text size
    document.documentElement.style.setProperty(
      '--base-font-size',
      textSize === 'small' ? '0.9rem' : textSize === 'large' ? '1.2rem' : '1rem'
    );

    // Apply reduced motion
    if (reducedMotion) {
      document.body.classList.add('reduced-motion');
    } else {
      document.body.classList.remove('reduced-motion');
    }

    toast({
      title: t('settings_saved'),
      description: t('Your settings have been saved successfully.'),
      status: 'success',
      duration: 3000,
      isClosable: true,
      position: 'top-right',
    });
  };

  // Reset settings to defaults
  const handleResetSettings = () => {
    setScreenReaderMode(false);
    setHighContrastMode(false);
    setTextSize('medium');
    setReducedMotion(false);
    setEmailNotifications(true);
    setPushNotifications(true);
    setSmsNotifications(false);

    // Remove all applied accessibility classes
    document.body.classList.remove('high-contrast', 'reduced-motion');
    document.documentElement.style.setProperty('--base-font-size', '1rem');

    toast({
      title: t('settings_reset'),
      description: t('Your settings have been reset to defaults.'),
      status: 'info',
      duration: 3000,
      isClosable: true,
      position: 'top-right',
    });
  };

  return (
    <Box>
      <Navigation />
      <Container maxWidth="lg" sx={{ mt: 10, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {t('settings_title')}
        </Typography>

        <Grid container spacing={3}>
          {/* Language Settings */}
          <Grid item xs={12} md={6}>
            <Card elevation={2}>
              <CardHeader title={t('settings_language')} titleTypographyProps={{ variant: 'h6' }} />
              <Divider />
              <CardContent>
                <Typography variant="body1" paragraph>
                  {t('settings_language_description')}
                </Typography>

                <Box sx={{ mt: 2 }}>
                  <FormControl component="fieldset">
                    <FormLabel component="legend">{t('settings_select_language')}</FormLabel>
                    <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
                      <LanguageSelector variant="text" />
                    </Box>
                  </FormControl>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Theme Settings */}
          <Grid item xs={12} md={6}>
            <Card elevation={2}>
              <CardHeader title={t('settings_theme')} titleTypographyProps={{ variant: 'h6' }} />
              <Divider />
              <CardContent>
                <FormControl component="fieldset">
                  <FormLabel component="legend">{t('settings_theme_mode')}</FormLabel>
                  <RadioGroup
                    row
                    aria-label="theme mode"
                    name="theme-mode-group"
                    value={mode}
                    onChange={handleModeChange}
                  >
                    <FormControlLabel
                      value="light"
                      control={<Radio />}
                      label={
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <LightModeIcon sx={{ mr: 1 }} />
                          {t('settings_theme_light')}
                        </Box>
                      }
                    />
                    <FormControlLabel
                      value="dark"
                      control={<Radio />}
                      label={
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <DarkModeIcon sx={{ mr: 1 }} />
                          {t('settings_theme_dark')}
                        </Box>
                      }
                    />
                  </RadioGroup>
                </FormControl>
              </CardContent>
            </Card>
          </Grid>

          {/* Accessibility Settings */}
          <Grid item xs={12}>
            <Card elevation={2}>
              <CardHeader
                title={t('settings_accessibility')}
                titleTypographyProps={{ variant: 'h6' }}
                avatar={<AccessibilityNewIcon />}
              />
              <Divider />
              <CardContent>
                <Grid container spacing={4}>
                  <Grid item xs={12} md={6}>
                    <FormControl component="fieldset" sx={{ width: '100%' }}>
                      <FormControlLabel
                        control={
                          <Switch
                            checked={highContrast}
                            onChange={handleContrastChange}
                            name="highContrast"
                            color="primary"
                          />
                        }
                        label={t('settings_high_contrast')}
                      />
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        {t('settings_high_contrast_description')}
                      </Typography>
                    </FormControl>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <FormControl component="fieldset" sx={{ width: '100%' }}>
                      <FormLabel component="legend">{t('settings_font_size')}</FormLabel>
                      <RadioGroup
                        aria-label="font size"
                        name="font-size-group"
                        value={fontSize}
                        onChange={handleFontSizeChange}
                      >
                        <FormControlLabel
                          value="small"
                          control={<Radio />}
                          label={
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <TextDecreaseIcon sx={{ mr: 1 }} />
                              {t('settings_font_small')}
                            </Box>
                          }
                        />
                        <FormControlLabel
                          value="medium"
                          control={<Radio />}
                          label={t('settings_font_medium')}
                        />
                        <FormControlLabel
                          value="large"
                          control={<Radio />}
                          label={
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <TextIncreaseIcon sx={{ mr: 1 }} />
                              {t('settings_font_large')}
                            </Box>
                          }
                        />
                      </RadioGroup>
                    </FormControl>
                  </Grid>
                </Grid>

                <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => window.location.reload()}
                  >
                    {t('settings_apply_changes')}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Notification Settings */}
          <Grid item xs={12}>
            <Card elevation={2}>
              <CardHeader
                title="Notification Settings"
                titleTypographyProps={{ variant: 'h6' }}
                avatar={<FaBell />}
              />
              <Divider />
              <CardContent>
                <NotificationPreferences />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default SettingsPage;
