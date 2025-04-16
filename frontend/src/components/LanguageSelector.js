import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Box,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Text,
  Icon,
  Flex,
  VisuallyHidden,
  useColorModeValue,
} from '@chakra-ui/react';
import { FaGlobe, FaCheck, FaChevronDown } from 'react-icons/fa';
import PropTypes from 'prop-types';

// Map of language codes to their display names and RTL status
const languages = {
  en: { name: 'English', nativeName: 'English', isRTL: false, flag: '🇺🇸' },
  es: { name: 'Spanish', nativeName: 'Español', isRTL: false, flag: '🇪🇸' },
  fr: { name: 'French', nativeName: 'Français', isRTL: false, flag: '🇫🇷' },
  zh: { name: 'Chinese', nativeName: '中文', isRTL: false, flag: '🇨🇳' },
  ar: { name: 'Arabic', nativeName: 'العربية', isRTL: true, flag: '🇸🇦' },
  // Add more languages as needed
  hi: { name: 'Hindi', nativeName: 'हिन्दी', isRTL: false, flag: '🇮🇳' },
  ru: { name: 'Russian', nativeName: 'Русский', isRTL: false, flag: '🇷🇺' },
  pt: { name: 'Portuguese', nativeName: 'Português', isRTL: false, flag: '🇵🇹' },
  sw: { name: 'Swahili', nativeName: 'Kiswahili', isRTL: false, flag: '🇰🇪' },
  uk: { name: 'Ukrainian', nativeName: 'Українська', isRTL: false, flag: '🇺🇦' },
};

const LanguageSelector = ({
  size = 'md',
  variant = 'ghost',
  showText = true,
  isCompact = false,
}) => {
  const { i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const currentLanguage = i18n.language || 'en';

  // Style variables based on theme
  const menuBg = useColorModeValue('white', 'gray.800');
  const menuHoverBg = useColorModeValue('gray.100', 'gray.700');
  const selectedBg = useColorModeValue('blue.50', 'blue.900');

  // Set document direction based on language RTL status
  React.useEffect(() => {
    const isRTL = languages[currentLanguage]?.isRTL || false;
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
    document.documentElement.lang = currentLanguage;

    // Store language preference
    localStorage.setItem('i18nextLng', currentLanguage);
  }, [currentLanguage]);

  const handleLanguageChange = langCode => {
    i18n.changeLanguage(langCode);
    setIsOpen(false);

    // Announce language change to screen readers
    const announcement = document.getElementById('language-change-announcement');
    if (announcement) {
      announcement.textContent = `Language changed to ${languages[langCode].name}`;
    }
  };

  return (
    <Box position="relative">
      {/* Hidden element for screen reader announcements */}
      <VisuallyHidden id="language-change-announcement" aria-live="assertive" />

      <Menu isOpen={isOpen} onClose={() => setIsOpen(false)} placement="bottom-end">
        <MenuButton
          as={Button}
          variant={variant}
          size={size}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Select language"
          leftIcon={<Icon as={FaGlobe} aria-hidden="true" />}
          rightIcon={!isCompact && <Icon as={FaChevronDown} aria-hidden="true" fontSize="xs" />}
          data-testid="language-selector-button"
        >
          {showText && !isCompact && (
            <Text fontSize={size === 'sm' ? 'xs' : 'sm'}>
              {languages[currentLanguage]?.nativeName || 'English'}
            </Text>
          )}
          {isCompact && (
            <Text fontSize="sm" aria-hidden="true">
              {languages[currentLanguage]?.flag}
            </Text>
          )}
        </MenuButton>

        <MenuList
          zIndex={1000}
          bg={menuBg}
          boxShadow="lg"
          borderRadius="md"
          maxH="60vh"
          overflowY="auto"
          aria-label="Language options"
        >
          {Object.keys(languages).map(langCode => {
            const lang = languages[langCode];
            const isSelected = currentLanguage === langCode;

            return (
              <MenuItem
                key={langCode}
                onClick={() => handleLanguageChange(langCode)}
                bg={isSelected ? selectedBg : 'transparent'}
                _hover={{ bg: menuHoverBg }}
                aria-current={isSelected ? 'true' : 'false'}
                role="option"
                position="relative"
                paddingEnd={isSelected ? '2.5rem' : undefined}
                data-testid={`language-option-${langCode}`}
              >
                <Flex align="center">
                  <Text fontSize="lg" aria-hidden="true" mr={2}>
                    {lang.flag}
                  </Text>
                  <Box>
                    <Text fontWeight={isSelected ? 'bold' : 'normal'}>{lang.nativeName}</Text>
                    {!isCompact && (
                      <Text fontSize="xs" color="gray.500">
                        {lang.name}
                      </Text>
                    )}
                  </Box>
                </Flex>

                {isSelected && (
                  <Icon
                    as={FaCheck}
                    position="absolute"
                    right={3}
                    color="green.500"
                    aria-hidden="true"
                  />
                )}
              </MenuItem>
            );
          })}
        </MenuList>
      </Menu>
    </Box>
  );
};


// Define PropTypes
LanguageSelector.propTypes = {
  /** TODO: Add description */
  size: PropTypes.any,
  /** TODO: Add description */
  variant: PropTypes.any,
  /** TODO: Add description */
  showText: PropTypes.any,
  /** TODO: Add description */
  isCompact: PropTypes.any,
};

export default LanguageSelector;
