import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Heading,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Select,
  HStack,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  useToast,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from '@chakra-ui/react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import QueueAnalyticsDashboard from '../components/QueueAnalyticsDashboard';
import DeadlineReminders from '../components/DeadlineReminders';
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];
const statusColors = {
  NEW: 'blue',
  IN_PROGRESS: 'orange',
  UNDER_REVIEW: 'purple',
  ON_HOLD: 'yellow',
  CLOSED: 'green',
};
const DashboardPage = () => {
  const [timeRange, setTimeRange] = useState('month');
  const [metrics, setMetrics] = useState({
    totalCases: 0,
    activeCases: 0,
    closedCases: 0,
    averageResolutionTime: 0,
    casesByStatus: [],
    casesByType: [],
    casesTrend: [],
    topAttorneys: [],
  });
  const [loading, setLoading] = useState(true);
  const toast = useToast();
  useEffect(() => {
    fetchDashboardData();
  }, [timeRange, fetchDashboardData]);
  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      // In a real app, this would be an API call
      const data = {
        totalCases: 150,
        activeCases: 45,
        closedCases: 105,
        averageResolutionTime: 15,
        casesByStatus: [
          { name: 'NEW', value: 20 },
          { name: 'IN_PROGRESS', value: 15 },
          { name: 'UNDER_REVIEW', value: 5 },
          { name: 'ON_HOLD', value: 5 },
          { name: 'CLOSED', value: 105 },
        ],
        casesByType: [
          { name: 'Criminal Law', cases: 45 },
          { name: 'Family Law', cases: 35 },
          { name: 'Immigration', cases: 30 },
          { name: 'Civil Rights', cases: 25 },
          { name: 'Housing', cases: 15 },
        ],
        casesTrend: [
          { month: 'Jan', cases: 12 },
          { month: 'Feb', cases: 15 },
          { month: 'Mar', cases: 18 },
          { month: 'Apr', cases: 14 },
          { month: 'May', cases: 21 },
          { month: 'Jun', cases: 25 },
        ],
        topAttorneys: [
          { name: 'John Doe', cases: 15, success_rate: 92 },
          { name: 'Jane Smith', cases: 12, success_rate: 88 },
          { name: 'Mike Johnson', cases: 10, success_rate: 85 },
          { name: 'Sarah Wilson', cases: 8, success_rate: 90 },
        ],
      };
      setMetrics(data);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch dashboard data',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };
  const calculateTrend = (current, previous) => {
    const trend = ((current - previous) / previous) * 100;
    return trend.toFixed(1);
  };
  if (loading) {
    return <Box>Loading...</Box>;
  }
  return (
    <Container maxW="container.xl" py={8}>
      <Box mb={8}>
        <HStack justify="space-between" mb={8}>
          <Heading size="lg">Dashboard</Heading>
          <Select w="200px" value={timeRange} onChange={e => setTimeRange(e.target.value)}>
            <option value="week">Last Week</option>
            <option value="month">Last Month</option>
            <option value="quarter">Last Quarter</option>
            <option value="year">Last Year</option>
          </Select>
        </HStack>
        <Tabs variant="line" colorScheme="blue" mb={6}>
          <TabList>
            <Tab>Overview</Tab>
            <Tab>Queue Analytics</Tab>
          </TabList>
          <TabPanels>
            <TabPanel p={0} pt={4}>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6}>
                <Stat p={4} shadow="md" borderWidth="1px" borderRadius="lg">
                  <StatLabel>Total Cases</StatLabel>
                  <StatNumber>{metrics.totalCases}</StatNumber>
                  <StatHelpText>
                    <StatArrow type="increase" />
                    {calculateTrend(metrics.totalCases, metrics.totalCases - 10)}%
                  </StatHelpText>
                </Stat>
                <Stat p={4} shadow="md" borderWidth="1px" borderRadius="lg">
                  <StatLabel>Active Cases</StatLabel>
                  <StatNumber>{metrics.activeCases}</StatNumber>
                  <StatHelpText>
                    <StatArrow type="decrease" />
                    {calculateTrend(metrics.activeCases, metrics.activeCases + 5)}%
                  </StatHelpText>
                </Stat>
                <Stat p={4} shadow="md" borderWidth="1px" borderRadius="lg">
                  <StatLabel>Closed Cases</StatLabel>
                  <StatNumber>{metrics.closedCases}</StatNumber>
                  <StatHelpText>
                    <StatArrow type="increase" />
                    {calculateTrend(metrics.closedCases, metrics.closedCases - 15)}%
                  </StatHelpText>
                </Stat>
                <Stat p={4} shadow="md" borderWidth="1px" borderRadius="lg">
                  <StatLabel>Avg. Resolution Time</StatLabel>
                  <StatNumber>{metrics.averageResolutionTime} days</StatNumber>
                  <StatHelpText>
                    <StatArrow type="decrease" />
                    {calculateTrend(
                      metrics.averageResolutionTime,
                      metrics.averageResolutionTime + 2
                    )}
                    %
                  </StatHelpText>
                </Stat>
              </SimpleGrid>
              <Box mt={8} mb={8}>
                <DeadlineReminders />
              </Box>
              <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={8} mb={8} mt={8}>
                <Box p={6} shadow="md" borderWidth="1px" borderRadius="lg">
                  <Heading size="md" mb={4}>
                    Cases by Type
                  </Heading>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={metrics.casesByType}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="cases" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </Box>
                <Box p={6} shadow="md" borderWidth="1px" borderRadius="lg">
                  <Heading size="md" mb={4}>
                    Cases by Status
                  </Heading>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={metrics.casesByStatus}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={100}
                        label
                      >
                        {metrics.casesByStatus.map((entry, index) => (
                          <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
              </SimpleGrid>
              <Box p={6} shadow="md" borderWidth="1px" borderRadius="lg" mb={8}>
                <Heading size="md" mb={4}>
                  Case Trend
                </Heading>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={metrics.casesTrend}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="cases" fill="#82ca9d" />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
              <Box p={6} shadow="md" borderWidth="1px" borderRadius="lg">
                <Heading size="md" mb={4}>
                  Top Performing Attorneys
                </Heading>
                <Table variant="simple">
                  <Thead>
                    <Tr>
                      <Th>Attorney</Th>
                      <Th isNumeric>Cases Handled</Th>
                      <Th isNumeric>Success Rate</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {metrics.topAttorneys.map(attorney => (
                      <Tr key={attorney.name}>
                        <Td>{attorney.name}</Td>
                        <Td isNumeric>{attorney.cases}</Td>
                        <Td isNumeric>
                          <Badge colorScheme={attorney.success_rate >= 90 ? 'green' : 'orange'}>
                            {attorney.success_rate}%
                          </Badge>
                        </Td>
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              </Box>
            </TabPanel>
            <TabPanel p={0} pt={4}>
              <QueueAnalyticsDashboard />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
    </Container>
  );
};
export default DashboardPage;