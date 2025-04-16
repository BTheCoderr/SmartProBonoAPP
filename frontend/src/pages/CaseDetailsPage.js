import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Heading,
  Text,
  VStack,
  HStack,
  Button,
  useToast,
  Badge,
  Select,
  Textarea,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Divider,
  List,
  ListItem,
  IconButton,
  useDisclosure,
} from '@chakra-ui/react';
import { EditIcon, AddIcon } from '@chakra-ui/icons';
import {
  getCaseById,
  updateCase,
  assignCase,
  updatePriority,
  getCaseHistory,
  addTimelineEvent,
  CaseStatus,
  CasePriority,
} from '../services/caseService';
import TimelineList from '../components/TimelineList';
import DocumentList from '../components/DocumentList';
import NextStepsList from '../components/NextStepsList';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';
import AssignCaseModal from '../components/AssignCaseModal';
const CaseDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const toast = useToast();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [statusNote, setStatusNote] = useState('');
  const [priorityNote, setPriorityNote] = useState('');
  const [history, setHistory] = useState([]);
  const [updating, setUpdating] = useState(false);
  // Fetch case data and history
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [caseDetails, caseHistory] = await Promise.all([getCaseById(id), getCaseHistory(id)]);
        setCaseData(caseDetails);
        setHistory(caseHistory);
        setError(null);
      } catch (err) {
        setError(err.message);
        toast({
          title: 'Error',
          description: err.message,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id, toast]);
  // Handle status update
  const handleStatusUpdate = async newStatus => {
    setUpdating(true);
    try {
      const updatedCase = await updateCase(id, {
        status: newStatus,
        notes: statusNote,
      });
      setCaseData(updatedCase);
      setStatusNote('');
      toast({
        title: 'Status Updated',
        description: `Case status updated to ${newStatus}`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      // Refresh history
      const newHistory = await getCaseHistory(id);
      setHistory(newHistory);
    } catch (err) {
      toast({
        title: 'Error',
        description: err.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setUpdating(false);
    }
  };
  // Handle priority update
  const handlePriorityUpdate = async newPriority => {
    setUpdating(true);
    try {
      const updatedCase = await updatePriority(id, newPriority, priorityNote);
      setCaseData(updatedCase);
      setPriorityNote('');
      toast({
        title: 'Priority Updated',
        description: `Case priority updated to ${newPriority}`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (err) {
      toast({
        title: 'Error',
        description: err.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setUpdating(false);
    }
  };
  // Handle case assignment
  const handleAssign = async (userId, notes) => {
    setUpdating(true);
    try {
      const updatedCase = await assignCase(id, userId, notes);
      setCaseData(updatedCase);
      onClose();
      toast({
        title: 'Case Assigned',
        description: 'Case has been successfully assigned',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (err) {
      toast({
        title: 'Error',
        description: err.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setUpdating(false);
    }
  };
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorAlert message={error} />;
  if (!caseData) return null;
  const getStatusColor = status => {
    const colors = {
      [CaseStatus.NEW]: 'blue',
      [CaseStatus.IN_PROGRESS]: 'green',
      [CaseStatus.UNDER_REVIEW]: 'purple',
      [CaseStatus.ON_HOLD]: 'orange',
      [CaseStatus.CLOSED]: 'gray',
    };
    return colors[status] || 'gray';
  };
  const getPriorityColor = priority => {
    const colors = {
      [CasePriority.LOW]: 'green',
      [CasePriority.MEDIUM]: 'blue',
      [CasePriority.HIGH]: 'orange',
      [CasePriority.URGENT]: 'red',
    };
    return colors[priority] || 'gray';
  };
  return (
    <Container maxW="container.xl" py={5}>
      <VStack spacing={6} align="stretch">
        {/* Header */}
        <HStack justify="space-between">
          <VStack align="start" spacing={2}>
            <Heading size="lg">{caseData.title}</Heading>
            <HStack spacing={4}>
              <Badge colorScheme={getStatusColor(caseData.status)}>{caseData.status}</Badge>
              <Badge colorScheme={getPriorityColor(caseData.priority)}>{caseData.priority}</Badge>
              <Text color="gray.600">Case #{caseData.id}</Text>
            </HStack>
          </VStack>
          <Button leftIcon={<EditIcon />} onClick={() => navigate(`/cases/${id}/edit`)}>
            Edit Case
          </Button>
        </HStack>
        {/* Status and Priority Controls */}
        <Box p={4} borderWidth={1} borderRadius="md">
          <VStack spacing={4} align="stretch">
            <HStack justify="space-between">
              <Box flex={1}>
                <Text fontWeight="bold" mb={2}>
                  Status
                </Text>
                <Select
                  value={caseData.status}
                  onChange={e => handleStatusUpdate(e.target.value)}
                  isDisabled={updating}
                >
                  {Object.values(CaseStatus).map(status => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </Select>
                <Textarea
                  mt={2}
                  placeholder="Add a note about this status change..."
                  value={statusNote}
                  onChange={e => setStatusNote(e.target.value)}
                  size="sm"
                />
              </Box>
              <Box flex={1} ml={4}>
                <Text fontWeight="bold" mb={2}>
                  Priority
                </Text>
                <Select
                  value={caseData.priority}
                  onChange={e => handlePriorityUpdate(e.target.value)}
                  isDisabled={updating}
                >
                  {Object.values(CasePriority).map(priority => (
                    <option key={priority} value={priority}>
                      {priority}
                    </option>
                  ))}
                </Select>
                <Textarea
                  mt={2}
                  placeholder="Add a note about this priority change..."
                  value={priorityNote}
                  onChange={e => setPriorityNote(e.target.value)}
                  size="sm"
                />
              </Box>
            </HStack>
            <Button leftIcon={<AddIcon />} onClick={onOpen} isDisabled={updating}>
              Assign Case
            </Button>
          </VStack>
        </Box>
        {/* Case Details Tabs */}
        <Tabs>
          <TabList>
            <Tab>Details</Tab>
            <Tab>History</Tab>
            <Tab>Timeline</Tab>
            <Tab>Documents</Tab>
            <Tab>Next Steps</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <VStack align="stretch" spacing={4}>
                <Box>
                  <Text fontWeight="bold">Description</Text>
                  <Text>{caseData.description}</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold">Type</Text>
                  <Text>{caseData.type}</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold">Assigned To</Text>
                  <Text>{caseData.assigned_to?.name || 'Not assigned'}</Text>
                </Box>
              </VStack>
            </TabPanel>
            <TabPanel>
              <List spacing={3}>
                {history.map((event, index) => (
                  <ListItem key={index}>
                    <HStack>
                      <Badge colorScheme={getStatusColor(event.status)}>{event.status}</Badge>
                      <Text>{event.timestamp}</Text>
                      {event.notes && <Text color="gray.600">- {event.notes}</Text>}
                    </HStack>
                  </ListItem>
                ))}
              </List>
            </TabPanel>
            <TabPanel>
              <TimelineList
                caseId={id}
                timeline={caseData.timeline}
                onUpdate={timeline => setCaseData({ ...caseData, timeline })}
              />
            </TabPanel>
            <TabPanel>
              <DocumentList
                caseId={id}
                documents={caseData.documents}
                onUpdate={documents => setCaseData({ ...caseData, documents })}
              />
            </TabPanel>
            <TabPanel>
              <NextStepsList
                caseId={id}
                nextSteps={caseData.next_steps}
                onUpdate={next_steps => setCaseData({ ...caseData, next_steps })}
              />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
      {/* Assign Case Modal */}
      <AssignCaseModal
        isOpen={isOpen}
        onClose={onClose}
        onAssign={handleAssign}
        isLoading={updating}
      />
    </Container>
  );
};
export default CaseDetailsPage;