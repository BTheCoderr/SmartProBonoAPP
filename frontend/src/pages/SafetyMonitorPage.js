import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  Heading,
  Text,
  Button,
  Card,
  CardBody,
  Flex,
  Badge,
  Avatar,
  Divider,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Icon,
  useToast,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Spinner,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react';
import {
  FaHome,
  FaPhone,
  FaArrowLeft,
  FaFileAlt,
  FaShieldAlt,
  FaMapMarkedAlt,
} from 'react-icons/fa';
import axios from 'axios';
import SafetyMonitorChat from '../components/SafetyMonitorChat';
import { logInfo } from '../utils/logger';

const SafetyMonitorPage = () => {
  const { caseId } = useParams();
  const navigate = useNavigate();
  const toast = useToast();
  const [caseData, setCaseData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  // Mock client and lawyer data (in a real app, this would come from the API)
  const clientInfo = {
    id: '123',
    name: 'Jane Doe',
    avatar: 'https://bit.ly/broken-link',
    phone: '(555) 123-4567',
    email: 'jane.doe@example.com',
  };

  const lawyerInfo = {
    id: '456',
    name: 'Atty. Michael Rodriguez',
    avatar: 'https://bit.ly/broken-link',
    phone: '(555) 987-6543',
    specialization: 'Immigration Law',
  };

  const logMessage = (message) => {
    if (process.env.NODE_ENV !== 'production') {
      logInfo(message);
    }
  };

  useEffect(() => {
    // In a real app, this would fetch case data from an API
    const fetchCaseData = async () => {
      setIsLoading(true);
      try {
        // Simulate API call
        // const response = await axios.get(`/api/case/${caseId}`);

        // Mock data for demonstration
        const mockData = {
          id: caseId,
          title: 'Immigration Status Consultation',
          status: 'Active',
          priority: 'URGENT',
          createdAt: '2023-05-15T10:30:00Z',
          updatedAt: '2023-05-17T14:45:00Z',
          description:
            'Client seeking assistance with immigration status following recent change in circumstances.',
          clientId: clientInfo.id,
          lawyerId: lawyerInfo.id,
          documents: [
            { id: 'd1', name: 'Visa Application.pdf', addedAt: '2023-05-15T11:30:00Z' },
            { id: 'd2', name: 'Supporting Documentation.zip', addedAt: '2023-05-16T09:15:00Z' },
          ],
          location: {
            latitude: 37.7749,
            longitude: -122.4194,
            address: 'San Francisco, CA',
          },
        };

        setTimeout(() => {
          setCaseData(mockData);
          setIsLoading(false);
        }, 800);
      } catch (err) {
        setError(err.message || 'Failed to load case data');
        setIsLoading(false);
        toast({
          title: 'Error',
          description: 'Failed to load case information.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    };

    fetchCaseData();
  }, [caseId, toast]);

  const handleSendSOS = location => {
    logInfo('SOS requested with location:', location);
    toast({
      title: 'SOS Alert Sent',
      description: 'Emergency alert has been sent to the support team.',
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
  };

  const handleLocationShare = location => {
    logInfo('Location shared:', location);
    toast({
      title: 'Location Shared',
      description: 'Your location is now being shared with the support team.',
      status: 'info',
      duration: 3000,
      isClosable: true,
    });
  };

  const handleAddCompanion = companions => {
    logInfo('Companions added:', companions);
    toast({
      title: 'Companions Added',
      description: `${companions.length} people can now monitor this conversation.`,
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  if (isLoading) {
    return (
      <Container maxW="container.xl" py={8}>
        <Flex justify="center" align="center" h="60vh" direction="column">
          <Spinner size="xl" />
          <Text mt={4}>Loading case information...</Text>
        </Flex>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxW="container.xl" py={8}>
        <Alert status="error">
          <AlertIcon />
          <AlertTitle mr={2}>Error!</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
        <Button mt={4} leftIcon={<FaArrowLeft />} onClick={() => navigate('/cases')}>
          Back to Cases
        </Button>
      </Container>
    );
  }

  return (
    <Container maxW="container.xl" py={6}>
      {/* Breadcrumbs Navigation */}
      <Breadcrumb mb={6} fontSize="sm">
        <BreadcrumbItem>
          <BreadcrumbLink href="/dashboard">
            <Icon as={FaHome} mr={1} />
            Dashboard
          </BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbItem>
          <BreadcrumbLink href="/cases">Cases</BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbItem isCurrentPage>
          <BreadcrumbLink href="#">Safety Monitor</BreadcrumbLink>
        </BreadcrumbItem>
      </Breadcrumb>

      <Grid templateColumns={{ base: '1fr', lg: '350px 1fr' }} gap={6}>
        {/* Left sidebar with case info */}
        <Box>
          <Button
            leftIcon={<FaArrowLeft />}
            variant="outline"
            mb={4}
            onClick={() => navigate(`/cases/${caseId}`)}
          >
            Back to Case
          </Button>

          <Card mb={4}>
            <CardBody>
              <Heading size="md" mb={4}>
                Case Information
              </Heading>

              <Badge colorScheme={caseData?.priority === 'URGENT' ? 'red' : 'blue'} mb={2}>
                {caseData?.priority}
              </Badge>

              <Heading size="lg" mb={2}>
                {caseData?.title}
              </Heading>
              <Text color="gray.600" mb={4}>
                {caseData?.description}
              </Text>

              <Divider mb={4} />

              <Box mb={4}>
                <Text fontWeight="bold" mb={2}>
                  Client
                </Text>
                <Flex align="center">
                  <Avatar name={clientInfo.name} size="sm" mr={2} />
                  <Box>
                    <Text>{clientInfo.name}</Text>
                    <Text fontSize="sm" color="gray.500">
                      {clientInfo.phone}
                    </Text>
                  </Box>
                </Flex>
              </Box>

              <Box mb={4}>
                <Text fontWeight="bold" mb={2}>
                  Support Team
                </Text>
                <Flex align="center">
                  <Avatar name={lawyerInfo.name} size="sm" mr={2} />
                  <Box>
                    <Text>{lawyerInfo.name}</Text>
                    <Text fontSize="sm" color="gray.500">
                      {lawyerInfo.specialization}
                    </Text>
                  </Box>
                </Flex>
              </Box>

              <Divider mb={4} />

              <Box>
                <Text fontWeight="bold" mb={2}>
                  Safety Instructions
                </Text>
                <Box bg="gray.50" p={3} borderRadius="md" fontSize="sm">
                  <Text mb={2}>
                    <Icon as={FaShieldAlt} mr={2} color="green.500" />
                    Use the SOS button in an emergency
                  </Text>
                  <Text mb={2}>
                    <Icon as={FaMapMarkedAlt} mr={2} color="blue.500" />
                    Share your location when requested
                  </Text>
                  <Text>
                    <Icon as={FaPhone} mr={2} color="red.500" />
                    Call 911 for immediate life-threatening emergencies
                  </Text>
                </Box>
              </Box>
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <Heading size="md" mb={4}>
                Documents
              </Heading>
              {caseData?.documents?.map(doc => (
                <Flex
                  key={doc.id}
                  align="center"
                  mb={2}
                  p={2}
                  borderRadius="md"
                  _hover={{ bg: 'gray.50' }}
                >
                  <Icon as={FaFileAlt} mr={2} color="blue.500" />
                  <Box>
                    <Text>{doc.name}</Text>
                    <Text fontSize="xs" color="gray.500">
                      Added: {new Date(doc.addedAt).toLocaleDateString()}
                    </Text>
                  </Box>
                </Flex>
              ))}
            </CardBody>
          </Card>
        </Box>

        {/* Main content area - Chat and safety monitoring */}
        <Box borderWidth="1px" borderRadius="lg" overflow="hidden" height="80vh">
          <Tabs
            isFitted
            variant="enclosed"
            colorScheme="blue"
            index={activeTab}
            onChange={index => setActiveTab(index)}
          >
            <TabList>
              <Tab>Safety Monitor</Tab>
              <Tab>Case Notes</Tab>
            </TabList>
            <TabPanels height="calc(80vh - 42px)">
              <TabPanel p={0} height="100%">
                <SafetyMonitorChat
                  caseId={caseId}
                  clientInfo={clientInfo}
                  lawyerInfo={lawyerInfo}
                  onSendSOS={handleSendSOS}
                  onLocationShare={handleLocationShare}
                  onAddCompanion={handleAddCompanion}
                />
              </TabPanel>
              <TabPanel>
                <Box p={4}>
                  <Heading size="md" mb={4}>
                    Case Notes
                  </Heading>
                  <Text color="gray.500">
                    This tab would contain case notes and documentation related to this client's
                    situation.
                  </Text>
                </Box>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Box>
      </Grid>
    </Container>
  );
};

export default SafetyMonitorPage;
