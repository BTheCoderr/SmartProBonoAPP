import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  Heading,
  Text,
  SimpleGrid,
  Card,
  CardHeader,
  CardBody,
  Flex,
  Icon,
  Divider,
  Button,
  useColorModeValue,
  VStack,
  Tab,
  Tabs,
  TabList,
  TabPanel,
  TabPanels,
  FormControl,
  FormLabel,
  Switch,
  Select,
  Progress,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  CloseButton,
  Link,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatGroup,
} from '@chakra-ui/react';
import {
  FaUniversalAccess,
  FaGlobe,
  FaLowVision,
  FaWifi,
  FaKeyboard,
  FaInfoCircle,
  FaCheck,
  FaBalanceScale,
  FaChevronRight,
  FaHome,
  FaEye,
} from 'react-icons/fa';

// Import custom components
import LanguageSelector from '../components/LanguageSelector';
import BandwidthModeSelector from '../components/BandwidthModeSelector';

const AccessibilityPage = () => {
  const { t } = useTranslation();
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const highlightColor = useColorModeValue('blue.50', 'blue.900');
  const legalAssistanceBg = useColorModeValue('green.50', 'green.900');

  // State for screen reader settings
  const [screenReaderEnabled, setScreenReaderEnabled] = useState(false);
  const [highContrastMode, setHighContrastMode] = useState(false);
  const [textSize, setTextSize] = useState('medium');
  const [keyboardNavigation, setKeyboardNavigation] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);

  // Implementation status for features
  const [showImplementationStatus, setShowImplementationStatus] = useState(true);

  // Usage statistics (would be fetched from backend in production)
  const usageStats = {
    totalAccessibilityUsers: 278,
    screenReaderUsers: 94,
    lowBandwidthUsers: 156,
    multilingualUsers: 203,
    lastUpdated: new Date().toISOString(),
  };

  const handleApplySettings = useCallback((
    textSizeValue = textSize,
    highContrastValue = highContrastMode,
    reducedMotionValue = reducedMotion
  ) => {
    // Apply text size
    document.documentElement.style.fontSize = 
      textSizeValue === 'small' ? '14px' : 
      textSizeValue === 'large' ? '18px' : '16px';

    // Apply high contrast
    document.body.classList.toggle('high-contrast', highContrastValue);

    // Apply reduced motion
    document.body.classList.toggle('reduce-motion', reducedMotionValue);

    // Save settings to localStorage
    localStorage.setItem('text-size', textSizeValue);
    localStorage.setItem('high-contrast', highContrastValue);
    localStorage.setItem('reduced-motion', reducedMotionValue);
  }, [textSize, highContrastMode, reducedMotion]);

  useEffect(() => {
    // Load user preferences from localStorage
    const savedTextSize = localStorage.getItem('text-size');
    const savedHighContrast = localStorage.getItem('high-contrast') === 'true';
    const savedReducedMotion = localStorage.getItem('reduced-motion') === 'true';

    if (savedTextSize) setTextSize(savedTextSize);
    if (savedHighContrast !== null) setHighContrastMode(savedHighContrast);
    if (savedReducedMotion !== null) setReducedMotion(savedReducedMotion);

    // Apply saved settings
    setTimeout(() => {
      handleApplySettings(savedTextSize, savedHighContrast, savedReducedMotion);
    }, 100);
  }, [handleApplySettings]);

  const features = [
    {
      title: 'Screen Reader Support',
      icon: FaLowVision,
      description:
        'ARIA attributes and semantic HTML improve screen reader navigation and understanding',
      implemented: 80,
    },
    {
      title: 'Multilingual Support',
      icon: FaGlobe,
      description: 'Multiple languages including RTL support for inclusive global access',
      implemented: 90,
    },
    {
      title: 'Low Bandwidth Mode',
      icon: FaWifi,
      description: 'Data-saving mode for users with limited internet connectivity',
      implemented: 85,
    },
    {
      title: 'Keyboard Navigation',
      icon: FaKeyboard,
      description: 'Full keyboard support for all interface elements without requiring a mouse',
      implemented: 75,
    },
    {
      title: 'High Contrast Mode',
      icon: FaLowVision,
      description: 'Enhanced visual contrast for users with vision impairments',
      implemented: 70,
    },
    {
      title: 'Text Scaling',
      icon: FaLowVision,
      description: 'Adjustable text size without breaking layout or functionality',
      implemented: 80,
    },
  ];

  // Legal services specifically designed for accessibility
  const legalAssistanceServices = [
    {
      title: 'Emergency Legal Support',
      description:
        'Accessible emergency legal help with screen reader support and simplified interfaces',
      link: '/emergency-legal-support',
    },
    {
      title: 'Case Management',
      description:
        'Track your cases with accessibility-enhanced interfaces and multiple communication options',
      link: '/cases',
    },
    {
      title: 'Legal Document Generator',
      description:
        'Create legal documents with step-by-step guided processes optimized for all users',
      link: '/document-generator',
    },
    {
      title: 'Safety Monitoring',
      description:
        'Enhanced safety features with accessible alerts and multiple notification methods',
      link: '/cases',
    },
  ];

  return (
    <Container maxW="container.xl" py={8}>
      {/* Hidden live region for announcements */}
      <div id="settings-announcement" aria-live="polite" className="sr-only"></div>

      {/* Breadcrumb Navigation */}
      <Breadcrumb mb={6} fontSize="sm" separator={<Icon as={FaChevronRight} color="gray.500" />}>
        <BreadcrumbItem>
          <BreadcrumbLink as={RouterLink} to="/" aria-label={t('Home')}>
            <Icon as={FaHome} aria-hidden="true" />
          </BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbItem isCurrentPage>
          <BreadcrumbLink href="#" aria-current="page">
            {t('accessibility_title')}
          </BreadcrumbLink>
        </BreadcrumbItem>
      </Breadcrumb>

      <Box
        mb={8}
        p={6}
        borderRadius="lg"
        bg={highlightColor}
        role="region"
        aria-labelledby="accessibility-title"
      >
        <Flex align="center" mb={4}>
          <Icon as={FaUniversalAccess} boxSize={8} mr={4} aria-hidden="true" />
          <Box>
            <Heading id="accessibility-title" as="h1" size="xl" mb={2}>
              {t('accessibility_title')}
            </Heading>
            <Text fontSize="lg">
              {t('Our commitment to making legal services accessible to everyone')}
            </Text>
          </Box>
        </Flex>

        <Text>
          {t(
            'The SmartProBono application is designed with accessibility as a core principle. Our goal is to ensure that all users, regardless of their abilities or circumstances, can access essential legal services and information.'
          )}
        </Text>
      </Box>

      {/* Usage Statistics */}
      <StatGroup
        mb={8}
        p={4}
        borderRadius="lg"
        bg={cardBg}
        borderColor={borderColor}
        borderWidth="1px"
        aria-labelledby="usage-stats-heading"
      >
        <Heading as="h2" size="md" id="usage-stats-heading" mb={4}>
          {t('Accessibility Usage')}
        </Heading>

        <SimpleGrid columns={{ base: 1, sm: 2, md: 4 }} spacing={4} width="100%">
          <Stat>
            <StatLabel>{t('Accessibility Users')}</StatLabel>
            <StatNumber>{usageStats.totalAccessibilityUsers}</StatNumber>
            <StatHelpText>{t('Active this month')}</StatHelpText>
          </Stat>

          <Stat>
            <StatLabel>{t('Screen Reader Users')}</StatLabel>
            <StatNumber>{usageStats.screenReaderUsers}</StatNumber>
            <StatHelpText>{t('Active this month')}</StatHelpText>
          </Stat>

          <Stat>
            <StatLabel>{t('Low Bandwidth Users')}</StatLabel>
            <StatNumber>{usageStats.lowBandwidthUsers}</StatNumber>
            <StatHelpText>{t('Active this month')}</StatHelpText>
          </Stat>

          <Stat>
            <StatLabel>{t('Multilingual Users')}</StatLabel>
            <StatNumber>{usageStats.multilingualUsers}</StatNumber>
            <StatHelpText>{t('Non-English users')}</StatHelpText>
          </Stat>
        </SimpleGrid>
      </StatGroup>

      {showImplementationStatus && (
        <Alert status="info" mb={8} borderRadius="md" role="alert">
          <AlertIcon />
          <Box flex="1">
            <AlertTitle>{t('Implementation Status')}</AlertTitle>
            <AlertDescription display="block">
              {t(
                "This page showcases the accessibility features we've added to the application. Some features are fully implemented, while others are in progress."
              )}
            </AlertDescription>
          </Box>
          <CloseButton
            position="absolute"
            right="8px"
            top="8px"
            onClick={() => setShowImplementationStatus(false)}
            aria-label={t('Close implementation status message')}
          />
        </Alert>
      )}

      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} mb={10}>
        {features.map((feature, index) => (
          <Card
            key={index}
            borderColor={borderColor}
            bg={cardBg}
            role="region"
            aria-labelledby={`feature-title-${index}`}
          >
            <CardHeader>
              <Flex align="center">
                <Icon as={feature.icon} boxSize={6} mr={3} aria-hidden="true" />
                <Heading size="md" id={`feature-title-${index}`}>
                  {t(feature.title)}
                </Heading>
              </Flex>
            </CardHeader>
            <CardBody>
              <Text mb={4}>{t(feature.description)}</Text>
              <Flex align="center">
                <Text fontSize="sm" fontWeight="bold" mr={2}>
                  {t('Implementation')}: {feature.implemented}%
                </Text>
                <Progress
                  value={feature.implemented}
                  size="sm"
                  colorScheme={
                    feature.implemented >= 80
                      ? 'green'
                      : feature.implemented >= 60
                        ? 'yellow'
                        : 'red'
                  }
                  flex="1"
                  borderRadius="full"
                  aria-label={`${feature.title} is ${feature.implemented}% implemented`}
                />
              </Flex>
            </CardBody>
          </Card>
        ))}
      </SimpleGrid>

      {/* Legal Assistance Services section */}
      <Box
        mb={8}
        p={6}
        borderRadius="lg"
        bg={legalAssistanceBg}
        role="region"
        aria-labelledby="legal-assistance-title"
      >
        <Heading as="h2" id="legal-assistance-title" size="lg" mb={4}>
          <Flex align="center">
            <Icon as={FaBalanceScale} mr={3} aria-hidden="true" />
            {t('Accessible Legal Assistance')}
          </Flex>
        </Heading>

        <Text mb={6}>
          {t(
            'Our Pro Bono application offers specialized legal services designed to be accessible to everyone, including people with disabilities, those with limited internet connectivity, and speakers of multiple languages.'
          )}
        </Text>

        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          {legalAssistanceServices.map((service, index) => (
            <Card key={index} bg={cardBg} role="region" aria-labelledby={`service-title-${index}`}>
              <CardHeader>
                <Heading size="md" id={`service-title-${index}`}>
                  {t(service.title)}
                </Heading>
              </CardHeader>
              <CardBody>
                <Text mb={4}>{t(service.description)}</Text>
                <Button
                  as={RouterLink}
                  to={service.link}
                  colorScheme="blue"
                  size="sm"
                  rightIcon={<Icon as={FaChevronRight} />}
                  aria-label={`${t('Access')} ${t(service.title)}`}
                >
                  {t('Access Service')}
                </Button>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>
      </Box>

      <Tabs isLazy colorScheme="blue" variant="enclosed">
        <TabList>
          <Tab aria-label={t('Screen Reader Settings')}>
            <Flex align="center">
              <Icon as={FaLowVision} mr={2} aria-hidden="true" />
              <Text>{t('Screen Reader')}</Text>
            </Flex>
          </Tab>
          <Tab aria-label={t('Language Settings')}>
            <Flex align="center">
              <Icon as={FaGlobe} mr={2} aria-hidden="true" />
              <Text>{t('Language')}</Text>
            </Flex>
          </Tab>
          <Tab aria-label={t('Bandwidth Settings')}>
            <Flex align="center">
              <Icon as={FaWifi} mr={2} aria-hidden="true" />
              <Text>{t('Bandwidth')}</Text>
            </Flex>
          </Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <Card bg={cardBg} borderColor={borderColor}>
              <CardHeader>
                <Heading size="md">{t('Screen Reader & Visual Settings')}</Heading>
              </CardHeader>
              <CardBody>
                <VStack spacing={6} align="stretch">
                  <FormControl display="flex" alignItems="center">
                    <FormLabel htmlFor="screen-reader-mode" mb="0" id="screen-reader-label">
                      {t('Enable screen reader optimizations')}
                    </FormLabel>
                    <Switch
                      id="screen-reader-mode"
                      isChecked={screenReaderEnabled}
                      onChange={e => setScreenReaderEnabled(e.target.checked)}
                      colorScheme="green"
                      aria-labelledby="screen-reader-label"
                    />
                  </FormControl>

                  <FormControl display="flex" alignItems="center">
                    <FormLabel htmlFor="high-contrast-mode" mb="0" id="contrast-label">
                      {t('High contrast mode')}
                    </FormLabel>
                    <Switch
                      id="high-contrast-mode"
                      isChecked={highContrastMode}
                      onChange={e => setHighContrastMode(e.target.checked)}
                      colorScheme="green"
                      aria-labelledby="contrast-label"
                    />
                  </FormControl>

                  <FormControl>
                    <FormLabel htmlFor="text-size" id="text-size-label">
                      {t('Text size')}
                    </FormLabel>
                    <Select
                      id="text-size"
                      value={textSize}
                      onChange={e => setTextSize(e.target.value)}
                      aria-labelledby="text-size-label"
                    >
                      <option value="small">{t('Small')}</option>
                      <option value="medium">{t('Medium')}</option>
                      <option value="large">{t('Large')}</option>
                    </Select>
                  </FormControl>

                  <FormControl display="flex" alignItems="center">
                    <FormLabel htmlFor="keyboard-navigation" mb="0" id="keyboard-label">
                      {t('Enhanced keyboard navigation')}
                    </FormLabel>
                    <Switch
                      id="keyboard-navigation"
                      isChecked={keyboardNavigation}
                      onChange={e => setKeyboardNavigation(e.target.checked)}
                      colorScheme="green"
                      aria-labelledby="keyboard-label"
                    />
                  </FormControl>

                  <FormControl display="flex" alignItems="center">
                    <FormLabel htmlFor="reduced-motion" mb="0" id="motion-label">
                      {t('Reduced motion')}
                    </FormLabel>
                    <Switch
                      id="reduced-motion"
                      isChecked={reducedMotion}
                      onChange={e => setReducedMotion(e.target.checked)}
                      colorScheme="green"
                      aria-labelledby="motion-label"
                    />
                  </FormControl>

                  <Button
                    onClick={() => handleApplySettings()}
                    colorScheme="blue"
                    leftIcon={<FaCheck />}
                    aria-label={t('Apply accessibility settings')}
                  >
                    {t('Apply Settings')}
                  </Button>
                </VStack>
              </CardBody>
            </Card>
          </TabPanel>

          <TabPanel>
            <Card bg={cardBg} borderColor={borderColor}>
              <CardHeader>
                <Heading size="md">{t('Language Settings')}</Heading>
              </CardHeader>
              <CardBody>
                <Box mb={6}>
                  <Text mb={4}>{t('Select your preferred language:')}</Text>
                  <LanguageSelector showText={true} size="lg" variant="outline" />
                </Box>

                <Divider my={6} />

                <Text fontSize="sm" color="gray.500" mb={4}>
                  <Icon as={FaInfoCircle} mr={2} aria-hidden="true" />
                  {t('Language selection is saved and applied across the entire application.')}
                </Text>

                <Alert status="success" variant="left-accent" mt={4}>
                  <AlertIcon />
                  <Box>
                    <AlertTitle>{t('New languages added!')}</AlertTitle>
                    <AlertDescription>
                      {t(
                        "We've recently added Hindi, Russian, Portuguese, Swahili, and Ukrainian language support."
                      )}
                    </AlertDescription>
                  </Box>
                </Alert>
              </CardBody>
            </Card>
          </TabPanel>

          <TabPanel>
            <Card bg={cardBg} borderColor={borderColor}>
              <CardHeader>
                <Heading size="md">{t('Bandwidth Settings')}</Heading>
              </CardHeader>
              <CardBody>
                <BandwidthModeSelector />
              </CardBody>
            </Card>
          </TabPanel>
        </TabPanels>
      </Tabs>

      {/* Accessibility Commitment */}
      <Box mt={10} p={6} borderRadius="lg" bg={cardBg} borderColor={borderColor} borderWidth="1px">
        <Heading as="h2" size="md" mb={4}>
          <Flex align="center">
            <Icon as={FaEye} mr={2} aria-hidden="true" />
            {t('Our Accessibility Commitment')}
          </Flex>
        </Heading>

        <Text mb={4}>
          {t(
            'We are committed to maintaining WCAG 2.1 AA standards across our entire platform. If you encounter any accessibility issues or have suggestions for improvement, please contact our support team.'
          )}
        </Text>

        <Link as={RouterLink} to="/contact" color="blue.500" fontWeight="medium">
          {t('Contact Support About Accessibility')}
        </Link>
      </Box>
    </Container>
  );
};

export default AccessibilityPage;
