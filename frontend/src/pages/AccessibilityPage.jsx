import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Switch,
  FormControlLabel,
  Slider,
  useTheme,
  Card,
  CardContent,
  Grid,
} from '@mui/material';
import { useTranslation } from 'react-i18next';

const AccessibilityPage = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const [settings, setSettings] = useState({
    screenReader: false,
    highContrast: false,
    textSize: 1,
    reduceMotion: false,
    keyboardNav: false,
  });

  const handleSettingChange = (setting) => (event) => {
    const value = event.target.checked ?? event.target.value;
    setSettings((prev) => ({
      ...prev,
      [setting]: value,
    }));
    
    // Apply settings to document
    if (setting === 'highContrast') {
      document.body.classList.toggle('high-contrast', value);
    } else if (setting === 'reduceMotion') {
      document.body.classList.toggle('reduce-motion', value);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper 
        elevation={3} 
        sx={{ 
          p: 4,
          backgroundColor: theme.palette.background.paper,
          borderRadius: 2
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom color="primary">
          {t('accessibility.options')}
        </Typography>

        <Typography variant="body1" paragraph sx={{ mb: 4 }}>
          {t('Our commitment to making legal services accessible to everyone')}
        </Typography>

        <Grid container spacing={3}>
          {/* Screen Reader Settings */}
          <Grid item xs={12} md={6}>
            <Card raised sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {t('accessibility.screenReader.enable')}
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.screenReader}
                      onChange={handleSettingChange('screenReader')}
                      color="primary"
                    />
                  }
                  label={t('accessibility.screenReader.description')}
                />
              </CardContent>
            </Card>
          </Grid>

          {/* High Contrast Settings */}
          <Grid item xs={12} md={6}>
            <Card raised sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {t('accessibility.contrast.high')}
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.highContrast}
                      onChange={handleSettingChange('highContrast')}
                      color="primary"
                    />
                  }
                  label={t('accessibility.contrast.description')}
                />
              </CardContent>
            </Card>
          </Grid>

          {/* Text Size Settings */}
          <Grid item xs={12}>
            <Card raised>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {t('accessibility.textSize.title')}
                </Typography>
                <Box sx={{ px: 2, py: 1 }}>
                  <Slider
                    value={settings.textSize}
                    onChange={handleSettingChange('textSize')}
                    min={0.8}
                    max={1.4}
                    step={0.1}
                    marks={[
                      { value: 0.8, label: t('accessibility.textSize.small') },
                      { value: 1, label: t('accessibility.textSize.medium') },
                      { value: 1.4, label: t('accessibility.textSize.large') },
                    ]}
                    valueLabelDisplay="auto"
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Motion Settings */}
          <Grid item xs={12} md={6}>
            <Card raised sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {t('accessibility.motion.reduce')}
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.reduceMotion}
                      onChange={handleSettingChange('reduceMotion')}
                      color="primary"
                    />
                  }
                  label={t('accessibility.motion.description')}
                />
              </CardContent>
            </Card>
          </Grid>

          {/* Keyboard Navigation Settings */}
          <Grid item xs={12} md={6}>
            <Card raised sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {t('accessibility.keyboard.enable')}
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.keyboardNav}
                      onChange={handleSettingChange('keyboardNav')}
                      color="primary"
                    />
                  }
                  label={t('accessibility.keyboard.description')}
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AccessibilityPage; 