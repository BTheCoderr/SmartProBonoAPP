import React, { useState, useEffect, useMemo } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  FormControl,
  FormLabel,
  Select,
  Textarea,
  VStack,
  HStack,
  Checkbox,
  Input,
  Box,
  Text,
  Badge,
  Spinner,
  useToast,
  Alert,
  AlertIcon,
} from '@chakra-ui/react';
import { getAvailableAttorneys } from '../services/userService';
import { attorneyCache } from '../services/cache/attorneyCache';
import PropTypes from 'prop-types';
const SPECIALTIES = [
  'immigration',
  'family',
  'housing',
  'employment',
  'criminal',
  'civil_rights',
  'bankruptcy',
  'consumer',
];
const AVAILABILITY_OPTIONS = [
  { value: 'any', label: 'Any Availability' },
  { value: 'weekdays', label: 'Weekdays' },
  { value: 'weekends', label: 'Weekends' },
  { value: 'evenings', label: 'Evenings' },
];
const SORT_OPTIONS = [
  { value: 'name', label: 'Name' },
  { value: 'cases', label: 'Case Load' },
  { value: 'specialties', label: 'Specialties' },
];
const AssignCaseModal = ({ isOpen, onClose, onAssign, caseType = '', isLoading: isAssigning }) => {
  const [selectedUser, setSelectedUser] = useState('');
  const [notes, setNotes] = useState('');
  const [attorneys, setAttorneys] = useState([]);
  const [loadingAttorneys, setLoadingAttorneys] = useState(false);
  const [error, setError] = useState(null);
  // Filters
  const [selectedSpecialties, setSelectedSpecialties] = useState([caseType].filter(Boolean));
  const [availability, setAvailability] = useState('any');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const toast = useToast();
  useEffect(() => {
    const fetchAttorneys = async () => {
      setLoadingAttorneys(true);
      setError(null);
      try {
        // Check cache first
        const filters = {
          specialties: selectedSpecialties,
          availability: availability === 'any' ? null : availability,
        };
        let attorneyData = attorneyCache.get(filters);
        if (!attorneyData) {
          attorneyData = await getAvailableAttorneys(filters);
          attorneyCache.set(filters, attorneyData);
        }
        setAttorneys(attorneyData);
      } catch (error) {
        setError(error.message);
        toast({
          title: 'Error',
          description: 'Failed to load available attorneys',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setLoadingAttorneys(false);
      }
    };
    if (isOpen) {
      fetchAttorneys();
    }
  }, [isOpen, selectedSpecialties, availability, toast]);
  const handleSpecialtyToggle = specialty => {
    setSelectedSpecialties(prev =>
      prev.includes(specialty) ? prev.filter(s => s !== specialty) : [...prev, specialty]
    );
  };
  const handleSort = newSortBy => {
    if (sortBy === newSortBy) {
      setSortOrder(prev => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortBy(newSortBy);
      setSortOrder('asc');
    }
  };
  const filteredAndSortedAttorneys = useMemo(() => {
    let filtered = [...attorneys];
    // Apply search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        attorney =>
          attorney.profile.full_name.toLowerCase().includes(query) ||
          attorney.profile.specialties.some(s => s.toLowerCase().includes(query))
      );
    }
    // Apply sorting
    filtered.sort((a, b) => {
      let comparison = 0;
      switch (sortBy) {
        case 'name':
          comparison = a.profile.full_name.localeCompare(b.profile.full_name);
          break;
        case 'cases':
          comparison = (a.profile.active_cases || 0) - (b.profile.active_cases || 0);
          break;
        case 'specialties':
          comparison = a.profile.specialties.length - b.profile.specialties.length;
          break;
        default:
          comparison = 0;
      }
      return sortOrder === 'asc' ? comparison : -comparison;
    });
    return filtered;
  }, [attorneys, searchQuery, sortBy, sortOrder]);
  const handleSubmit = () => {
    onAssign(selectedUser, notes);
  };
  const handleClose = () => {
    setSelectedUser('');
    setNotes('');
    setSearchQuery('');
    onClose();
  };
  return (
    <Modal isOpen={isOpen} onClose={handleClose} size="xl">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Assign Case</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <VStack spacing={4}>
            {error && (
              <Alert status="error">
                <AlertIcon />
                {error}
              </Alert>
            )}
            <FormControl>
              <FormLabel>Search Attorneys</FormLabel>
              <Input
                placeholder="Search by name or specialty..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Availability</FormLabel>
              <Select value={availability} onChange={e => setAvailability(e.target.value)}>
                {AVAILABILITY_OPTIONS.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </Select>
            </FormControl>
            <FormControl>
              <FormLabel>Specialties</FormLabel>
              <Box>
                {SPECIALTIES.map(specialty => (
                  <Checkbox
                    key={specialty}
                    isChecked={selectedSpecialties.includes(specialty)}
                    onChange={() => handleSpecialtyToggle(specialty)}
                    mr={3}
                    mb={2}
                  >
                    {specialty.replace('_', ' ')}
                  </Checkbox>
                ))}
              </Box>
            </FormControl>
            <FormControl>
              <HStack justify="space-between" mb={2}>
                <FormLabel mb={0}>Select Attorney</FormLabel>
                <Select
                  size="sm"
                  width="auto"
                  value={sortBy}
                  onChange={e => handleSort(e.target.value)}
                >
                  {SORT_OPTIONS.map(option => (
                    <option key={option.value} value={option.value}>
                      Sort by {option.label}
                    </option>
                  ))}
                </Select>
              </HStack>
              {loadingAttorneys ? (
                <Box textAlign="center" py={4}>
                  <Spinner />
                </Box>
              ) : (
                <Select
                  placeholder="Select attorney"
                  value={selectedUser}
                  onChange={e => setSelectedUser(e.target.value)}
                  isDisabled={isAssigning}
                >
                  {filteredAndSortedAttorneys.map(attorney => (
                    <option key={attorney.id} value={attorney.id}>
                      {attorney.profile.full_name} - {attorney.profile.specialties.join(', ')}
                      {attorney.profile.active_cases
                        ? ` (${attorney.profile.active_cases} active cases)`
                        : ''}
                    </option>
                  ))}
                </Select>
              )}
            </FormControl>
            <FormControl>
              <FormLabel>Assignment Notes</FormLabel>
              <Textarea
                placeholder="Add notes about this assignment..."
                value={notes}
                onChange={e => setNotes(e.target.value)}
                isDisabled={isAssigning}
              />
            </FormControl>
          </VStack>
        </ModalBody>
        <ModalFooter>
          <Button variant="ghost" mr={3} onClick={handleClose} isDisabled={isAssigning}>
            Cancel
          </Button>
          <Button
            colorScheme="blue"
            onClick={handleSubmit}
            isLoading={isAssigning}
            loadingText="Assigning..."
            isDisabled={!selectedUser || loadingAttorneys}
          >
            Assign
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

// Define PropTypes
AssignCaseModal.propTypes = {
  /** TODO: Add description */
  isOpen: PropTypes.any,
  /** TODO: Add description */
  onClose: PropTypes.any,
  /** TODO: Add description */
  onAssign: PropTypes.any,
  /** TODO: Add description */
  caseType: PropTypes.any,
  /** TODO: Add description */
  isLoading: isAssigning: PropTypes.any,
};

export default AssignCaseModal;