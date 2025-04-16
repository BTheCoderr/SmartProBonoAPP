import React, { useState, useEffect } from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Grid,
  GridItem,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Heading,
  Icon,
  Tooltip,
  useColorModeValue,
  Divider,
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
  Spinner,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Button,
  Flex,
} from '@chakra-ui/react';
import {
  FaClock,
  FaExclamationTriangle,
  FaChartBar,
  FaUser,
  FaUserTie,
  FaHistory,
  FaDatabase,
  FaChartLine,
  FaSync,
} from 'react-icons/fa';
import axios from 'axios';
// Chart component using recharts
import {
import PropTypes from 'prop-types';
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
const COLORS = ['#FF5252', '#FF9800', '#FFC107', '#4CAF50', '#2196F3', '#673AB7', '#9C27B0'];
const PriorityBadge = ({ priority }) => {
  const colors = {
    URGENT: 'red',
    HIGH: 'orange',
    MEDIUM: 'yellow',
    LOW: 'green',
  };
  return (
    <Badge colorScheme={colors[priority] || 'gray'} px={2} py={0.5} borderRadius="full">
      {priority}
    </Badge>
  );
};
const QueueAnalyticsDashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);
  const [auditLoading, setAuditLoading] = useState(true);
  const backgroundColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  const textColor = useColorModeValue('gray.800', 'white');
  const subTextColor = useColorModeValue('gray.600', 'gray.400');
  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/priority-queue/analytics');
      setAnalytics(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch queue analytics');
      console.error('Error fetching queue analytics:', err);
    } finally {
      setLoading(false);
    }
  };
  const fetchAuditLogs = async () => {
    try {
      setAuditLoading(true);
      const response = await axios.get('/api/priority-queue/audit');
      setAuditLogs(response.data);
    } catch (err) {
      console.error('Error fetching audit logs:', err);
    } finally {
      setAuditLoading(false);
    }
  };
  useEffect(() => {
    fetchAnalytics();
    fetchAuditLogs();
    // Refresh every 5 minutes
    const interval = setInterval(fetchAnalytics, 300000);
    return () => clearInterval(interval);
  }, []);
  if (loading) {
    return (
      <Box p={6} textAlign="center">
        <Spinner size="xl" />
        <Text mt={4}>Loading analytics data...</Text>
      </Box>
    );
  }
  if (error) {
    return (
      <Alert
        status="error"
        variant="subtle"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        textAlign="center"
        height="200px"
      >
        <AlertIcon boxSize="40px" mr={0} />
        <AlertTitle mt={4} mb={1} fontSize="lg">
          Analytics Error
        </AlertTitle>
        <AlertDescription maxWidth="sm">
          {error}
          <Button leftIcon={<FaSync />} mt={4} onClick={fetchAnalytics}>
            Retry
          </Button>
        </AlertDescription>
      </Alert>
    );
  }
  const formatPriorityDataForChart = () => {
    if (!analytics || !analytics.priority_distribution) return [];
    return Object.entries(analytics.priority_distribution).map(([name, value]) => ({
      name,
      value,
    }));
  };
  const formatCaseTypeDataForChart = () => {
    if (!analytics || !analytics.situation_type_distribution) return [];
    return Object.entries(analytics.situation_type_distribution).map(([name, value]) => ({
      name,
      value,
    }));
  };
  const formatQueueHistoryForChart = () => {
    if (!analytics || !analytics.queue_history) return [];
    return analytics.queue_history
      .slice(0, 10)
      .map(item => ({
        timestamp: new Date(item.timestamp).toLocaleDateString(),
        urgent: item.urgent_cases,
        high: item.high_cases,
        medium: item.medium_cases,
        low: item.low_cases,
        total: item.total_cases,
      }))
      .reverse();
  };
  const formatTimeAsHoursMinutes = minutes => {
    if (!minutes) return 'N/A';
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = Math.round(minutes % 60);
    if (hours === 0) {
      return `${remainingMinutes} min`;
    }
    return `${hours}h ${remainingMinutes}m`;
  };
  return (
    <Box w="100%">
      <Tabs variant="enclosed" colorScheme="blue">
        <TabList>
          <Tab>
            <Icon as={FaChartBar} mr={2} /> Overview
          </Tab>
          <Tab>
            <Icon as={FaUserTie} mr={2} /> Lawyer Performance
          </Tab>
          <Tab>
            <Icon as={FaHistory} mr={2} /> History
          </Tab>
          <Tab>
            <Icon as={FaDatabase} mr={2} /> Audit Logs
          </Tab>
        </TabList>
        <TabPanels>
          {/* Overview Tab */}
          <TabPanel>
            <VStack spacing={6} align="stretch">
              <HStack justify="space-between" align="center">
                <Heading size="lg">Queue Analytics Dashboard</Heading>
                <Tooltip label="Last updated">
                  <HStack spacing={1} color={subTextColor}>
                    <Icon as={FaClock} />
                    <Text fontSize="sm">{new Date().toLocaleTimeString()}</Text>
                  </HStack>
                </Tooltip>
              </HStack>
              <Grid
                templateColumns={{
                  base: 'repeat(1, 1fr)',
                  md: 'repeat(2, 1fr)',
                  lg: 'repeat(3, 1fr)',
                }}
                gap={6}
              >
                <GridItem>
                  <Box
                    p={5}
                    borderRadius="lg"
                    bg={backgroundColor}
                    boxShadow="md"
                    borderWidth="1px"
                    borderColor={borderColor}
                  >
                    <Stat>
                      <StatLabel fontSize="md">Active Cases</StatLabel>
                      <StatNumber fontSize="3xl">{analytics?.active_cases || 0}</StatNumber>
                      <StatHelpText>Currently in queue</StatHelpText>
                    </Stat>
                  </Box>
                </GridItem>
                <GridItem>
                  <Box
                    p={5}
                    borderRadius="lg"
                    bg={backgroundColor}
                    boxShadow="md"
                    borderWidth="1px"
                    borderColor={borderColor}
                  >
                    <Stat>
                      <StatLabel fontSize="md">Average Wait Time</StatLabel>
                      <StatNumber fontSize="2xl">
                        {formatTimeAsHoursMinutes(analytics?.average_wait_time_minutes)}
                      </StatNumber>
                      <StatHelpText>Across all priorities</StatHelpText>
                    </Stat>
                  </Box>
                </GridItem>
                <GridItem>
                  <Box
                    p={5}
                    borderRadius="lg"
                    bg={backgroundColor}
                    boxShadow="md"
                    borderWidth="1px"
                    borderColor={borderColor}
                  >
                    <Stat>
                      <StatLabel fontSize="md">Max Wait Time</StatLabel>
                      <StatNumber fontSize="2xl">
                        {formatTimeAsHoursMinutes(analytics?.max_wait_time_minutes)}
                      </StatNumber>
                      <StatHelpText>Longest currently waiting</StatHelpText>
                    </Stat>
                  </Box>
                </GridItem>
              </Grid>
              <Divider />
              <Grid templateColumns={{ base: 'repeat(1, 1fr)', lg: 'repeat(2, 1fr)' }} gap={6}>
                {/* Priority Distribution Chart */}
                <GridItem>
                  <Box
                    p={5}
                    borderRadius="lg"
                    bg={backgroundColor}
                    boxShadow="md"
                    borderWidth="1px"
                    borderColor={borderColor}
                    height="350px"
                  >
                    <Heading size="md" mb={4}>
                      Priority Distribution
                    </Heading>
                    <ResponsiveContainer width="100%" height="85%">
                      <PieChart>
                        <Pie
                          data={formatPriorityDataForChart()}
                          cx="50%"
                          cy="50%"
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                          nameKey="name"
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        >
                          {formatPriorityDataForChart().map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Legend />
                        <RechartsTooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                </GridItem>
                {/* Case Type Distribution Chart */}
                <GridItem>
                  <Box
                    p={5}
                    borderRadius="lg"
                    bg={backgroundColor}
                    boxShadow="md"
                    borderWidth="1px"
                    borderColor={borderColor}
                    height="350px"
                  >
                    <Heading size="md" mb={4}>
                      Case Type Distribution
                    </Heading>
                    <ResponsiveContainer width="100%" height="85%">
                      <BarChart
                        data={formatCaseTypeDataForChart()}
                        margin={{ top: 5, right: 30, left: 20, bottom: 50 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" angle={-45} textAnchor="end" height={60} />
                        <YAxis />
                        <RechartsTooltip />
                        <Bar dataKey="value" fill="#8884d8" name="Cases">
                          {formatCaseTypeDataForChart().map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </GridItem>
              </Grid>
              {/* Bottlenecks Table */}
              <Box
                p={5}
                borderRadius="lg"
                bg={backgroundColor}
                boxShadow="md"
                borderWidth="1px"
                borderColor={borderColor}
              >
                <Heading size="md" mb={4}>
                  Case Bottlenecks
                </Heading>
                <Table variant="simple" size="sm">
                  <Thead>
                    <Tr>
                      <Th>Situation Type</Th>
                      <Th>Average Wait</Th>
                      <Th>Case Count</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {analytics?.bottlenecks &&
                      analytics.bottlenecks.map((bottleneck, index) => (
                        <Tr key={index}>
                          <Td>{bottleneck.situation_type}</Td>
                          <Td>{formatTimeAsHoursMinutes(bottleneck.average_wait_minutes)}</Td>
                          <Td>{bottleneck.case_count}</Td>
                        </Tr>
                      ))}
                    {(!analytics?.bottlenecks || analytics.bottlenecks.length === 0) && (
                      <Tr>
                        <Td colSpan={3} textAlign="center">
                          No bottlenecks detected
                        </Td>
                      </Tr>
                    )}
                  </Tbody>
                </Table>
              </Box>
            </VStack>
          </TabPanel>
          {/* Lawyer Performance Tab */}
          <TabPanel>
            <VStack spacing={6} align="stretch">
              <Heading size="lg" mb={4}>
                Lawyer Response Performance
              </Heading>
              <Box
                p={5}
                borderRadius="lg"
                bg={backgroundColor}
                boxShadow="md"
                borderWidth="1px"
                borderColor={borderColor}
              >
                <Table variant="simple">
                  <Thead>
                    <Tr>
                      <Th>Lawyer ID</Th>
                      <Th>Total Cases</Th>
                      <Th>Avg. Resolution Time</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {analytics?.lawyer_performance &&
                      analytics.lawyer_performance.map((lawyer, index) => (
                        <Tr key={index}>
                          <Td>{lawyer.lawyer_id}</Td>
                          <Td>{lawyer.total_cases}</Td>
                          <Td>{formatTimeAsHoursMinutes(lawyer.avg_resolution_minutes)}</Td>
                        </Tr>
                      ))}
                    {(!analytics?.lawyer_performance ||
                      analytics.lawyer_performance.length === 0) && (
                      <Tr>
                        <Td colSpan={3} textAlign="center">
                          No lawyer performance data available
                        </Td>
                      </Tr>
                    )}
                  </Tbody>
                </Table>
              </Box>
            </VStack>
          </TabPanel>
          {/* History Tab */}
          <TabPanel>
            <VStack spacing={6} align="stretch">
              <Heading size="lg" mb={4}>
                Queue History
              </Heading>
              <Box
                p={5}
                borderRadius="lg"
                bg={backgroundColor}
                boxShadow="md"
                borderWidth="1px"
                borderColor={borderColor}
                height="400px"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={formatQueueHistoryForChart()}
                    margin={{ top: 5, right: 30, left: 20, bottom: 30 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="total"
                      stroke="#8884d8"
                      name="Total Cases"
                      strokeWidth={2}
                    />
                    <Line type="monotone" dataKey="urgent" stroke="#FF5252" name="Urgent" />
                    <Line type="monotone" dataKey="high" stroke="#FF9800" name="High" />
                    <Line type="monotone" dataKey="medium" stroke="#FFC107" name="Medium" />
                    <Line type="monotone" dataKey="low" stroke="#4CAF50" name="Low" />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
              <Box
                p={5}
                borderRadius="lg"
                bg={backgroundColor}
                boxShadow="md"
                borderWidth="1px"
                borderColor={borderColor}
              >
                <Heading size="md" mb={4}>
                  Historical Queue Data
                </Heading>
                <Table variant="simple" size="sm">
                  <Thead>
                    <Tr>
                      <Th>Date</Th>
                      <Th>Total</Th>
                      <Th>Urgent</Th>
                      <Th>High</Th>
                      <Th>Medium</Th>
                      <Th>Low</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {analytics?.queue_history &&
                      analytics.queue_history.map((history, index) => (
                        <Tr key={index}>
                          <Td>{new Date(history.timestamp).toLocaleString()}</Td>
                          <Td>{history.total_cases}</Td>
                          <Td>{history.urgent_cases}</Td>
                          <Td>{history.high_cases}</Td>
                          <Td>{history.medium_cases}</Td>
                          <Td>{history.low_cases}</Td>
                        </Tr>
                      ))}
                    {(!analytics?.queue_history || analytics.queue_history.length === 0) && (
                      <Tr>
                        <Td colSpan={6} textAlign="center">
                          No historical data available
                        </Td>
                      </Tr>
                    )}
                  </Tbody>
                </Table>
              </Box>
            </VStack>
          </TabPanel>
          {/* Audit Logs Tab */}
          <TabPanel>
            <VStack spacing={6} align="stretch">
              <Flex justify="space-between" align="center">
                <Heading size="lg">Audit Logs</Heading>
                <Button leftIcon={<FaSync />} onClick={fetchAuditLogs} size="sm">
                  Refresh
                </Button>
              </Flex>
              <Box
                p={5}
                borderRadius="lg"
                bg={backgroundColor}
                boxShadow="md"
                borderWidth="1px"
                borderColor={borderColor}
              >
                {auditLoading ? (
                  <Flex justify="center" align="center" height="200px">
                    <Spinner mr={3} />
                    <Text>Loading audit logs...</Text>
                  </Flex>
                ) : (
                  <Table variant="simple" size="sm">
                    <Thead>
                      <Tr>
                        <Th>Timestamp</Th>
                        <Th>Event Type</Th>
                        <Th>User ID</Th>
                        <Th>Details</Th>
                      </Tr>
                    </Thead>
                    <Tbody>
                      {auditLogs &&
                        auditLogs.map((log, index) => (
                          <Tr key={index}>
                            <Td>{new Date(log.timestamp).toLocaleString()}</Td>
                            <Td>{log.event_type}</Td>
                            <Td>{log.user_id}</Td>
                            <Td>
                              <Tooltip label={JSON.stringify(log.details, null, 2)}>
                                <Text cursor="pointer" textDecoration="underline">
                                  View Details
                                </Text>
                              </Tooltip>
                            </Td>
                          </Tr>
                        ))}
                      {(!auditLogs || auditLogs.length === 0) && (
                        <Tr>
                          <Td colSpan={4} textAlign="center">
                            No audit logs available
                          </Td>
                        </Tr>
                      )}
                    </Tbody>
                  </Table>
                )}
              </Box>
            </VStack>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

// Define PropTypes
PriorityBadge.propTypes = {
  /** TODO: Add description */
  priority: PropTypes.any,
};

export default QueueAnalyticsDashboard;