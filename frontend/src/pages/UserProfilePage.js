import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Heading,
  VStack,
  FormControl,
  FormLabel,
  Input,
  Select,
  Button,
  useToast,
  Divider,
  Text,
  SimpleGrid,
  Switch,
  Badge,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
} from '@chakra-ui/react';
import { getUserById, updateUserProfile, updateUserAvailability } from '../services/userService';

const UserProfilePage = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [profileData, setProfileData] = useState({
    full_name: '',
    email: '',
    phone: '',
    role: '',
    specialties: [],
    bio: '',
  });
  const [availability, setAvailability] = useState({
    monday: { available: false, hours: '9:00-17:00' },
    tuesday: { available: false, hours: '9:00-17:00' },
    wednesday: { available: false, hours: '9:00-17:00' },
    thursday: { available: false, hours: '9:00-17:00' },
    friday: { available: false, hours: '9:00-17:00' },
  });
  const toast = useToast();

  const roles = ['ATTORNEY', 'PARALEGAL', 'ADMIN'];
  const specialties = [
    'CRIMINAL_LAW',
    'FAMILY_LAW',
    'IMMIGRATION_LAW',
    'CIVIL_RIGHTS',
    'HOUSING_LAW',
  ];

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      // In a real app, you'd get the user ID from auth context or URL params
      const userId = '123';
      const userData = await getUserById(userId);
      setUser(userData);
      setProfileData({
        full_name: userData.full_name,
        email: userData.email,
        phone: userData.phone,
        role: userData.role,
        specialties: userData.profile.specialties,
        bio: userData.profile.bio,
      });
      setAvailability(userData.availability);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch user data',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleProfileChange = (field, value) => {
    setProfileData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSpecialtyChange = specialty => {
    setProfileData(prev => {
      const specialties = prev.specialties.includes(specialty)
        ? prev.specialties.filter(s => s !== specialty)
        : [...prev.specialties, specialty];
      return { ...prev, specialties };
    });
  };

  const handleAvailabilityChange = (day, field, value) => {
    setAvailability(prev => ({
      ...prev,
      [day]: {
        ...prev[day],
        [field]: value,
      },
    }));
  };

  const handleProfileSubmit = async () => {
    try {
      await updateUserProfile(user.id, profileData);
      toast({
        title: 'Success',
        description: 'Profile updated successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update profile',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleAvailabilitySubmit = async () => {
    try {
      await updateUserAvailability(user.id, availability);
      toast({
        title: 'Success',
        description: 'Availability updated successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update availability',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  if (loading) {
    return <Box>Loading...</Box>;
  }

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading size="lg" mb={6}>
            Profile Settings
          </Heading>
          <VStack spacing={4} align="stretch">
            <FormControl>
              <FormLabel>Full Name</FormLabel>
              <Input
                value={profileData.full_name}
                onChange={e => handleProfileChange('full_name', e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Email</FormLabel>
              <Input
                type="email"
                value={profileData.email}
                onChange={e => handleProfileChange('email', e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Phone</FormLabel>
              <Input
                value={profileData.phone}
                onChange={e => handleProfileChange('phone', e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Role</FormLabel>
              <Select
                value={profileData.role}
                onChange={e => handleProfileChange('role', e.target.value)}
              >
                {roles.map(role => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ))}
              </Select>
            </FormControl>
            <FormControl>
              <FormLabel>Specialties</FormLabel>
              <SimpleGrid columns={2} spacing={4}>
                {specialties.map(specialty => (
                  <Box key={specialty}>
                    <Switch
                      isChecked={profileData.specialties.includes(specialty)}
                      onChange={() => handleSpecialtyChange(specialty)}
                    />
                    <Text ml={2} display="inline-block">
                      {specialty.replace('_', ' ')}
                    </Text>
                  </Box>
                ))}
              </SimpleGrid>
            </FormControl>
            <FormControl>
              <FormLabel>Bio</FormLabel>
              <Input
                as="textarea"
                value={profileData.bio}
                onChange={e => handleProfileChange('bio', e.target.value)}
                height="100px"
              />
            </FormControl>
            <Button colorScheme="blue" onClick={handleProfileSubmit}>
              Save Profile
            </Button>
          </VStack>
        </Box>

        <Divider my={8} />

        <Box>
          <Heading size="lg" mb={6}>
            Availability Settings
          </Heading>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Day</Th>
                <Th>Available</Th>
                <Th>Hours</Th>
              </Tr>
            </Thead>
            <Tbody>
              {Object.entries(availability).map(([day, data]) => (
                <Tr key={day}>
                  <Td>{day.charAt(0).toUpperCase() + day.slice(1)}</Td>
                  <Td>
                    <Switch
                      isChecked={data.available}
                      onChange={e => handleAvailabilityChange(day, 'available', e.target.checked)}
                    />
                  </Td>
                  <Td>
                    <Input
                      value={data.hours}
                      onChange={e => handleAvailabilityChange(day, 'hours', e.target.value)}
                      isDisabled={!data.available}
                      placeholder="9:00-17:00"
                    />
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
          <Button mt={4} colorScheme="blue" onClick={handleAvailabilitySubmit}>
            Save Availability
          </Button>
        </Box>

        <Divider my={8} />

        <Box>
          <Heading size="lg" mb={6}>
            Current Case Load
          </Heading>
          <SimpleGrid columns={3} spacing={4}>
            <Box p={4} borderWidth={1} borderRadius="md">
              <Text fontSize="lg" fontWeight="bold">
                Active Cases
              </Text>
              <Badge colorScheme="blue" fontSize="2xl">
                {user.case_load.active_cases}
              </Badge>
            </Box>
            <Box p={4} borderWidth={1} borderRadius="md">
              <Text fontSize="lg" fontWeight="bold">
                Cases This Month
              </Text>
              <Badge colorScheme="green" fontSize="2xl">
                {user.case_load.cases_this_month}
              </Badge>
            </Box>
            <Box p={4} borderWidth={1} borderRadius="md">
              <Text fontSize="lg" fontWeight="bold">
                Total Cases
              </Text>
              <Badge colorScheme="purple" fontSize="2xl">
                {user.case_load.total_cases}
              </Badge>
            </Box>
          </SimpleGrid>
        </Box>
      </VStack>
    </Container>
  );
};

export default UserProfilePage;
