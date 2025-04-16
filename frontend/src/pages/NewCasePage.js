import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Heading,
  FormControl,
  Input,
  Select,
  Textarea,
  Button,
  VStack,
  HStack,
  useToast,
  IconButton,
  Text,
  Card,
  CardBody,
  useColorModeValue,
  Badge,
  Divider,
} from '@chakra-ui/react';
import { ArrowBackIcon } from '@chakra-ui/icons';
import { createCase } from '../services/caseService';
// Data
import {
  CASE_STATUS,
  CASE_TYPES,
  PRIORITY_LEVELS,
  getStatusLabel,
  getCaseTypeLabel,
  getPriorityLabel,
} from '../data/casesData';
const NewCasePage = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    type: 'civil',
    priority: 'medium',
    status: 'new',
  });
  const handleInputChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };
  const handleSubmit = async e => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const newCase = await createCase(formData);
      toast({
        title: 'Case created successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
        position: 'top-right',
      });
      navigate(`/cases/${newCase.id}`);
    } catch (error) {
      toast({
        title: 'Error creating case',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
        position: 'top-right',
      });
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <Box bg={useColorModeValue('gray.50', 'gray.900')} minH="100vh" py={8}>
      <Container maxW="container.lg">
        <HStack spacing={4} mb={8}>
          <IconButton
            icon={<ArrowBackIcon />}
            onClick={() => navigate('/cases')}
            aria-label="Back to cases"
            variant="ghost"
            size="lg"
            _hover={{ bg: useColorModeValue('gray.100', 'gray.700') }}
          />
          <Heading size="lg">Create New Case</Heading>
        </HStack>
        <Card
          bg={bgColor}
          shadow="lg"
          borderRadius="xl"
          borderColor={borderColor}
          borderWidth="1px"
        >
          <CardBody>
            <Box as="form" onSubmit={handleSubmit}>
              <VStack spacing={6} align="stretch">
                <FormControl isRequired>
                  <Text mb={2} fontWeight="medium">
                    Case Title
                  </Text>
                  <Input
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    placeholder="Enter case title"
                    size="lg"
                    bg={useColorModeValue('white', 'gray.800')}
                    borderColor={borderColor}
                    _hover={{ borderColor: 'blue.400' }}
                    _focus={{ borderColor: 'blue.400', boxShadow: 'outline' }}
                  />
                </FormControl>
                <FormControl>
                  <Text mb={2} fontWeight="medium">
                    Case Description
                  </Text>
                  <Textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Enter case description"
                    size="lg"
                    rows={4}
                    bg={useColorModeValue('white', 'gray.800')}
                    borderColor={borderColor}
                    _hover={{ borderColor: 'blue.400' }}
                    _focus={{ borderColor: 'blue.400', boxShadow: 'outline' }}
                  />
                </FormControl>
                <Divider />
                <HStack spacing={4} width="100%" align="flex-start">
                  <FormControl>
                    <Text mb={2} fontWeight="medium">
                      Case Type
                    </Text>
                    <Select
                      name="type"
                      value={formData.type}
                      onChange={handleInputChange}
                      size="lg"
                      bg={useColorModeValue('white', 'gray.800')}
                      borderColor={borderColor}
                      _hover={{ borderColor: 'blue.400' }}
                    >
                      {Object.values(CASE_TYPES).map(type => (
                        <option key={type} value={type}>
                          {getCaseTypeLabel(type)}
                        </option>
                      ))}
                    </Select>
                  </FormControl>
                  <FormControl>
                    <Text mb={2} fontWeight="medium">
                      Priority
                    </Text>
                    <Select
                      name="priority"
                      value={formData.priority}
                      onChange={handleInputChange}
                      size="lg"
                      bg={useColorModeValue('white', 'gray.800')}
                      borderColor={borderColor}
                      _hover={{ borderColor: 'blue.400' }}
                    >
                      {Object.values(PRIORITY_LEVELS).map(priority => (
                        <option key={priority} value={priority}>
                          {getPriorityLabel(priority)}
                        </option>
                      ))}
                    </Select>
                  </FormControl>
                  <FormControl>
                    <Text mb={2} fontWeight="medium">
                      Status
                    </Text>
                    <Select
                      name="status"
                      value={formData.status}
                      onChange={handleInputChange}
                      size="lg"
                      bg={useColorModeValue('white', 'gray.800')}
                      borderColor={borderColor}
                      _hover={{ borderColor: 'blue.400' }}
                    >
                      {Object.values(CASE_STATUS).map(status => (
                        <option key={status} value={status}>
                          {getStatusLabel(status)}
                        </option>
                      ))}
                    </Select>
                  </FormControl>
                </HStack>
                <Button
                  type="submit"
                  colorScheme="blue"
                  isLoading={isLoading}
                  loadingText="Creating..."
                  size="lg"
                  width="full"
                  height="56px"
                  mt={4}
                  fontSize="md"
                  _hover={{ transform: 'translateY(-1px)', boxShadow: 'lg' }}
                  transition="all 0.2s"
                >
                  Create Case
                </Button>
              </VStack>
            </Box>
          </CardBody>
        </Card>
      </Container>
    </Box>
  );
};
export default NewCasePage;