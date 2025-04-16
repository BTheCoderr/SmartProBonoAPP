// Document template form schema utilities
import axios from 'axios';

// Template schema cache for performance
const templateCache = {};

/**
 * Fetches a template form schema from the backend API
 * @param {string} templateId - The ID of the template to fetch
 * @returns {Promise<Object>} - The template schema
 */
export const fetchTemplateFormSchema = async (templateId) => {
  try {
    // Check cache first
    if (templateCache[templateId]) {
      return templateCache[templateId];
    }

    // Fetch from API
    const response = await axios.get(`/api/documents/templates/${templateId}`);
    const templateSchema = response.data;
    
    // Cache the result
    templateCache[templateId] = templateSchema;
    
    return templateSchema;
  } catch (error) {
    console.error('Error fetching template schema:', error);
    // Return a fallback schema
    return getFallbackSchema(templateId);
  }
};

/**
 * Gets a template form schema (synchronous version - for backward compatibility)
 * This will try to use the cache or return a basic schema
 * @param {string} templateId - The ID of the template to get
 * @returns {Object} - The template schema
 */
export const getTemplateFormSchema = (templateId) => {
  // Return from cache if available
  if (templateCache[templateId]) {
    return templateCache[templateId];
  }
  
  // Return fallback schema
  return getFallbackSchema(templateId);
};

/**
 * Provides a fallback schema for a given template ID
 * @param {string} templateId - The ID of the template
 * @returns {Object} - A basic schema for the template
 */
