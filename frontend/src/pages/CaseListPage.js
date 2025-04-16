import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Heading,
  Stack,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  Select,
  HStack,
  Input,
  Button,
  useToast,
  Spinner,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { getAllCases } from '../services/caseService';

const CaseListPage = () => {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    search: '',
  });
  const navigate = useNavigate();
  const toast = useToast();

  const statusOptions = ['NEW', 'IN_PROGRESS', 'UNDER_REVIEW', 'ON_HOLD', 'CLOSED'];
  const priorityOptions = ['LOW', 'MEDIUM', 'HIGH', 'URGENT'];

  const statusColors = {
    NEW: 'blue',
    IN_PROGRESS: 'orange',
    UNDER_REVIEW: 'purple',
    ON_HOLD: 'yellow',
    CLOSED: 'green',
  };

  const priorityColors = {
    LOW: 'gray',
    MEDIUM: 'blue',
    HIGH: 'orange',
    URGENT: 'red',
  };

  useEffect(() => {
    fetchCases();
  }, [filters, fetchCases]);

  const fetchCases = async () => {
    try {
      setLoading(true);
      const response = await getAllCases(filters);
      setCases(response);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch cases',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleRowClick = caseId => {
    navigate(`/cases/${caseId}`);
  };

  return (
    <Container maxW="container.xl" py={8}>
      <Stack spacing={6}>
        <Heading size="lg">Cases</Heading>

        <HStack spacing={4}>
          <Select
            placeholder="Filter by status"
            value={filters.status}
            onChange={e => handleFilterChange('status', e.target.value)}
          >
            {statusOptions.map(status => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </Select>

          <Select
            placeholder="Filter by priority"
            value={filters.priority}
            onChange={e => handleFilterChange('priority', e.target.value)}
          >
            {priorityOptions.map(priority => (
              <option key={priority} value={priority}>
                {priority}
              </option>
            ))}
          </Select>

          <Input
            placeholder="Search cases..."
            value={filters.search}
            onChange={e => handleFilterChange('search', e.target.value)}
          />

          <Button
            onClick={() => setFilters({ status: '', priority: '', search: '' })}
            variant="outline"
          >
            Clear Filters
          </Button>
        </HStack>

        {loading ? (
          <Box textAlign="center" py={8}>
            <Spinner size="xl" />
          </Box>
        ) : (
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Case ID</Th>
                <Th>Title</Th>
                <Th>Status</Th>
                <Th>Priority</Th>
                <Th>Assigned To</Th>
                <Th>Last Updated</Th>
              </Tr>
            </Thead>
            <Tbody>
              {cases.map(caseItem => (
                <Tr
                  key={caseItem.id}
                  onClick={() => handleRowClick(caseItem.id)}
                  cursor="pointer"
                  _hover={{ bg: 'gray.50' }}
                >
                  <Td>{caseItem.id}</Td>
                  <Td>{caseItem.title}</Td>
                  <Td>
                    <Badge colorScheme={statusColors[caseItem.status]}>{caseItem.status}</Badge>
                  </Td>
                  <Td>
                    <Badge colorScheme={priorityColors[caseItem.priority]}>
                      {caseItem.priority}
                    </Badge>
                  </Td>
                  <Td>{caseItem.assigned_to?.full_name || 'Unassigned'}</Td>
                  <Td>{new Date(caseItem.updated_at).toLocaleDateString()}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        )}
      </Stack>
    </Container>
  );
};

export default CaseListPage;
