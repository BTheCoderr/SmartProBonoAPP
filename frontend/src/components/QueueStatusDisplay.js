import React, { useState, useEffect } from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Badge,
  Progress,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Grid,
  GridItem,
  useColorModeValue,
  Heading,
  Icon,
  Tooltip,
} from '@chakra-ui/react';
import { FaClock, FaExclamationTriangle, FaCheckCircle } from 'react-icons/fa';
import axios from 'axios';
import PropTypes from 'prop-types';
const PriorityBadge = ({ priority, count }) => {
  const colors = {
    URGENT: 'red',
    HIGH: 'orange',
    MEDIUM: 'yellow',
    LOW: 'green',
  };
  const badgeColor = useColorModeValue(`${colors[priority]}.100`, `${colors[priority]}.800`);
  return (
    <Badge
      colorScheme={colors[priority]}
      fontSize="sm"
      px={3}
      py={1}
      borderRadius="full"
      display="flex"
      alignItems="center"
      justifyContent="center"
      gap={2}
    >
      {priority}
      <Box as="span" bg={badgeColor} px={2} py={0.5} borderRadius="full" fontSize="xs">
        {count}
      </Box>
    </Badge>
  );
};
const QueueStatusDisplay = () => {
  const [queueStatus, setQueueStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  const fetchQueueStatus = async () => {
    try {
      const response = await axios.get('/api/priority-queue/status');
      setQueueStatus(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch queue status');
      console.error('Error fetching queue status:', err);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    fetchQueueStatus();
    // Refresh every 30 seconds
    const interval = setInterval(fetchQueueStatus, 30000);
    return () => clearInterval(interval);
  }, []);
  if (loading) {
    return (
      <Box p={4}>
        <Progress size="xs" isIndeterminate />
      </Box>
    );
  }
  if (error) {
    return (
      <Box p={4} textAlign="center" color="red.500">
        <Icon as={FaExclamationTriangle} mr={2} />
        {error}
      </Box>
    );
  }
  const totalCases = queueStatus?.total_cases || 0;
  const priorityBreakdown = queueStatus?.priority_breakdown || {};
  return (
    <Box p={6} borderRadius="lg" bg={bgColor} boxShadow="sm" border="1px" borderColor={borderColor}>
      <VStack spacing={6} align="stretch">
        <HStack justify="space-between" align="center">
          <Heading size="md">Queue Status</Heading>
          <Tooltip label="Last updated">
            <HStack spacing={1} color="gray.500">
              <Icon as={FaClock} />
              <Text fontSize="sm">{new Date().toLocaleTimeString()}</Text>
            </HStack>
          </Tooltip>
        </HStack>
        <Grid templateColumns="repeat(2, 1fr)" gap={4}>
          <GridItem>
            <Stat>
              <StatLabel>Total Cases</StatLabel>
              <StatNumber>{totalCases}</StatNumber>
              <StatHelpText>In queue</StatHelpText>
            </Stat>
          </GridItem>
          <GridItem>
            <Stat>
              <StatLabel>Next Case</StatLabel>
              <StatNumber fontSize="lg">
                {queueStatus?.next_case ? (
                  <HStack>
                    <Icon as={FaCheckCircle} color="green.500" />
                    <Text>{queueStatus.next_case}</Text>
                  </HStack>
                ) : (
                  'No cases'
                )}
              </StatNumber>
              <StatHelpText>Ready for assignment</StatHelpText>
            </Stat>
          </GridItem>
        </Grid>
        <Box>
          <Text mb={2} fontWeight="medium">
            Priority Breakdown
          </Text>
          <VStack spacing={2} align="stretch">
            {Object.entries(priorityBreakdown).map(([priority, count]) => (
              <HStack key={priority} justify="space-between">
                <PriorityBadge priority={priority} count={count} />
                <Progress
                  value={(count / totalCases) * 100}
                  size="sm"
                  colorScheme={
                    priority === 'URGENT'
                      ? 'red'
                      : priority === 'HIGH'
                        ? 'orange'
                        : priority === 'MEDIUM'
                          ? 'yellow'
                          : 'green'
                  }
                  flex={1}
                  ml={4}
                />
              </HStack>
            ))}
          </VStack>
        </Box>
      </VStack>
    </Box>
  );
};

// Define PropTypes
PriorityBadge.propTypes = {
  /** TODO: Add description */
  priority: PropTypes.any,
  /** TODO: Add description */
  count: PropTypes.any,
};

export default QueueStatusDisplay;