const getFallbackSchema = (templateId) => {
  // Special cases for new templates
  if (templateId === 'last-will-testament') {
    return {
      sections: [
        {
          title: 'Personal Information',
          description: 'Enter your personal details for the will',
          fields: [
            {
              id: 'testator_name',
              label: 'Your Full Legal Name',
              type: 'text',
              required: true,
              helpText: 'Enter your full legal name as it should appear in the will'
            },
            {
              id: 'testator_address',
              label: 'Your Current Address',
              type: 'textarea',
              required: true,
              helpText: 'Enter your full current address'
            },
            {
              id: 'marital_status',
              label: 'Marital Status',
              type: 'select',
              options: [
                { value: 'single', label: 'Single' },
                { value: 'married', label: 'Married' },
                { value: 'divorced', label: 'Divorced' },
                { value: 'widowed', label: 'Widowed' }
              ],
              required: true,
              helpText: 'Select your current marital status'
            }
          ]
        },
        {
          title: 'Executors',
          description: 'Designate who will execute your will',
          fields: [
            {
              id: 'executor_name',
              label: 'Executor Full Name',
              type: 'text',
              required: true,
              helpText: 'The person who will be responsible for executing your will'
            },
            {
              id: 'executor_address',
              label: 'Executor Address',
              type: 'textarea',
              required: true,
              helpText: 'Enter the full current address of your executor'
            },
            {
              id: 'alternate_executor_name',
              label: 'Alternate Executor Name',
              type: 'text',
              required: true,
              helpText: 'A backup person who will execute your will if your first choice cannot'
            }
          ]
        },
        {
          title: 'Will Content',
          description: 'Define the content of your will',
          fields: [
            {
              id: 'revocation_clause',
              label: 'Revocation Clause',
              type: 'textarea',
              required: true,
              helpText: 'Standard clause revoking all previous wills and codicils',
              defaultValue: 'I hereby revoke all previous wills and codicils made by me.'
            },
            {
              id: 'children_names',
              label: 'Names of Children',
              type: 'textarea',
              required: false,
              helpText: 'List the full names of all your children, separated by commas'
            },
            {
              id: 'specific_bequests',
              label: 'Specific Bequests',
              type: 'textarea',
              required: false,
              helpText: 'List any specific items or amounts you want to leave to specific people'
            },
            {
              id: 'residuary_beneficiaries',
              label: 'Residuary Beneficiaries',
              type: 'textarea',
              required: true,
              helpText: 'Who should receive the remainder of your estate'
            }
          ]
        }
      ]
    };
  }
  
  if (templateId === 'medical-power-of-attorney') {
    return {
      sections: [
        {
          title: 'Principal Information',
          description: 'Enter your personal details',
          fields: [
            {
              id: 'principal_name',
              label: 'Your Full Legal Name',
              type: 'text',
              required: true,
              helpText: 'Enter your full legal name as the one granting power of attorney'
            },
            {
              id: 'principal_address',
              label: 'Your Current Address',
              type: 'textarea',
              required: true,
              helpText: 'Enter your full current address'
            },
            {
              id: 'effective_date',
              label: 'Effective Date',
              type: 'date',
              required: true,
              helpText: 'When this document should take effect'
            }
          ]
        },
        {
          title: 'Healthcare Agent',
          description: 'Designate who will make decisions for you',
          fields: [
            {
              id: 'agent_name',
              label: 'Agent Full Name',
              type: 'text',
              required: true,
              helpText: 'The person who will make healthcare decisions on your behalf'
            },
            {
              id: 'agent_address',
              label: 'Agent Address',
              type: 'textarea',
              required: true,
              helpText: 'Enter the full current address of your agent'
            },
            {
              id: 'agent_phone',
              label: 'Agent Phone Number',
              type: 'tel',
              required: true,
              helpText: 'Phone number where your agent can be reached'
            }
          ]
        },
        {
          title: 'Alternate Agent',
          description: 'Designate a backup decision-maker',
          fields: [
            {
              id: 'alternate_agent_name',
              label: 'Alternate Agent Full Name',
              type: 'text',
              required: true,
              helpText: 'Backup person who will make decisions if your first agent cannot'
            },
            {
              id: 'alternate_agent_address',
              label: 'Alternate Agent Address',
              type: 'textarea',
              required: true,
              helpText: 'Enter the full current address of your alternate agent'
            },
            {
              id: 'alternate_agent_phone',
              label: 'Alternate Agent Phone Number',
              type: 'tel',
              required: true,
              helpText: 'Phone number where your alternate agent can be reached'
            }
          ]
        },
        {
          title: 'Healthcare Preferences',
          description: 'Define your healthcare preferences',
          fields: [
            {
              id: 'life_sustaining_treatment',
              label: 'Life-Sustaining Treatment',
              type: 'textarea',
              required: false,
              helpText: 'Your wishes regarding life-sustaining treatments'
            },
            {
              id: 'artificial_nutrition',
              label: 'Artificial Nutrition and Hydration',
              type: 'textarea',
              required: false,
              helpText: 'Your wishes regarding artificial nutrition and hydration'
            },
            {
              id: 'pain_medication',
              label: 'Pain Relief',
              type: 'textarea',
              required: false,
              helpText: 'Your wishes regarding pain relief and comfort care'
            },
            {
              id: 'organ_donation',
              label: 'Organ Donation',
              type: 'textarea',
              required: false,
              helpText: 'Your preferences regarding organ donation'
            }
          ]
        }
      ]
    };
  }
  
  // Default schema for other templates
  return {
    sections: [
      {
        title: 'Basic Information',
        description: 'Enter the basic information for your document',
        fields: [
          {
            id: 'title',
            label: 'Document Title',
            type: 'text',
            required: true,
            helpText: 'Enter a title for your document'
          },
          {
            id: 'description',
            label: 'Description',
            type: 'textarea',
            required: false,
            helpText: 'Provide a brief description of the document'
          }
        ]
      }
    ]
  };
};

/**
 * Validates document form data against template requirements
 * @param {Object} formData - The form data to validate
 * @param {string} templateId - The ID of the template
 * @returns {Object} - Object with isValid flag and any validation errors
 */
export const validateDocumentForm = async (formData, templateId) => {
  try {
    // Fetch the template schema if not in cache
    const templateSchema = await fetchTemplateFormSchema(templateId);
    
    const errors = {};
    let isValid = true;
    
    // Check if all required fields are filled
    if (templateSchema && templateSchema.required_fields) {
      templateSchema.required_fields.forEach(fieldId => {
        if (!formData[fieldId] || formData[fieldId].trim() === '') {
          errors[fieldId] = 'This field is required';
          isValid = false;
        }
      });
    }
    
    return { isValid, errors };
  } catch (error) {
    console.error('Error validating document form:', error);
    return { 
      isValid: false, 
      errors: { _general: 'Failed to validate form. Please try again.' } 
    };
  }
}; 