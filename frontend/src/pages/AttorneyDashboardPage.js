import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Heading,
  SimpleGrid,
  VStack,
  HStack,
  Text,
  Button,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  Flex,
  IconButton,
  useToast,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
} from '@chakra-ui/react';
import { 
  AddIcon, 
  CalendarIcon, 
  EditIcon, 
  ViewIcon, 
  DownloadIcon, 
  AttachmentIcon 
} from '@chakra-ui/icons';
import CalendarScheduler from '../components/CalendarScheduler';
import DeadlineReminders from '../components/DeadlineReminders';

// Case status colors
const statusColors = {
  NEW: 'blue',
  IN_PROGRESS: 'orange',
  PENDING: 'purple',
  CLOSED: 'green',
};

// Priority colors
const priorityColors = {
  LOW: 'green',
  MEDIUM: 'blue',
  HIGH: 'orange',
  CRITICAL: 'red',
};

const AttorneyDashboardPage = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const [cases, setCases] = useState([]);
  const [upcomingDeadlines, setUpcomingDeadlines] = useState([]);
  const [recentDocuments, setRecentDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [selectedCaseId, setSelectedCaseId] = useState(null);
  const [generatingDocument, setGeneratingDocument] = useState(false);

  useEffect(() => {
    // In a real implementation, these would be separate API calls
    fetchAssignedCases();
    fetchUpcomingDeadlines();
    fetchRecentDocuments();
  }, []);

  const fetchAssignedCases = async () => {
    try {
      // This would be an API call to get assigned cases
      // For now, using mock data
      setTimeout(() => {
        const mockCases = [
          {
            id: '1',
            title: 'Smith v. Johnson',
            client: 'John Smith',
            case_type: 'FAMILY',
            status: 'IN_PROGRESS',
            updated_at: '2023-06-15T10:30:00Z',
            next_deadline: '2023-06-25T00:00:00Z',
            next_deadline_title: 'File Motion for Support'
          },
          {
            id: '2',
            title: 'Housing Rights Coalition',
            client: 'Maria Garcia',
            case_type: 'HOUSING',
            status: 'NEW',
            updated_at: '2023-06-10T14:25:00Z',
            next_deadline: '2023-06-20T00:00:00Z',
            next_deadline_title: 'Submit Evidence Collection'
          },
          {
            id: '3',
            title: 'Estate of Williams',
            client: 'Robert Williams',
            case_type: 'ELDER',
            status: 'PENDING',
            updated_at: '2023-06-05T09:15:00Z',
            next_deadline: '2023-06-30T00:00:00Z',
            next_deadline_title: 'File Probate Petition'
          },
          {
            id: '4',
            title: 'Reynolds Immigration Matter',
            client: 'Sofia Reynolds',
            case_type: 'IMMIGRATION',
            status: 'IN_PROGRESS',
            updated_at: '2023-06-12T11:45:00Z',
            next_deadline: '2023-07-05T00:00:00Z',
            next_deadline_title: 'USCIS Interview Preparation'
          },
          {
            id: '5',
            title: 'Thompson Benefits Appeal',
            client: 'David Thompson',
            case_type: 'BENEFITS',
            status: 'PENDING',
            updated_at: '2023-06-08T13:20:00Z',
            next_deadline: '2023-06-28T00:00:00Z',
            next_deadline_title: 'Submit Appeal Brief'
          }
        ];
        setCases(mockCases);
        setLoading(false);
      }, 1000);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch assigned cases',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      setLoading(false);
    }
  };

  const fetchUpcomingDeadlines = async () => {
    try {
      // This would be an API call to get upcoming deadlines
      // For now, using mock data
      setTimeout(() => {
        const mockDeadlines = [
          {
            id: '1',
            case_id: '1',
            case_title: 'Smith v. Johnson',
            title: 'File Motion for Support',
            due_date: '2023-06-25T00:00:00Z',
            priority: 'HIGH',
            status: 'PENDING',
          },
          {
            id: '2',
            case_id: '2',
            case_title: 'Housing Rights Coalition',
            title: 'Submit Evidence Collection',
            due_date: '2023-06-20T00:00:00Z',
            priority: 'MEDIUM',
            status: 'PENDING',
          },
          {
            id: '3',
            case_id: '3',
            case_title: 'Estate of Williams',
            title: 'File Probate Petition',
            due_date: '2023-06-30T00:00:00Z',
            priority: 'MEDIUM',
            status: 'PENDING',
          },
          {
            id: '4',
            case_id: '4',
            case_title: 'Reynolds Immigration Matter',
            title: 'USCIS Interview Preparation',
            due_date: '2023-07-05T00:00:00Z',
            priority: 'HIGH',
            status: 'PENDING',
          },
          {
            id: '5',
            case_id: '5',
            case_title: 'Thompson Benefits Appeal',
            title: 'Submit Appeal Brief',
            due_date: '2023-06-28T00:00:00Z',
            priority: 'CRITICAL',
            status: 'PENDING',
          }
        ];
        setUpcomingDeadlines(mockDeadlines);
      }, 1000);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch upcoming deadlines',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const fetchRecentDocuments = async () => {
    try {
      // This would be an API call to get recent documents
      // For now, using mock data
      setTimeout(() => {
        const mockDocuments = [
          {
            id: '1',
            case_id: '1',
            case_title: 'Smith v. Johnson',
            title: 'Child Support Motion',
            created_at: '2023-06-14T16:30:00Z',
            status: 'DRAFT',
            file_format: 'pdf'
          },
          {
            id: '2',
            case_id: '2',
            case_title: 'Housing Rights Coalition',
            title: 'Tenant Rights Declaration',
            created_at: '2023-06-09T11:45:00Z',
            status: 'FINAL',
            file_format: 'pdf'
          },
          {
            id: '3',
            case_id: '3',
            case_title: 'Estate of Williams',
            title: 'Last Will and Testament',
            created_at: '2023-06-04T09:20:00Z',
            status: 'FINAL',
            file_format: 'pdf'
          },
          {
            id: '4',
            case_id: '4',
            case_title: 'Reynolds Immigration Matter',
            title: 'Form I-485 Application',
            created_at: '2023-06-11T14:15:00Z',
            status: 'DRAFT',
            file_format: 'pdf'
          },
          {
            id: '5',
            case_id: '5',
            case_title: 'Thompson Benefits Appeal',
            title: 'Appeal Submission Letter',
            created_at: '2023-06-07T10:10:00Z',
            status: 'FINAL',
            file_format: 'pdf'
          }
        ];
        setRecentDocuments(mockDocuments);
      }, 1000);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch recent documents',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleCaseClick = (caseId) => {
    navigate(`/cases/${caseId}`);
  };

  const handleDeadlineClick = (deadlineId, caseId) => {
    navigate(`/cases/${caseId}?tab=deadlines&highlight=${deadlineId}`);
  };

  const handleDocumentClick = (documentId, caseId) => {
    navigate(`/documents/${documentId}?case=${caseId}`);
  };

  const handleNewCase = () => {
    navigate('/cases/new');
  };

  const handleGenerateDocument = (caseId) => {
    setSelectedCaseId(caseId);
    onOpen();
  };

  const confirmGenerateDocument = () => {
    setGeneratingDocument(true);
    // This would call the document generation API
    setTimeout(() => {
      setGeneratingDocument(false);
      onClose();
      toast({
        title: 'Document Generated',
        description: 'New document has been created and saved as a draft',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      // Refresh documents list
      fetchRecentDocuments();
    }, 2000);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return <Box p={8}>Loading...</Box>;
  }

  return (
    <Container maxW="container.xl" py={8}>
      <HStack justify="space-between" mb={8}>
        <Heading size="lg">Attorney Dashboard</Heading>
        <Button leftIcon={<AddIcon />} colorScheme="blue" onClick={handleNewCase}>
          New Case
        </Button>
      </HStack>

      <Tabs variant="line" colorScheme="blue" isLazy>
        <TabList>
          <Tab>My Cases</Tab>
          <Tab>Deadlines</Tab>
          <Tab>Documents</Tab>
          <Tab>Calendar</Tab>
        </TabList>

        <TabPanels>
          {/* Cases Tab */}
          <TabPanel>
            <VStack spacing={4} align="stretch">
              <Box overflowX="auto">
                <Table variant="simple">
                  <Thead>
                    <Tr>
                      <Th>Case Title</Th>
                      <Th>Client</Th>
                      <Th>Type</Th>
                      <Th>Status</Th>
                      <Th>Last Updated</Th>
                      <Th>Next Deadline</Th>
                      <Th>Actions</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {cases.map((caseItem) => (
                      <Tr key={caseItem.id} _hover={{ bg: 'gray.50', cursor: 'pointer' }}>
                        <Td onClick={() => handleCaseClick(caseItem.id)}>{caseItem.title}</Td>
                        <Td>{caseItem.client}</Td>
                        <Td>{caseItem.case_type}</Td>
                        <Td>
                          <Badge colorScheme={statusColors[caseItem.status]}>{caseItem.status}</Badge>
                        </Td>
                        <Td>{formatDate(caseItem.updated_at)}</Td>
                        <Td>
                          <VStack align="start" spacing={0}>
                            <Text>{formatDate(caseItem.next_deadline)}</Text>
                            <Text fontSize="sm" color="gray.600">{caseItem.next_deadline_title}</Text>
                          </VStack>
                        </Td>
                        <Td>
                          <HStack spacing={2}>
                            <IconButton
                              aria-label="View case"
                              icon={<ViewIcon />}
                              size="sm"
                              onClick={() => handleCaseClick(caseItem.id)}
                            />
                            <IconButton
                              aria-label="Generate document"
                              icon={<AttachmentIcon />}
                              size="sm"
                              onClick={() => handleGenerateDocument(caseItem.id)}
                            />
                          </HStack>
                        </Td>
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              </Box>
            </VStack>
          </TabPanel>

          {/* Deadlines Tab */}
          <TabPanel>
            <VStack spacing={4} align="stretch">
              <DeadlineReminders />
              <Box overflowX="auto" mt={4}>
                <Heading size="md" mb={4}>All Upcoming Deadlines</Heading>
                <Table variant="simple">
                  <Thead>
                    <Tr>
                      <Th>Deadline</Th>
                      <Th>Case</Th>
                      <Th>Due Date</Th>
                      <Th>Priority</Th>
                      <Th>Status</Th>
                      <Th>Actions</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {upcomingDeadlines.map((deadline) => (
                      <Tr key={deadline.id} _hover={{ bg: 'gray.50', cursor: 'pointer' }}>
                        <Td onClick={() => handleDeadlineClick(deadline.id, deadline.case_id)}>
                          {deadline.title}
                        </Td>
                        <Td>{deadline.case_title}</Td>
                        <Td>{formatDate(deadline.due_date)}</Td>
                        <Td>
                          <Badge colorScheme={priorityColors[deadline.priority]}>{deadline.priority}</Badge>
                        </Td>
                        <Td>
                          <Badge colorScheme={deadline.status === 'COMPLETED' ? 'green' : 'blue'}>
                            {deadline.status}
                          </Badge>
                        </Td>
                        <Td>
                          <HStack spacing={2}>
                            <IconButton
                              aria-label="View deadline"
                              icon={<ViewIcon />}
                              size="sm"
                              onClick={() => handleDeadlineClick(deadline.id, deadline.case_id)}
                            />
                            <IconButton
                              aria-label="Edit deadline"
                              icon={<EditIcon />}
                              size="sm"
                              onClick={() => handleDeadlineClick(deadline.id, deadline.case_id)}
                            />
                          </HStack>
                        </Td>
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              </Box>
            </VStack>
          </TabPanel>

          {/* Documents Tab */}
          <TabPanel>
            <VStack spacing={4} align="stretch">
              <Flex justify="space-between">
                <Heading size="md">Recent Documents</Heading>
                <Button 
                  colorScheme="blue" 
                  size="sm"
                  leftIcon={<AddIcon />}
                  onClick={() => navigate('/documents/create')}
                >
                  New Document
                </Button>
              </Flex>
              <Box overflowX="auto">
                <Table variant="simple">
                  <Thead>
                    <Tr>
                      <Th>Document Title</Th>
                      <Th>Case</Th>
                      <Th>Created Date</Th>
                      <Th>Status</Th>
                      <Th>Actions</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {recentDocuments.map((document) => (
                      <Tr key={document.id} _hover={{ bg: 'gray.50', cursor: 'pointer' }}>
                        <Td onClick={() => handleDocumentClick(document.id, document.case_id)}>
                          {document.title}
                        </Td>
                        <Td>{document.case_title}</Td>
                        <Td>{formatDate(document.created_at)}</Td>
                        <Td>
                          <Badge colorScheme={document.status === 'FINAL' ? 'green' : 'orange'}>
                            {document.status}
                          </Badge>
                        </Td>
                        <Td>
                          <HStack spacing={2}>
                            <IconButton
                              aria-label="View document"
                              icon={<ViewIcon />}
                              size="sm"
                              onClick={() => handleDocumentClick(document.id, document.case_id)}
                            />
                            <IconButton
                              aria-label="Edit document"
                              icon={<EditIcon />}
                              size="sm"
                              onClick={() => handleDocumentClick(document.id, document.case_id)}
                            />
                            <IconButton
                              aria-label="Download document"
                              icon={<DownloadIcon />}
                              size="sm"
                              onClick={() => {
                                toast({
                                  title: 'Downloading',
                                  description: `Downloading ${document.title}.${document.file_format}`,
                                  status: 'info',
                                  duration: 3000,
                                  isClosable: true,
                                });
                              }}
                            />
                          </HStack>
                        </Td>
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              </Box>
            </VStack>
          </TabPanel>

          {/* Calendar Tab */}
          <TabPanel>
            <Box height="700px">
              <CalendarScheduler />
            </Box>
          </TabPanel>
        </TabPanels>
      </Tabs>

      {/* Document Generation Modal */}
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Generate Document</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Text>
              Generate a new document for the selected case? This will take you to the document generator where you can select a template and fill in required information.
            </Text>
          </ModalBody>

          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>
              Cancel
            </Button>
            <Button 
              colorScheme="blue" 
              onClick={confirmGenerateDocument} 
              isLoading={generatingDocument}
            >
              Continue
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Container>
  );
};

export default AttorneyDashboardPage; 