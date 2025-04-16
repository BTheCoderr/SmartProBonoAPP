import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Textarea,
  Stack,
  Heading,
  Text,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Flex,
  Checkbox,
  Badge,
  IconButton,
  Tooltip,
  Divider,
  VStack,
  HStack,
} from '@chakra-ui/react';
import {
  CalendarIcon,
  TimeIcon,
  CheckIcon,
  WarningIcon,
  InfoIcon,
  AddIcon,
  DownloadIcon,
  ExternalLinkIcon,
  LinkIcon,
} from '@chakra-ui/icons';
import 'react-datepicker/dist/react-datepicker.css';
import calendarIntegration, {
  CALENDAR_PROVIDERS,
  EVENT_TYPES,
  PRIORITY_LEVELS,
} from '../utils/calendarIntegration';
import { useFocusGroup, useFocusable } from '../utils/focusManager';
import { logUserAction } from '../utils/auditLogger';
// Main component for scheduling court dates and appointments
const CalendarScheduler = ({ caseData, onEventScheduled, className }) => {
  const toast = useToast();
  const { isOpen, onOpen, onClose } = useDisclosure();
  // State for the event form
  const [formData, setFormData] = useState({
    title: '',
    type: EVENT_TYPES.COURT_DATE,
    startTime: new Date(),
    endTime: new Date(new Date().getTime() + 60 * 60 * 1000), // Default to 1 hour later
    description: '',
    location: '',
    priority: PRIORITY_LEVELS.MEDIUM,
    notes: '',
    contactInfo: '',
    clientName: '',
    documentLinks: [],
    caseId: '',
    caseName: '',
  });
  // State for adding document links
  const [newDocLink, setNewDocLink] = useState({ title: '', url: '' });
  // State for calendar provider selection
  const [selectedProvider, setSelectedProvider] = useState(CALENDAR_PROVIDERS.GOOGLE);
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [authToken, setAuthToken] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  // Focus management setup
  const formFocusGroup = useFocusGroup('calendar-form', 'vertical');
  const documentLinksFocusGroup = useFocusGroup('document-links', 'vertical');
  const actionButtonsFocusGroup = useFocusGroup('calendar-actions', 'horizontal');
  // Register focusable elements for the form
  const titleRef = useFocusable('title-input', formFocusGroup);
  const typeRef = useFocusable('type-select', formFocusGroup);
  const dateRef = useFocusable('date-picker', formFocusGroup);
  const timeRef = useFocusable('time-picker', formFocusGroup);
  const endTimeRef = useFocusable('end-time-picker', formFocusGroup);
  const locationRef = useFocusable('location-input', formFocusGroup);
  const priorityRef = useFocusable('priority-select', formFocusGroup);
  const descriptionRef = useFocusable('description-input', formFocusGroup);
  const notesRef = useFocusable('notes-input', formFocusGroup);
  const contactRef = useFocusable('contact-input', formFocusGroup);
  // Register focusable elements for the action buttons
  const scheduleRef = useFocusable('schedule-button', actionButtonsFocusGroup);
  const exportRef = useFocusable('export-button', actionButtonsFocusGroup);
  const cancelRef = useFocusable('cancel-button', actionButtonsFocusGroup);
  // Initialize form data if caseData is provided
  useEffect(() => {
    if (caseData) {
      setFormData(prev => ({
        ...prev,
        caseId: caseData.id || '',
        caseName: caseData.title || '',
        clientName: caseData.client?.name || '',
      }));
    }
  }, [caseData]);
  // Handle OAuth callback
  useEffect(() => {
    const handleCallback = () => {
      const hash = window.location.hash;
      if (hash && hash.includes('access_token')) {
        // Extract access token
        const params = new URLSearchParams(hash.substring(1));
        const accessToken = params.get('access_token');
        if (accessToken) {
          setAuthToken(accessToken);
          toast({
            title: 'Successfully authenticated!',
            description: 'You can now add events to your calendar.',
            status: 'success',
            duration: 5000,
            isClosable: true,
          });
          // Clear the URL hash
          window.history.replaceState(null, null, window.location.pathname);
        }
      }
    };
    handleCallback();
  }, [toast]);
  // Handle form input changes
  const handleInputChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };
  // Handle date/time selection
  const handleDateTimeChange = (date, field) => {
    setFormData(prev => ({
      ...prev,
      [field]: date,
    }));
  };
  // Handle provider selection
  const handleProviderChange = e => {
    setSelectedProvider(e.target.value);
    // Reset auth token when provider changes
    setAuthToken(null);
  };
  // Handle authentication
  const handleAuthenticate = () => {
    if (
      selectedProvider === CALENDAR_PROVIDERS.GOOGLE ||
      selectedProvider === CALENDAR_PROVIDERS.OUTLOOK
    ) {
      setIsAuthenticating(true);
      const authUrl = calendarIntegration.getAuthorizationUrl(selectedProvider);
      if (authUrl) {
        window.location.href = authUrl;
      } else {
        toast({
          title: 'Authentication Error',
          description: 'Unable to generate authentication URL.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
        setIsAuthenticating(false);
      }
    } else {
      // Other providers don't need OAuth
      toast({
        title: 'No Authentication Required',
        description: 'This provider allows direct export without authentication.',
        status: 'info',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  // Handle document link form
  const handleDocLinkChange = e => {
    const { name, value } = e.target;
    setNewDocLink(prev => ({
      ...prev,
      [name]: value,
    }));
  };
  // Add a document link
  const handleAddDocLink = () => {
    if (newDocLink.title && newDocLink.url) {
      setFormData(prev => ({
        ...prev,
        documentLinks: [...prev.documentLinks, { ...newDocLink }],
      }));
      setNewDocLink({ title: '', url: '' });
      // Log the action
      logUserAction('Added document link to calendar event', {
        documentTitle: newDocLink.title,
        eventTitle: formData.title,
      });
    }
  };
  // Remove a document link
  const handleRemoveDocLink = index => {
    setFormData(prev => ({
      ...prev,
      documentLinks: prev.documentLinks.filter((_, i) => i !== index),
    }));
  };
  // Submit handler for the form
  const handleSubmit = async e => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const eventData = {
        ...formData,
        startTime: formData.startTime.toISOString(),
        endTime: formData.endTime.toISOString(),
      };
      if (
        selectedProvider === CALENDAR_PROVIDERS.ICAL ||
        selectedProvider === CALENDAR_PROVIDERS.APPLE
      ) {
        // For iCal or Apple Calendar, just download the file
        calendarIntegration.downloadICalendarFile(eventData);
        toast({
          title: 'Calendar Event Created',
          description:
            'The calendar file has been downloaded. Import it into your calendar application.',
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
        if (onEventScheduled) {
          onEventScheduled(eventData);
        }
      } else {
        // For Google or Outlook Calendar
        if (!authToken) {
          toast({
            title: 'Authentication Required',
            description: 'Please authenticate with your calendar provider first.',
            status: 'warning',
            duration: 5000,
            isClosable: true,
          });
          setIsSubmitting(false);
          return;
        }
        const result = await calendarIntegration.createCalendarEvent(eventData, selectedProvider, {
          accessToken: authToken,
        });
        toast({
          title: 'Event Added to Calendar',
          description: `"${formData.title}" has been added to your calendar.`,
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
        if (onEventScheduled) {
          onEventScheduled(eventData);
        }
        // Reset form
        setFormData({
          title: '',
          type: EVENT_TYPES.COURT_DATE,
          startTime: new Date(),
          endTime: new Date(new Date().getTime() + 60 * 60 * 1000),
          description: '',
          location: '',
          priority: PRIORITY_LEVELS.MEDIUM,
          notes: '',
          contactInfo: '',
          clientName: '',
          documentLinks: [],
          caseId: caseData?.id || '',
          caseName: caseData?.title || '',
        });
        onClose();
      }
    } catch (error) {
      console.error('Error creating calendar event:', error);
      toast({
        title: 'Error Creating Event',
        description: error.message || 'Failed to create the calendar event. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };
  // Document link item component (to avoid hooks in render functions)
  const DocumentLinkItem = ({ doc, index, onRemove }) => {
    const focusableProps = useFocusable(`remove-doc-${index}`, documentLinksFocusGroup);
    
    return (
      <Flex key={index} justify="space-between" align="center" mb={2}>
        <HStack>
          <LinkIcon />
          <Text fontWeight="medium">{doc.title}</Text>
        </HStack>
        <IconButton
          aria-label={`Remove document ${doc.title}`}
          icon={<WarningIcon />}
          size="sm"
          colorScheme="red"
          variant="ghost"
          onClick={() => onRemove(index)}
          {...focusableProps}
        />
      </Flex>
    );
  };
  // Helper for rendering document links
  const renderDocumentLinks = () => {
    return (
      <VStack align="stretch" spacing={2} mb={4}>
        <Text fontWeight="semibold" mb={1}>
          Related Documents
        </Text>
        {formData.documentLinks.map((doc, index) => (
          <DocumentLinkItem 
            key={index}
            doc={doc}
            index={index}
            onRemove={handleRemoveDocLink}
          />
        ))}
      </VStack>
    );
  };
  // Helper for event type options
  const renderEventTypeOptions = () => {
    return Object.entries(EVENT_TYPES).map(([key, value]) => (
      <option key={value} value={value}>
        {key
          .split('_')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ')}
      </option>
    ));
  };
  // Helper for priority options
  const renderPriorityOptions = () => {
    return Object.entries(PRIORITY_LEVELS).map(([key, value]) => (
      <option key={value} value={value}>
        {key.charAt(0) + key.slice(1).toLowerCase()}
      </option>
    ));
  };
  // Helper for provider options
  const renderProviderOptions = () => {
    return Object.entries(CALENDAR_PROVIDERS).map(([key, value]) => (
      <option key={value} value={value}>
        {key
          .split('_')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ')}
      </option>
    ));
  };
  // Render the priority badge
  const renderPriorityBadge = priority => {
    const colorScheme =
      priority === PRIORITY_LEVELS.HIGH
        ? 'red'
        : priority === PRIORITY_LEVELS.MEDIUM
          ? 'yellow'
          : 'green';
    return (
      <Badge colorScheme={colorScheme} ml={2}>
        {priority === PRIORITY_LEVELS.HIGH
          ? 'High'
          : priority === PRIORITY_LEVELS.MEDIUM
            ? 'Medium'
            : 'Low'}
      </Badge>
    );
  };
  // Auth button component to handle conditional use of hooks
  const AuthButton = () => {
    const focusableProps = useFocusable('auth-button', actionButtonsFocusGroup);
    
    return (
      <Button
        onClick={handleAuthenticate}
        isLoading={isAuthenticating}
        colorScheme="purple"
        {...focusableProps}
      >
        Connect
      </Button>
    );
  };
  return (
    <Box className={className}>
      <Flex justifyContent="space-between" alignItems="center" mb={4}>
        <Heading size="md">
          <CalendarIcon mr={2} />
          Court Dates & Appointments
        </Heading>
        <Button
          leftIcon={<AddIcon />}
          colorScheme="blue"
          onClick={onOpen}
          aria-label="Schedule new event"
        >
          Schedule New
        </Button>
      </Flex>
      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent aria-labelledby="calendar-scheduler-modal-title">
          <form onSubmit={handleSubmit}>
            <ModalHeader id="calendar-scheduler-modal-title">
              Schedule Court Date or Appointment
              {formData.priority && renderPriorityBadge(formData.priority)}
            </ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <VStack spacing={4} align="stretch">
                <FormControl isRequired>
                  <FormLabel htmlFor="title">Event Title</FormLabel>
                  <Input
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    placeholder="e.g., Initial Hearing, Client Meeting"
                    ref={titleRef}
                  />
                </FormControl>
                <FormControl isRequired>
                  <FormLabel htmlFor="type">Event Type</FormLabel>
                  <Select
                    id="type"
                    name="type"
                    value={formData.type}
                    onChange={handleInputChange}
                    ref={typeRef}
                  >
                    {renderEventTypeOptions()}
                  </Select>
                </FormControl>
                <HStack spacing={4}>
                  <FormControl isRequired flex="1">
                    <FormLabel htmlFor="startTime">Date</FormLabel>
                    <Input
                      id="date"
                      type="date"
                      value={formData.startTime.toISOString().split('T')[0]}
                      onChange={e => {
                        const date = new Date(e.target.value);
                        const current = new Date(formData.startTime);
                        current.setFullYear(date.getFullYear());
                        current.setMonth(date.getMonth());
                        current.setDate(date.getDate());
                        handleDateTimeChange(current, 'startTime');
                        // Also update end time to same date but keep time
                        const end = new Date(formData.endTime);
                        end.setFullYear(date.getFullYear());
                        end.setMonth(date.getMonth());
                        end.setDate(date.getDate());
                        handleDateTimeChange(end, 'endTime');
                      }}
                      ref={dateRef}
                    />
                  </FormControl>
                  <FormControl isRequired flex="1">
                    <FormLabel htmlFor="startTimeInput">Start Time</FormLabel>
                    <Input
                      id="startTimeInput"
                      type="time"
                      value={formData.startTime.toTimeString().substring(0, 5)}
                      onChange={e => {
                        const [hours, minutes] = e.target.value.split(':');
                        const date = new Date(formData.startTime);
                        date.setHours(parseInt(hours, 10));
                        date.setMinutes(parseInt(minutes, 10));
                        handleDateTimeChange(date, 'startTime');
                      }}
                      ref={timeRef}
                    />
                  </FormControl>
                  <FormControl flex="1">
                    <FormLabel htmlFor="endTimeInput">End Time</FormLabel>
                    <Input
                      id="endTimeInput"
                      type="time"
                      value={formData.endTime.toTimeString().substring(0, 5)}
                      onChange={e => {
                        const [hours, minutes] = e.target.value.split(':');
                        const date = new Date(formData.endTime);
                        date.setHours(parseInt(hours, 10));
                        date.setMinutes(parseInt(minutes, 10));
                        handleDateTimeChange(date, 'endTime');
                      }}
                      ref={endTimeRef}
                    />
                  </FormControl>
                </HStack>
                <FormControl>
                  <FormLabel htmlFor="location">Location</FormLabel>
                  <Input
                    id="location"
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    placeholder="e.g., Courtroom 302, 123 Main St, or Video Conference"
                    ref={locationRef}
                  />
                </FormControl>
                <FormControl>
                  <FormLabel htmlFor="priority">Priority</FormLabel>
                  <Select
                    id="priority"
                    name="priority"
                    value={formData.priority}
                    onChange={handleInputChange}
                    ref={priorityRef}
                  >
                    {renderPriorityOptions()}
                  </Select>
                </FormControl>
                <FormControl>
                  <FormLabel htmlFor="description">Description</FormLabel>
                  <Textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Brief description of the event"
                    rows={2}
                    ref={descriptionRef}
                  />
                </FormControl>
                <FormControl>
                  <FormLabel htmlFor="notes">Notes</FormLabel>
                  <Textarea
                    id="notes"
                    name="notes"
                    value={formData.notes}
                    onChange={handleInputChange}
                    placeholder="Additional notes, preparations needed, etc."
                    rows={3}
                    ref={notesRef}
                  />
                </FormControl>
                <FormControl>
                  <FormLabel htmlFor="contactInfo">Contact Information</FormLabel>
                  <Input
                    id="contactInfo"
                    name="contactInfo"
                    value={formData.contactInfo}
                    onChange={handleInputChange}
                    placeholder="Contact person and information for this event"
                    ref={contactRef}
                  />
                </FormControl>
                <Box>
                  <FormLabel>Related Documents</FormLabel>
                  <HStack>
                    <Input
                      name="title"
                      value={newDocLink.title}
                      onChange={handleDocLinkChange}
                      placeholder="Document Title"
                      size="sm"
                      flex="1"
                      {...useFocusable('doc-title-input', documentLinksFocusGroup)}
                    />
                    <Input
                      name="url"
                      value={newDocLink.url}
                      onChange={handleDocLinkChange}
                      placeholder="URL"
                      size="sm"
                      flex="2"
                      {...useFocusable('doc-url-input', documentLinksFocusGroup)}
                    />
                    <IconButton
                      aria-label="Add document link"
                      icon={<AddIcon />}
                      size="sm"
                      colorScheme="blue"
                      onClick={handleAddDocLink}
                      isDisabled={!newDocLink.title || !newDocLink.url}
                      {...useFocusable('add-doc-button', documentLinksFocusGroup)}
                    />
                  </HStack>
                  {renderDocumentLinks()}
                </Box>
                <Divider />
                <Box>
                  <FormLabel>Calendar Service</FormLabel>
                  <HStack>
                    <Select
                      value={selectedProvider}
                      onChange={handleProviderChange}
                      flex="1"
                      {...useFocusable('provider-select', actionButtonsFocusGroup)}
                    >
                      {renderProviderOptions()}
                    </Select>
                    {(selectedProvider === CALENDAR_PROVIDERS.GOOGLE ||
                      selectedProvider === CALENDAR_PROVIDERS.OUTLOOK) &&
                      !authToken && <AuthButton />}
                    {authToken && (
                      <Badge colorScheme="green" p={2} borderRadius="md">
                        <Flex align="center">
                          <CheckIcon mr={1} />
                          Connected
                        </Flex>
                      </Badge>
                    )}
                  </HStack>
                  <Text fontSize="xs" mt={1} color="gray.500">
                    <InfoIcon mr={1} />
                    {selectedProvider === CALENDAR_PROVIDERS.GOOGLE ||
                    selectedProvider === CALENDAR_PROVIDERS.OUTLOOK
                      ? authToken
                        ? "You're connected and ready to add events directly to your calendar."
                        : 'Connect to add events directly to your calendar.'
                      : "You'll receive a file to import into your calendar application."}
import PropTypes from 'prop-types';
                  </Text>
                </Box>
              </VStack>
            </ModalBody>
            <ModalFooter>
              <HStack spacing={3}>
                <Button onClick={onClose} variant="outline" ref={cancelRef}>
                  Cancel
                </Button>
                {(selectedProvider === CALENDAR_PROVIDERS.ICAL ||
                  selectedProvider === CALENDAR_PROVIDERS.APPLE) && (
                  <Button
                    type="submit"
                    colorScheme="blue"
                    leftIcon={<DownloadIcon />}
                    isLoading={isSubmitting}
                    ref={exportRef}
                  >
                    Export Calendar File
                  </Button>
                )}
                {(selectedProvider === CALENDAR_PROVIDERS.GOOGLE ||
                  selectedProvider === CALENDAR_PROVIDERS.OUTLOOK) && (
                  <Button
                    type="submit"
                    colorScheme="blue"
                    leftIcon={<CalendarIcon />}
                    isLoading={isSubmitting}
                    isDisabled={!authToken}
                    ref={scheduleRef}
                  >
                    Add to Calendar
                  </Button>
                )}
              </HStack>
            </ModalFooter>
          </form>
        </ModalContent>
      </Modal>
    </Box>
  );
};

// Define PropTypes
CalendarScheduler.propTypes = {
  /** TODO: Add description */
  caseData: PropTypes.any,
  /** TODO: Add description */
  onEventScheduled: PropTypes.any,
  /** TODO: Add description */
  className: PropTypes.any,
};

export default CalendarScheduler;