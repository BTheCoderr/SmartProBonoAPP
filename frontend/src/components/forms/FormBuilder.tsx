import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Grid,
  MenuItem,
  Select,
  TextField,
  Typography,
  Alert,
  FormControl,
  InputLabel,
} from '@mui/material';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { useAuth } from '../../hooks/useAuth';
import { api } from '../../services/api';

interface FormBuilderProps {
  templateId?: string;
  onSubmit?: (data: any) => void;
  onCancel?: () => void;
}

interface FormTemplate {
  id: string;
  name: string;
  description: string;
  schema: any;
}

const FormBuilder: React.FC<FormBuilderProps> = ({
  templateId,
  onSubmit,
  onCancel,
}) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [template, setTemplate] = useState<FormTemplate | null>(null);
  const [templates, setTemplates] = useState<FormTemplate[]>([]);
  const { user } = useAuth();

  // Fetch available templates
  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const response = await api.get('/api/immigration/form-templates');
        setTemplates(response.data.templates);
        setLoading(false);
      } catch (err) {
        setError('Failed to load form templates');
        setLoading(false);
      }
    };

    fetchTemplates();
  }, []);

  // Fetch specific template if templateId is provided
  useEffect(() => {
    const fetchTemplate = async () => {
      if (!templateId) return;
      try {
        const response = await api.get(`/api/immigration/form-templates/${templateId}`);
        setTemplate(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load form template');
        setLoading(false);
      }
    };

    fetchTemplate();
  }, [templateId]);

  // Generate validation schema from template
  const generateValidationSchema = (schema: any) => {
    const yupSchema: any = {};
    
    Object.entries(schema.properties).forEach(([key, value]: [string, any]) => {
      if (value.type === 'string') {
        yupSchema[key] = yup.string();
        if (value.required) yupSchema[key] = yupSchema[key].required('This field is required');
        if (value.format === 'email') yupSchema[key] = yupSchema[key].email('Invalid email format');
      } else if (value.type === 'number') {
        yupSchema[key] = yup.number();
        if (value.required) yupSchema[key] = yupSchema[key].required('This field is required');
      }
    });

    return yup.object().shape(yupSchema);
  };

  // Generate initial values from schema
  const generateInitialValues = (schema: any) => {
    const initialValues: any = {};
    
    Object.entries(schema.properties).forEach(([key, value]: [string, any]) => {
      initialValues[key] = value.default || '';
    });

    return initialValues;
  };

  const formik = useFormik({
    initialValues: template ? generateInitialValues(template.schema) : {},
    validationSchema: template ? generateValidationSchema(template.schema) : null,
    enableReinitialize: true,
    onSubmit: async (values) => {
      try {
        const response = await api.post('/api/immigration/submit-form/' + template?.id, values);
        if (onSubmit) onSubmit(response.data);
      } catch (err) {
        setError('Failed to submit form');
      }
    },
  });

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Card>
      <CardContent>
        {!templateId && (
          <FormControl fullWidth margin="normal">
            <InputLabel>Select Template</InputLabel>
            <Select
              value={template?.id || ''}
              onChange={(e) => {
                const selected = templates.find(t => t.id === e.target.value);
                setTemplate(selected || null);
              }}
            >
              {templates.map((t) => (
                <MenuItem key={t.id} value={t.id}>
                  {t.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        )}

        {template && (
          <form onSubmit={formik.handleSubmit}>
            <Typography variant="h6" gutterBottom>
              {template.name}
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              {template.description}
            </Typography>

            <Grid container spacing={3}>
              {Object.entries(template.schema.properties).map(([key, value]: [string, any]) => (
                <Grid item xs={12} sm={6} key={key}>
                  <TextField
                    fullWidth
                    id={key}
                    name={key}
                    label={value.title || key}
                    type={value.format === 'email' ? 'email' : value.type === 'number' ? 'number' : 'text'}
                    value={formik.values[key]}
                    onChange={formik.handleChange}
                    error={formik.touched[key] && Boolean(formik.errors[key])}
                    helperText={formik.touched[key] && formik.errors[key]}
                    required={value.required}
                  />
                </Grid>
              ))}
            </Grid>

            <Box mt={3} display="flex" justifyContent="flex-end" gap={2}>
              {onCancel && (
                <Button onClick={onCancel} color="inherit">
                  Cancel
                </Button>
              )}
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={!formik.isValid || formik.isSubmitting}
              >
                {formik.isSubmitting ? 'Submitting...' : 'Submit'}
              </Button>
            </Box>
          </form>
        )}
      </CardContent>
    </Card>
  );
};

export default FormBuilder; 