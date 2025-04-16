import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Flex,
  Heading,
  Text,
  Button,
  IconButton,
  Tooltip,
  VStack,
  HStack,
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  useDisclosure,
  List,
  ListItem,
  Container,
  Badge,
  VisuallyHidden,
  useColorModeValue,
  Divider,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  Kbd,
} from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import {
  FaBookmark,
  FaList,
  FaSearch,
  FaPrint,
  FaDownload,
  FaHighlighter,
  FaCopy,
  FaVolumeUp,
  FaChevronLeft,
  FaChevronRight,
  FaHeading,
  FaParagraph,
  FaCog,
  FaFont,
  FaInfoCircle,
} from 'react-icons/fa';
import {
import PropTypes from 'prop-types';
  useFocusable,
  useFocusNavigation,
  useFocusAfterOperation,
  useFocusTrap,
} from '../utils/focusManager';
/**
 * LegalDocumentViewer Component
 *
 * A comprehensive legal document viewer with advanced accessibility features:
 * - Enhanced screen reader support with document structure navigation
 * - Focus management for keyboard navigation
 * - Text-to-speech functionality for document sections
 * - Document section annotations and descriptions
 * - Responsive design with mobile support
 */
const LegalDocumentViewer = ({ document, onBookmark, onPrint, onDownload, onClose }) => {
  const { t } = useTranslation();
  const { isOpen, onOpen, onClose: onDrawerClose } = useDisclosure();
  const [currentSection, setCurrentSection] = useState(0);
  const [textSize, setTextSize] = useState(16);
  const [highlights, setHighlights] = useState([]);
  const [bookmarks, setBookmarks] = useState([]);
  const [selectedText, setSelectedText] = useState('');
  const [announcement, setAnnouncement] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const contentRef = useRef(null);
  const speechSynthesis = window.speechSynthesis;
  const speechUtterance = useRef(null);
  // Focus management
  const documentViewerFocusGroupId = 'legal-document-viewer';
  const documentNavFocusGroupId = 'document-navigation';
  const documentToolbarFocusGroupId = 'document-toolbar';
  // Refs for key elements
  const mainHeadingRef = useRef(null);
  // Focus trap for drawer
  const {
    containerRef: drawerRef,
    isActive: drawerFocusTrapActive,
    activate: activateDrawerFocusTrap,
    deactivate: deactivateDrawerFocusTrap,
    handleKeyDown: handleDrawerKeyDown,
  } = useFocusTrap('document-structure-drawer');
  // Navigation controls focus management
  const {
    handleKeyDown: handleNavKeyDown,
    focusNext: focusNextNav,
    focusPrev: focusPrevNav,
  } = useFocusNavigation(documentNavFocusGroupId, {
    trapFocus: false,
    arrowKeyNavigation: true,
  });
  // Toolbar focus management
  const {
    handleKeyDown: handleToolbarKeyDown,
    focusNext: focusNextTool,
    focusPrev: focusPrevTool,
  } = useFocusNavigation(documentToolbarFocusGroupId, {
    trapFocus: false,
    arrowKeyNavigation: true,
  });
  // Register focusable elements
  const { ref: prevButtonRef } = useFocusable(documentNavFocusGroupId, 'prev-section-button', {
    order: 1,
  });
  const { ref: nextButtonRef } = useFocusable(documentNavFocusGroupId, 'next-section-button', {
    order: 2,
  });
  const { ref: tocButtonRef } = useFocusable(documentToolbarFocusGroupId, 'toc-button', {
    order: 1,
  });
  const { ref: searchButtonRef } = useFocusable(documentToolbarFocusGroupId, 'search-button', {
    order: 2,
  });
  const { ref: highlightButtonRef } = useFocusable(
    documentToolbarFocusGroupId,
    'highlight-button',
    { order: 3 }
  );
  const { ref: speakButtonRef } = useFocusable(documentToolbarFocusGroupId, 'speak-button', {
    order: 4,
  });
  const { ref: printButtonRef } = useFocusable(documentToolbarFocusGroupId, 'print-button', {
    order: 5,
  });
  const { ref: downloadButtonRef } = useFocusable(documentToolbarFocusGroupId, 'download-button', {
    order: 6,
  });
  const { ref: settingsButtonRef } = useFocusable(documentToolbarFocusGroupId, 'settings-button', {
    order: 7,
  });
  // Colors
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const sectionBgColor = useColorModeValue('gray.50', 'gray.900');
  // Process document structure for screen readers and navigation
  const processedSections =
    document?.sections?.map(section => ({
      ...section,
      // Create accessible description for screen readers
      accessibleDescription: `${section.type === 'heading' ? 'Section: ' : 'Paragraph: '}${section.content}`,
    })) || [];
  // Handle drawer open/close
  useEffect(() => {
    if (isOpen) {
      // Setup focus trap when drawer opens
      setTimeout(() => {
        activateDrawerFocusTrap();
      }, 100);
    } else {
      deactivateDrawerFocusTrap();
    }
  }, [isOpen, activateDrawerFocusTrap, deactivateDrawerFocusTrap]);
  // Make an announcement to screen readers
  const announce = (message, politeness = 'polite') => {
    setAnnouncement({ text: message, politeness });
  };
  // Navigation handlers
  const goToSection = sectionIndex => {
    if (sectionIndex >= 0 && sectionIndex < processedSections.length) {
      setCurrentSection(sectionIndex);
      // Announce section change
      const section = processedSections[sectionIndex];
      announce(
        `Navigated to ${section.type === 'heading' ? 'section' : 'paragraph'}: ${section.content}`
      );
      // Close drawer if open
      if (isOpen) {
        onDrawerClose();
      }
      // Set focus to the section heading or content
      setTimeout(() => {
        const sectionElement = document.getElementById(`section-${sectionIndex}`);
        if (sectionElement) {
          sectionElement.focus();
        }
      }, 100);
    }
  };
  const goToPrevSection = () => {
    goToSection(currentSection - 1);
  };
  const goToNextSection = () => {
    goToSection(currentSection + 1);
  };
  // Text selection handler
  const handleTextSelection = () => {
    const selection = window.getSelection();
    if (selection && selection.toString()) {
      setSelectedText(selection.toString());
    }
  };
  // Highlight selected text
  const highlightSelectedText = () => {
    if (selectedText) {
      setHighlights([...highlights, selectedText]);
      announce(`Highlighted text: ${selectedText}`);
    }
  };
  // Text-to-speech functionality
  const speakSection = (sectionIndex = currentSection) => {
    if (!speechSynthesis) {
      announce('Text-to-speech is not supported in your browser', 'assertive');
      return;
    }
    // Stop any current speech
    if (speechSynthesis.speaking) {
      speechSynthesis.cancel();
      setIsSpeaking(false);
      announce('Stopped reading');
      return;
    }
    const section = processedSections[sectionIndex];
    if (section) {
      speechUtterance.current = new SpeechSynthesisUtterance(section.content);
      speechUtterance.current.onend = () => {
        setIsSpeaking(false);
        announce('Finished reading section');
      };
      speechUtterance.current.onerror = () => {
        setIsSpeaking(false);
        announce('Error occurred while reading section', 'assertive');
      };
      // Start speaking
      speechSynthesis.speak(speechUtterance.current);
      setIsSpeaking(true);
      announce(`Reading section: ${section.type === 'heading' ? 'Heading' : 'Paragraph'}`);
    }
  };
  // Handle bookmark section
  const bookmarkSection = (sectionIndex = currentSection) => {
    if (!bookmarks.includes(sectionIndex)) {
      setBookmarks([...bookmarks, sectionIndex]);
      announce(`Bookmarked section ${sectionIndex + 1}`);
      if (onBookmark) {
        onBookmark(sectionIndex);
      }
    } else {
      setBookmarks(bookmarks.filter(b => b !== sectionIndex));
      announce(`Removed bookmark from section ${sectionIndex + 1}`);
    }
  };
  // Keyboard shortcut handler
  const handleKeyboardShortcuts = e => {
    // Global document viewer shortcuts
    if (e.altKey) {
      switch (e.key) {
        case 'ArrowLeft':
          e.preventDefault();
          goToPrevSection();
          break;
        case 'ArrowRight':
          e.preventDefault();
          goToNextSection();
          break;
        case 't':
          e.preventDefault();
          onOpen();
          break;
        case 's':
          e.preventDefault();
          speakSection();
          break;
        case 'b':
          e.preventDefault();
          bookmarkSection();
          break;
        case 'h':
          e.preventDefault();
          highlightSelectedText();
          break;
        case 'p':
          e.preventDefault();
          if (onPrint) onPrint();
          announce('Printing document');
          break;
        case 'd':
          e.preventDefault();
          if (onDownload) onDownload();
          announce('Downloading document');
          break;
        default:
          break;
      }
    }
  };
  // Listen for keyboard shortcuts
  useEffect(() => {
    document.addEventListener('keydown', handleKeyboardShortcuts);
    return () => {
      document.removeEventListener('keydown', handleKeyboardShortcuts);
    };
  }, [currentSection, selectedText, document, handleKeyboardShortcuts]);
  // Cleanup text-to-speech on unmount
  useEffect(() => {
    return () => {
      if (speechSynthesis && speechSynthesis.speaking) {
        speechSynthesis.cancel();
      }
    };
  }, [speechSynthesis]);
  // Focus the current section when it changes
  useEffect(() => {
    const sectionElement = document.getElementById(`section-${currentSection}`);
    if (sectionElement) {
      sectionElement.focus();
    }
  }, [currentSection, document]);
  // Initial focus when component mounts
  useEffect(() => {
    if (mainHeadingRef.current) {
      mainHeadingRef.current.focus();
    }
  }, []);
  return (
    <Box
      bg={bgColor}
      borderWidth="1px"
      borderColor={borderColor}
      borderRadius="lg"
      overflow="hidden"
      role="region"
      aria-labelledby="document-title"
      onMouseUp={handleTextSelection}
      position="relative"
    >
      {/* Screen reader announcements */}
      <VisuallyHidden aria-live={announcement.politeness || 'polite'} aria-atomic="true">
        {announcement.text}
      </VisuallyHidden>
      {/* Document header */}
      <Flex
        p={4}
        bg={sectionBgColor}
        borderBottomWidth="1px"
        borderColor={borderColor}
        align="center"
        justify="space-between"
        wrap="wrap"
      >
        <Heading
          as="h1"
          size="lg"
          id="document-title"
          tabIndex={-1}
          ref={mainHeadingRef}
          aria-label={`Legal document: ${document?.title}`}
        >
          {document?.title}
        </Heading>
        {/* Document type badge */}
        <Badge colorScheme="blue" p={2} ml={2}>
          {document?.type}
        </Badge>
      </Flex>
      {/* Document toolbar */}
      <Flex
        p={2}
        bg={sectionBgColor}
        borderBottomWidth="1px"
        borderColor={borderColor}
        align="center"
        wrap="wrap"
        onKeyDown={handleToolbarKeyDown}
        aria-label="Document toolbar"
        role="toolbar"
      >
        <Tooltip label={`Table of contents (Alt+T)`}>
          <IconButton
            icon={<FaList />}
            aria-label="Table of contents"
            size="md"
            variant="ghost"
            onClick={onOpen}
            mr={2}
            ref={tocButtonRef}
          />
        </Tooltip>
        <Tooltip label="Search in document">
          <IconButton
            icon={<FaSearch />}
            aria-label="Search in document"
            size="md"
            variant="ghost"
            mr={2}
            ref={searchButtonRef}
          />
        </Tooltip>
        <Tooltip label={`Highlight text (Alt+H)`}>
          <IconButton
            icon={<FaHighlighter />}
            aria-label="Highlight selected text"
            size="md"
            variant="ghost"
            mr={2}
            onClick={highlightSelectedText}
            isDisabled={!selectedText}
            ref={highlightButtonRef}
          />
        </Tooltip>
        <Tooltip label={`Read aloud (Alt+S)`}>
          <IconButton
            icon={<FaVolumeUp />}
            aria-label={isSpeaking ? 'Stop reading' : 'Read section aloud'}
            size="md"
            variant="ghost"
            mr={2}
            onClick={() => speakSection()}
            colorScheme={isSpeaking ? 'red' : 'gray'}
            ref={speakButtonRef}
          />
        </Tooltip>
        <Divider orientation="vertical" h="24px" mx={2} />
        <Tooltip label={`Print document (Alt+P)`}>
          <IconButton
            icon={<FaPrint />}
            aria-label="Print document"
            size="md"
            variant="ghost"
            mr={2}
            onClick={onPrint}
            ref={printButtonRef}
          />
        </Tooltip>
        <Tooltip label={`Download document (Alt+D)`}>
          <IconButton
            icon={<FaDownload />}
            aria-label="Download document"
            size="md"
            variant="ghost"
            mr={2}
            onClick={onDownload}
            ref={downloadButtonRef}
          />
        </Tooltip>
        <Menu>
          <Tooltip label="Settings">
            <MenuButton
              as={IconButton}
              icon={<FaCog />}
              aria-label="Document settings"
              size="md"
              variant="ghost"
              ref={settingsButtonRef}
            />
          </Tooltip>
          <MenuList>
            <MenuItem closeOnSelect={false}>
              <Box width="100%">
                <Text mb={2}>Text Size</Text>
                <Slider
                  min={12}
                  max={24}
                  step={2}
                  value={textSize}
                  onChange={val => setTextSize(val)}
                  aria-label="Adjust text size"
                >
                  <SliderTrack>
                    <SliderFilledTrack />
                  </SliderTrack>
                  <SliderThumb />
                </Slider>
              </Box>
            </MenuItem>
          </MenuList>
        </Menu>
      </Flex>
      {/* Document navigation */}
      <Flex
        justify="space-between"
        p={2}
        onKeyDown={handleNavKeyDown}
        aria-label="Document navigation"
        role="navigation"
      >
        <Button
          leftIcon={<FaChevronLeft />}
          onClick={goToPrevSection}
          isDisabled={currentSection <= 0}
          ref={prevButtonRef}
          aria-label="Previous section"
        >
          Previous
        </Button>
        <Text>
          Section {currentSection + 1} of {processedSections.length}
        </Text>
        <Button
          rightIcon={<FaChevronRight />}
          onClick={goToNextSection}
          isDisabled={currentSection >= processedSections.length - 1}
          ref={nextButtonRef}
          aria-label="Next section"
        >
          Next
        </Button>
      </Flex>
      {/* Document content */}
      <Box
        p={6}
        ref={contentRef}
        aria-label="Document content"
        role="article"
        fontSize={`${textSize}px`}
      >
        {processedSections.map((section, index) => (
          <Box
            key={index}
            id={`section-${index}`}
            mb={5}
            p={3}
            borderLeft={currentSection === index ? '4px solid' : 'none'}
            borderColor="blue.500"
            bg={currentSection === index ? 'blue.50' : 'transparent'}
            position="relative"
            tabIndex={0}
            aria-label={section.accessibleDescription}
            _focus={{
              outline: '2px solid blue',
              outlineOffset: '2px',
            }}
            onFocus={() => setCurrentSection(index)}
          >
            {section.type === 'heading' ? (
              <Heading
                as={section.level === 1 ? 'h2' : section.level === 2 ? 'h3' : 'h4'}
                size={section.level === 1 ? 'lg' : section.level === 2 ? 'md' : 'sm'}
                mb={2}
                display="flex"
                alignItems="center"
              >
                <Box mr={2}>
                  <FaHeading
                    size={section.level === 1 ? 20 : section.level === 2 ? 16 : 14}
                    aria-hidden="true"
                  />
                </Box>
                {section.content}
                {bookmarks.includes(index) && (
                  <Box ml={2} color="yellow.500">
                    <FaBookmark aria-hidden="true" />
                  </Box>
                )}
              </Heading>
            ) : (
              <Box display="flex">
                <Box mr={2} pt={1}>
                  <FaParagraph size={12} aria-hidden="true" />
                </Box>
                <Text>{section.content}</Text>
                {bookmarks.includes(index) && (
                  <Box ml={2} color="yellow.500">
                    <FaBookmark aria-hidden="true" />
                  </Box>
                )}
              </Box>
            )}
            {/* Actions for each section */}
            <HStack
              position="absolute"
              top={2}
              right={2}
              opacity={0.7}
              _groupHover={{ opacity: 1 }}
            >
              <Tooltip label="Bookmark section">
                <IconButton
                  icon={<FaBookmark />}
                  size="xs"
                  variant="ghost"
                  aria-label={
                    bookmarks.includes(index) ? 'Remove bookmark' : 'Bookmark this section'
                  }
                  onClick={() => bookmarkSection(index)}
                  colorScheme={bookmarks.includes(index) ? 'yellow' : 'gray'}
                />
              </Tooltip>
              <Tooltip label="Read this section aloud">
                <IconButton
                  icon={<FaVolumeUp />}
                  size="xs"
                  variant="ghost"
                  aria-label="Read this section aloud"
                  onClick={() => speakSection(index)}
                />
              </Tooltip>
              <Tooltip label="Copy section text">
                <IconButton
                  icon={<FaCopy />}
                  size="xs"
                  variant="ghost"
                  aria-label="Copy section text"
                  onClick={() => {
                    navigator.clipboard.writeText(section.content);
                    announce('Section text copied to clipboard');
                  }}
                />
              </Tooltip>
            </HStack>
          </Box>
        ))}
      </Box>
      {/* Table of contents drawer */}
      <Drawer isOpen={isOpen} placement="left" onClose={onDrawerClose} finalFocusRef={tocButtonRef}>
        <DrawerOverlay />
        <DrawerContent ref={drawerRef} onKeyDown={handleDrawerKeyDown}>
          <DrawerCloseButton />
          <DrawerHeader>Document Structure</DrawerHeader>
          <DrawerBody>
            <List spacing={2}>
              {processedSections.map((section, index) => (
                <ListItem
                  key={index}
                  p={2}
                  borderRadius="md"
                  cursor="pointer"
                  _hover={{ bg: 'gray.100' }}
                  onClick={() => goToSection(index)}
                  display="flex"
                  alignItems="center"
                  bg={currentSection === index ? 'blue.50' : 'transparent'}
                  tabIndex={0}
                  role="button"
                  aria-pressed={currentSection === index}
                >
                  <Box mr={2}>
                    {section.type === 'heading' ? (
                      <FaHeading
                        size={section.level === 1 ? 18 : section.level === 2 ? 16 : 14}
                        aria-hidden="true"
                      />
                    ) : (
                      <FaParagraph size={12} aria-hidden="true" />
                    )}
                  </Box>
                  <Text
                    fontWeight={section.type === 'heading' ? 'bold' : 'normal'}
                    pl={
                      section.type === 'heading' && section.level > 1 ? (section.level - 1) * 4 : 0
                    }
                    fontSize={section.type === 'heading' ? 'md' : 'sm'}
                    noOfLines={2}
                  >
                    {section.content}
                  </Text>
                  {bookmarks.includes(index) && (
                    <Box ml="auto" color="yellow.500">
                      <FaBookmark aria-hidden="true" />
                    </Box>
                  )}
                </ListItem>
              ))}
            </List>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
      {/* Keyboard shortcuts help */}
      <Box position="fixed" bottom={4} right={4}>
        <Tooltip label="Keyboard shortcuts">
          <IconButton
            icon={<FaInfoCircle />}
            aria-label="Show keyboard shortcuts"
            size="md"
            colorScheme="blue"
            onClick={() => {
              announce(`Keyboard shortcuts: Alt+Left Arrow: Previous section. 
                Alt+Right Arrow: Next section. 
                Alt+T: Table of contents. 
                Alt+S: Read section aloud. 
                Alt+B: Bookmark section. 
                Alt+H: Highlight selected text. 
                Alt+P: Print document. 
                Alt+D: Download document.`);
            }}
          />
        </Tooltip>
      </Box>
    </Box>
  );
};

// Define PropTypes
LegalDocumentViewer.propTypes = {
  /** TODO: Add description */
  document: PropTypes.any,
  /** TODO: Add description */
  onBookmark: PropTypes.any,
  /** TODO: Add description */
  onPrint: PropTypes.any,
  /** TODO: Add description */
  onDownload: PropTypes.any,
  /** TODO: Add description */
  onClose: PropTypes.any,
};

export default LegalDocumentViewer;