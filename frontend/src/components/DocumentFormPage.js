import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Button, Typography } from '@mui/material';
import { useToast } from '@chakra-ui/react';

const getTemplateFormSchema = async templateId => {
  try {
    const response = await fetch(`/api/templates/${templateId}/schema`);
    if (!response.ok) {
      throw new Error('Failed to fetch template schema');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching template schema:', error);
    throw error;
  }
};

const DocumentFormPage = () => {
  const { templateId } = useParams();
  const [formSchema, setFormSchema] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const toast = useToast();

  useEffect(() => {
    const fetchSchema = async () => {
      try {
        setLoading(true);
        const schema = await getTemplateFormSchema(templateId);
        setFormSchema(schema);
      } catch (err) {
        setError(err.message);
        toast({
          title: 'Error',
          description: 'Failed to load form schema',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setLoading(false);
      }
    };

    fetchSchema();
  }, [templateId, toast]);

  if (loading) {
    return <Box>Loading...</Box>;
  }

  if (error) {
    return <Box>Error: {error}</Box>;
  }

  return (
    <Box>
      <Typography variant="h4">Document Form</Typography>
      {formSchema && (
        <form>
          {/* Form fields based on schema */}
          <Button type="submit" variant="contained" color="primary">
            Generate Document
          </Button>
        </form>
      )}
    </Box>
  );
};

export default DocumentFormPage;
