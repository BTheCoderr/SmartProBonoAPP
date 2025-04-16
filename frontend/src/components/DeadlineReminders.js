import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  Text,
  Badge,
  VStack,
  HStack,
  IconButton,
  useColorModeValue,
  Checkbox,
  Divider,
  useToast,
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  FormControl,
  FormLabel,
  Input,
  Select,
  Tooltip,
} from '@chakra-ui/react';
import { FaCheckCircle, FaBell, FaPlus, FaSort } from 'react-icons/fa';
import { format, isBefore, addDays, parseISO } from 'date-fns';
// Priority colors
const priorityColors = {
  HIGH: 'red',
  MEDIUM: 'orange',
  LOW: 'green',
};
// Mock data for deadlines - in a real app, this would come from an API
const mockDeadlines = [
  {
    id: 1,
    caseId: 'CASE-2023-001',
    caseName: 'Johnson Family Custody',
    title: 'File Motion for Extension',
    description: 'Submit motion for extension of time to court',
    deadline: '2023-07-15T10:00:00Z',
    priority: 'HIGH',
    completed: false,
  },
  {
    id: 2,
    caseId: 'CASE-2023-003',
    caseName: 'Smith Immigration Petition',
    title: 'Client Document Collection',
    description: 'Collect all required immigration documents from client',
    deadline: '2023-07-25T15:00:00Z',
    priority: 'MEDIUM',
    completed: false,
  },
  {
    id: 3,
    caseId: 'CASE-2023-008',
    caseName: 'Garcia Housing Dispute',
    title: 'Hearing Preparation',
    description: 'Prepare client for upcoming eviction hearing',
    deadline: '2023-08-02T09:00:00Z',
    priority: 'HIGH',
    completed: false,
  },
  {
    id: 4,
    caseId: 'CASE-2023-005',
    caseName: 'Williams Expungement',
    title: 'Submit Court Forms',
    description: 'Submit completed expungement forms to county clerk',
    deadline: '2023-08-10T14:00:00Z',
    priority: 'MEDIUM',
    completed: false,
  },
  {
    id: 5,
    caseId: 'CASE-2023-012',
    caseName: 'Thompson Bankruptcy',
    title: 'Financial Document Review',
    description: 'Review client financial documents before filing',
    deadline: '2023-08-18T11:30:00Z',
    priority: 'LOW',
    completed: false,
  },
];
const DeadlineReminders = () => {
  const [deadlines, setDeadlines] = useState([]);
  const [sortBy, setSortBy] = useState('deadline'); // 'deadline' or 'priority'
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [newDeadline, setNewDeadline] = useState({
    caseId: '',
    caseName: '',
    title: '',
    description: '',
    deadline: '',
    priority: 'MEDIUM',
  });
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const toast = useToast();
  // Fetch deadlines on component mount
  useEffect(() => {
    // In a real app, this would be an API call
    fetchDeadlines();
  }, [fetchDeadlines]);
  const fetchDeadlines = () => {
    // Simulate API call with mock data
    setDeadlines(mockDeadlines);
    sortDeadlines(mockDeadlines, sortBy);
  };
  const sortDeadlines = (deadlinesToSort, sortField) => {
    const sorted = [...deadlinesToSort].sort((a, b) => {
      if (sortField === 'deadline') {
        return new Date(a.deadline) - new Date(b.deadline);
      } else if (sortField === 'priority') {
        const priorityValues = { HIGH: 3, MEDIUM: 2, LOW: 1 };
        return priorityValues[b.priority] - priorityValues[a.priority];
      }
      return 0;
    });
    setDeadlines(sorted);
  };
  const toggleSort = () => {
    const newSortBy = sortBy === 'deadline' ? 'priority' : 'deadline';
    setSortBy(newSortBy);
    sortDeadlines(deadlines, newSortBy);
  };
  const handleToggleComplete = id => {
    const updatedDeadlines = deadlines.map(deadline =>
      deadline.id === id ? { ...deadline, completed: !deadline.completed } : deadline
    );
    setDeadlines(updatedDeadlines);
    // In a real app, you would save this to the backend
    const completedDeadline = updatedDeadlines.find(d => d.id === id);
    if (completedDeadline.completed) {
      toast({
        title: 'Deadline completed',
        description: `${completedDeadline.title} marked as completed.`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    }
  };
  const isDeadlineNear = deadlineDate => {
    const today = new Date();
    const deadlineDateTime = new Date(deadlineDate);
    const threeDaysFromNow = addDays(today, 3);
    return isBefore(deadlineDateTime, threeDaysFromNow) && !isBefore(deadlineDateTime, today);
  };
  const isDeadlinePast = deadlineDate => {
    const today = new Date();
    const deadlineDateTime = new Date(deadlineDate);
    return isBefore(deadlineDateTime, today);
  };
  const handleAddDeadline = () => {
    // Validate form fields
    if (!newDeadline.caseId || !newDeadline.title || !newDeadline.deadline) {
      toast({
        title: 'Error',
        description: 'Please fill out all required fields',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    // Create new deadline with generated ID
    const deadline = {
      ...newDeadline,
      id: Date.now(), // Simple ID generation
      completed: false,
    };
    // Add to deadlines list
    const updatedDeadlines = [...deadlines, deadline];
    sortDeadlines(updatedDeadlines, sortBy);
    // Close modal and reset form
    setIsAddModalOpen(false);
    setNewDeadline({
      caseId: '',
      caseName: '',
      title: '',
      description: '',
      deadline: '',
      priority: 'MEDIUM',
    });
    // Show success message
    toast({
      title: 'Deadline added',
      description: 'New deadline has been added successfully.',
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };
  const getDeadlineStatusText = deadline => {
    if (deadline.completed) {
      return 'Completed';
    }
    if (isDeadlinePast(deadline.deadline)) {
      return 'Overdue';
    }
    if (isDeadlineNear(deadline.deadline)) {
      return 'Upcoming';
    }
    return 'Future';
  };
  const getDeadlineStatusColor = deadline => {
    if (deadline.completed) {
      return 'green';
    }
    if (isDeadlinePast(deadline.deadline)) {
      return 'red';
    }
    if (isDeadlineNear(deadline.deadline)) {
      return 'orange';
    }
    return 'blue';
  };
  return (
    <Box
      borderWidth="1px"
      borderRadius="lg"
      p={4}
      shadow="md"
      bg={bgColor}
      borderColor={borderColor}
    >
      <HStack justifyContent="space-between" mb={4}>
        <HStack>
          <FaBell />
          <Heading size="md">Upcoming Deadlines</Heading>
        </HStack>
        <HStack>
          <Tooltip label={`Sort by ${sortBy === 'deadline' ? 'priority' : 'date'}`}>
            <IconButton
              icon={<FaSort />}
              size="sm"
              onClick={toggleSort}
              aria-label={`Sort by ${sortBy === 'deadline' ? 'priority' : 'date'}`}
            />
          </Tooltip>
          <Tooltip label="Add new deadline">
            <IconButton
              icon={<FaPlus />}
              size="sm"
              colorScheme="blue"
              onClick={() => setIsAddModalOpen(true)}
              aria-label="Add new deadline"
            />
          </Tooltip>
        </HStack>
      </HStack>
      {deadlines.length === 0 ? (
        <Text textAlign="center" py={4}>
          No upcoming deadlines
        </Text>
      ) : (
        <VStack spacing={3} align="stretch" maxH="350px" overflowY="auto">
          {deadlines.map(deadline => (
            <Box
              key={deadline.id}
              p={3}
              borderWidth="1px"
              borderRadius="md"
              borderColor={deadline.completed ? 'gray.200' : borderColor}
              opacity={deadline.completed ? 0.7 : 1}
              bg={deadline.completed ? 'gray.50' : bgColor}
            >
              <HStack justifyContent="space-between">
                <VStack align="start" spacing={1} flex="1">
                  <HStack width="100%">
                    <Checkbox
                      isChecked={deadline.completed}
                      onChange={() => handleToggleComplete(deadline.id)}
                      colorScheme="green"
                      size="lg"
                    />
                    <Text
                      fontWeight="bold"
                      textDecoration={deadline.completed ? 'line-through' : 'none'}
                    >
                      {deadline.title}
                    </Text>
                  </HStack>
                  <HStack spacing={2} ml={6}>
                    <Badge colorScheme={getDeadlineStatusColor(deadline)}>
                      {getDeadlineStatusText(deadline)}
                    </Badge>
                    <Badge colorScheme={priorityColors[deadline.priority]}>
                      {deadline.priority}
                    </Badge>
                    <Text fontSize="sm" color="gray.500">
                      {deadline.caseId}: {deadline.caseName}
                    </Text>
                  </HStack>
                  {deadline.description && (
                    <Text fontSize="sm" ml={6} color="gray.600">
                      {deadline.description}
                    </Text>
                  )}
                  <Text fontSize="sm" ml={6} color="gray.500">
                    Due: {format(parseISO(deadline.deadline), 'MMM dd, yyyy hh:mm a')}
                  </Text>
                </VStack>
                {deadline.completed && (
                  <IconButton
                    icon={<FaCheckCircle />}
                    colorScheme="green"
                    variant="ghost"
                    isRound
                    size="sm"
                    aria-label="Completed"
                  />
                )}
              </HStack>
            </Box>
          ))}
        </VStack>
      )}
      {/* Add Deadline Modal */}
      <Modal isOpen={isAddModalOpen} onClose={() => setIsAddModalOpen(false)}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Add New Deadline</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={4}>
              <FormControl isRequired>
                <FormLabel>Case ID</FormLabel>
                <Input
                  placeholder="e.g., CASE-2023-015"
                  value={newDeadline.caseId}
                  onChange={e => setNewDeadline({ ...newDeadline, caseId: e.target.value })}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Case Name</FormLabel>
                <Input
                  placeholder="e.g., Smith Family Trust"
                  value={newDeadline.caseName}
                  onChange={e => setNewDeadline({ ...newDeadline, caseName: e.target.value })}
                />
              </FormControl>
              <FormControl isRequired>
                <FormLabel>Deadline Title</FormLabel>
                <Input
                  placeholder="e.g., File Response to Motion"
                  value={newDeadline.title}
                  onChange={e => setNewDeadline({ ...newDeadline, title: e.target.value })}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Description</FormLabel>
                <Input
                  placeholder="Optional details about the deadline"
                  value={newDeadline.description}
                  onChange={e => setNewDeadline({ ...newDeadline, description: e.target.value })}
                />
              </FormControl>
              <FormControl isRequired>
                <FormLabel>Deadline Date & Time</FormLabel>
                <Input
                  type="datetime-local"
                  value={newDeadline.deadline}
                  onChange={e => setNewDeadline({ ...newDeadline, deadline: e.target.value })}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Priority</FormLabel>
                <Select
                  value={newDeadline.priority}
                  onChange={e => setNewDeadline({ ...newDeadline, priority: e.target.value })}
                >
                  <option value="HIGH">High</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="LOW">Low</option>
                </Select>
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={() => setIsAddModalOpen(false)}>
              Cancel
            </Button>
            <Button colorScheme="blue" onClick={handleAddDeadline}>
              Add Deadline
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
};
export default DeadlineReminders;