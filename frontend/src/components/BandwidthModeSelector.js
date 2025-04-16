import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Box,
  Switch,
  FormControl,
  FormLabel,
  Text,
  Badge,
  HStack,
  Icon,
  Button,
  Flex,
  useColorModeValue,
  VisuallyHidden,
} from '@chakra-ui/react';
import { FaInfoCircle, FaWifi, FaSpinner } from 'react-icons/fa';
import PropTypes from 'prop-types';
/**
 * A component that allows users to toggle between normal and low bandwidth modes
 * for better accessibility in limited connectivity environments.
 */
const BandwidthModeSelector = ({ isCompact = false }) => {
  const { t, i18n } = useTranslation();
  const [isLowBandwidthMode, setLowBandwidthMode] = useState(false);
  const [isDetecting, setIsDetecting] = useState(false);
  const [lastChecked, setLastChecked] = useState(null);
  // Theme colors
  const infoBg = useColorModeValue('blue.50', 'blue.900');
  const infoColor = useColorModeValue('blue.700', 'blue.200');
  const badgeBg = useColorModeValue('gray.100', 'gray.700');
  // Ensure necessary languages are loaded
  useEffect(() => {
    const currentLang = i18n.language;
    // Preload the current language resources if not already loaded
    if (!i18n.hasResourceBundle(currentLang, 'translation')) {
      // Instead of using loadLanguageAsync, directly import the language file
      import(`../i18n/locales/${currentLang}.js`)
        .then(module => {
          i18n.addResourceBundle(currentLang, 'translation', module.default);
        })
        .catch(err => console.error(`Failed to load language: ${currentLang}`, err));
    }
  }, [i18n]);
  // Format the last checked time
  const formattedLastChecked = lastChecked
    ? new Intl.DateTimeFormat(undefined, {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
      }).format(lastChecked)
    : null;
  const handleToggle = () => {
    // Toggle the current mode
    setLowBandwidthMode(!isLowBandwidthMode);
    // Announce change to screen readers
    const announcementText = isLowBandwidthMode
      ? t('Low bandwidth mode disabled')
      : t('Low bandwidth mode enabled');
    const announcement = document.getElementById('bandwidth-mode-announcement');
    if (announcement) {
      announcement.textContent = announcementText;
    }
  };
  const handleManualCheck = e => {
    e.preventDefault();
    setIsDetecting(true);
    // Simulate network speed detection
    setTimeout(() => {
      setIsDetecting(false);
      setLastChecked(new Date());
    }, 1500);
    
    // Announce to screen readers
    const announcement = document.getElementById('bandwidth-mode-announcement');
    if (announcement) {
      announcement.textContent = t('Checking connection speed...');
    }
  };
  // Features enabled/disabled in low bandwidth mode
  const lowBandwidthFeatures = [
    { enabled: true, name: t('Text-based communication') },
    { enabled: true, name: t('Essential legal information') },
    { enabled: true, name: t('Case management') },
    { enabled: false, name: t('High-quality images') },
    { enabled: false, name: t('Animations and transitions') },
    { enabled: false, name: t('Auto-playing videos') },
    { enabled: false, name: t('Real-time updates') },
  ];
  return (
    <section aria-labelledby="bandwidth-settings-heading">
      <VisuallyHidden>
        <h2 id="bandwidth-settings-heading">{t('Bandwidth Settings')}</h2>
      </VisuallyHidden>
      {/* Hidden live region for screen reader announcements */}
      <VisuallyHidden aria-live="assertive" id="bandwidth-mode-announcement" />
      <FormControl
        display="flex"
        alignItems="center"
        mb={4}
        role="group"
        aria-labelledby="bandwidth-mode-label"
      >
        <FormLabel
          id="bandwidth-mode-label"
          htmlFor="bandwidth-toggle"
          mb="0"
          fontWeight="medium"
          cursor="pointer"
        >
          {isCompact ? null : (
            <HStack spacing={2}>
              <Text>{t('settings_low_bandwidth')}</Text>
              <Badge bg={badgeBg} fontSize="0.8em" role="status">
                {isLowBandwidthMode ? t('Enabled') : t('Disabled')}
              </Badge>
            </HStack>
          )}
        </FormLabel>
        <Switch
          id="bandwidth-toggle"
          isChecked={isLowBandwidthMode}
          onChange={handleToggle}
          colorScheme="green"
          size={isCompact ? 'md' : 'lg'}
          ml={isCompact ? 0 : 2}
          aria-label={
            isLowBandwidthMode ? t('Disable low bandwidth mode') : t('Enable low bandwidth mode')
          }
          aria-describedby="bandwidth-toggle-description"
        />
      </FormControl>
      {!isCompact && (
        <>
          <Box
            bg={infoBg}
            p={3}
            borderRadius="md"
            mb={4}
            color={infoColor}
            role="region"
            id="bandwidth-toggle-description"
            aria-label={t('Information about low bandwidth mode')}
          >
            <Flex align="flex-start">
              <Icon as={FaInfoCircle} mt={1} mr={2} aria-hidden="true" />
              <Box>
                <Text fontSize="sm">
                  {t(
                    'Low bandwidth mode reduces data usage and optimizes the application for slower internet connections. Some visual features will be simplified or disabled.'
                  )}
                </Text>
                {lastChecked && (
                  <Text fontSize="xs" mt={1} role="status">
                    {t('Last connection check')}: {formattedLastChecked}
                  </Text>
                )}
              </Box>
            </Flex>
          </Box>
          <Button
            leftIcon={isDetecting ? <FaSpinner className="fa-spin" /> : <FaWifi />}
            onClick={handleManualCheck}
            size="sm"
            isLoading={isDetecting}
            loadingText={t('Checking...')}
            mb={4}
            aria-label={t('Check connection speed')}
          >
            {t('Check connection speed')}
          </Button>
          <Box mt={4} role="region" aria-labelledby="bandwidth-features-heading">
            <Text fontSize="sm" fontWeight="medium" mb={2} id="bandwidth-features-heading">
              {t('Features in low bandwidth mode')}:
            </Text>
            <ul aria-label={t('Feature availability in low bandwidth mode')}>
              {lowBandwidthFeatures.map((feature, index) => (
                <li
                  key={index}
                  style={{
                    fontSize: '0.875rem',
                    color: feature.enabled
                      ? 'var(--chakra-colors-green-500)'
                      : 'var(--chakra-colors-red-500)',
                  }}
                >
                  {feature.name}: <span>{feature.enabled ? t('Available') : t('Limited')}</span>
                </li>
              ))}
            </ul>
          </Box>
        </>
      )}
    </section>
  );
};

// Define PropTypes
BandwidthModeSelector.propTypes = {
  /** Whether to display a compact version of the selector */
  isCompact: PropTypes.bool,
};

export default BandwidthModeSelector;