import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Checkbox,
  Chip,
  Button,
  Grid,
  Paper,
  Divider
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  RadioButtonUnchecked as UncheckedIcon,
  Description as DocumentIcon,
  Download as DownloadIcon,
  Print as PrintIcon
} from '@mui/icons-material';

const DocumentChecklist = ({ type = 'immigration' }) => {
  const [checkedItems, setCheckedItems] = useState({});

  const documentTypes = {
    immigration: {
      title: 'Immigration Document Checklist',
      description: 'Essential documents needed for immigration applications',
      documents: [
        {
          category: 'Personal Documents',
          items: [
            { id: 'passport', name: 'Valid Passport', required: true, description: 'Must be valid for at least 6 months' },
            { id: 'birth_cert', name: 'Birth Certificate', required: true, description: 'Official copy with translation if needed' },
            { id: 'marriage_cert', name: 'Marriage Certificate', required: false, description: 'If applicable, with translation' },
            { id: 'divorce_decree', name: 'Divorce Decree', required: false, description: 'If applicable, with translation' },
            { id: 'death_cert', name: 'Death Certificate', required: false, description: 'If applicable, with translation' }
          ]
        },
        {
          category: 'Financial Documents',
          items: [
            { id: 'bank_statements', name: 'Bank Statements', required: true, description: 'Last 6 months of statements' },
            { id: 'tax_returns', name: 'Tax Returns', required: true, description: 'Last 3 years of tax returns' },
            { id: 'employment_letter', name: 'Employment Letter', required: true, description: 'Current employment verification' },
            { id: 'pay_stubs', name: 'Pay Stubs', required: true, description: 'Last 6 months of pay stubs' },
            { id: 'sponsor_affidavit', name: 'Sponsor Affidavit of Support', required: false, description: 'Form I-864 if applicable' }
          ]
        },
        {
          category: 'Immigration Documents',
          items: [
            { id: 'visa_applications', name: 'Previous Visa Applications', required: false, description: 'Any previous applications' },
            { id: 'i94', name: 'I-94 Arrival/Departure Record', required: true, description: 'Current and previous records' },
            { id: 'sevis_records', name: 'SEVIS Records', required: false, description: 'For student visa holders' },
            { id: 'work_permits', name: 'Work Permits', required: false, description: 'Current and previous work permits' }
          ]
        },
        {
          category: 'Supporting Documents',
          items: [
            { id: 'photos', name: 'Passport Photos', required: true, description: 'Recent photos meeting requirements' },
            { id: 'medical_exam', name: 'Medical Examination', required: true, description: 'From authorized physician' },
            { id: 'police_clearance', name: 'Police Clearance', required: true, description: 'From all countries lived in' },
            { id: 'education_records', name: 'Education Records', required: false, description: 'Diplomas, transcripts, evaluations' }
          ]
        }
      ]
    },
    family: {
      title: 'Family Law Document Checklist',
      description: 'Documents needed for family law matters',
      documents: [
        {
          category: 'Personal Information',
          items: [
            { id: 'id_documents', name: 'ID Documents', required: true, description: 'Driver\'s license, passport, etc.' },
            { id: 'birth_certificates', name: 'Birth Certificates', required: true, description: 'For all parties involved' },
            { id: 'marriage_certificate', name: 'Marriage Certificate', required: true, description: 'If applicable' },
            { id: 'divorce_papers', name: 'Previous Divorce Papers', required: false, description: 'If applicable' }
          ]
        },
        {
          category: 'Financial Information',
          items: [
            { id: 'income_documents', name: 'Income Documents', required: true, description: 'Pay stubs, tax returns, W-2s' },
            { id: 'bank_accounts', name: 'Bank Account Statements', required: true, description: 'All accounts, last 6 months' },
            { id: 'property_deeds', name: 'Property Deeds', required: true, description: 'Real estate ownership documents' },
            { id: 'debt_documents', name: 'Debt Documents', required: true, description: 'Credit card statements, loans' }
          ]
        }
      ]
    }
  };

  const currentType = documentTypes[type] || documentTypes.immigration;

  const handleCheckboxChange = (itemId) => {
    setCheckedItems(prev => ({
      ...prev,
      [itemId]: !prev[itemId]
    }));
  };

  const handleSelectAll = (categoryItems) => {
    const allChecked = categoryItems.every(item => checkedItems[item.id]);
    const newCheckedItems = { ...checkedItems };
    
    categoryItems.forEach(item => {
      newCheckedItems[item.id] = !allChecked;
    });
    
    setCheckedItems(newCheckedItems);
  };

  const getProgress = () => {
    const totalItems = currentType.documents.reduce((acc, category) => acc + category.items.length, 0);
    const checkedCount = Object.values(checkedItems).filter(Boolean).length;
    return Math.round((checkedCount / totalItems) * 100);
  };

  const handleDownload = () => {
    // Create a simple text version of the checklist
    let checklistText = `${currentType.title}\n${currentType.description}\n\n`;
    
    currentType.documents.forEach(category => {
      checklistText += `${category.category}:\n`;
      category.items.forEach(item => {
        const status = checkedItems[item.id] ? '✓' : '☐';
        checklistText += `${status} ${item.name}${item.required ? ' (Required)' : ''}\n`;
        if (item.description) {
          checklistText += `   ${item.description}\n`;
        }
      });
      checklistText += '\n';
    });
    
    const blob = new Blob([checklistText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentType.title.replace(/\s+/g, '_')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
      <Paper elevation={2} sx={{ p: 4, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Box>
            <Typography variant="h4" component="h1" gutterBottom sx={{ color: '#1565C0', fontWeight: 700 }}>
              {currentType.title}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              {currentType.description}
            </Typography>
          </Box>
          <Box sx={{ textAlign: 'right' }}>
            <Typography variant="h6" sx={{ color: '#1565C0', fontWeight: 600 }}>
              Progress: {getProgress()}%
            </Typography>
            <Box sx={{ width: 200, height: 8, bgcolor: '#e0e0e0', borderRadius: 4, mt: 1 }}>
              <Box 
                sx={{ 
                  width: `${getProgress()}%`, 
                  height: '100%', 
                  bgcolor: '#1565C0', 
                  borderRadius: 4,
                  transition: 'width 0.3s ease'
                }} 
              />
            </Box>
          </Box>
        </Box>

        <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
          <Button
            variant="contained"
            startIcon={<DownloadIcon />}
            onClick={handleDownload}
            sx={{
              backgroundColor: '#1565C0',
              '&:hover': { backgroundColor: '#0D47A1' }
            }}
          >
            Download Checklist
          </Button>
          <Button
            variant="outlined"
            startIcon={<PrintIcon />}
            onClick={() => window.print()}
            sx={{
              borderColor: '#1565C0',
              color: '#1565C0',
              '&:hover': { 
                borderColor: '#0D47A1',
                backgroundColor: 'rgba(21, 101, 192, 0.04)'
              }
            }}
          >
            Print Checklist
          </Button>
        </Box>
      </Paper>

      <Grid container spacing={3}>
        {currentType.documents.map((category, categoryIndex) => (
          <Grid item xs={12} md={6} key={categoryIndex}>
            <Card elevation={2} sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6" sx={{ color: '#1565C0', fontWeight: 600 }}>
                    {category.category}
                  </Typography>
                  <Button
                    size="small"
                    onClick={() => handleSelectAll(category.items)}
                    sx={{ color: '#1565C0', fontSize: '0.75rem' }}
                  >
                    {category.items.every(item => checkedItems[item.id]) ? 'Uncheck All' : 'Check All'}
                  </Button>
                </Box>
                
                <List>
                  {category.items.map((item, itemIndex) => (
                    <React.Fragment key={item.id}>
                      <ListItem sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          <Checkbox
                            checked={checkedItems[item.id] || false}
                            onChange={() => handleCheckboxChange(item.id)}
                            icon={<UncheckedIcon />}
                            checkedIcon={<CheckCircleIcon />}
                            sx={{
                              color: '#1565C0',
                              '&.Mui-checked': { color: '#1565C0' }
                            }}
                          />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                {item.name}
                              </Typography>
                              {item.required && (
                                <Chip 
                                  label="Required" 
                                  size="small" 
                                  color="error" 
                                  sx={{ fontSize: '0.7rem', height: 20 }}
                                />
                              )}
                            </Box>
                          }
                          secondary={
                            <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                              {item.description}
                            </Typography>
                          }
                        />
                      </ListItem>
                      {itemIndex < category.items.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper elevation={2} sx={{ p: 3, mt: 3, bgcolor: '#f8f9fa' }}>
        <Typography variant="h6" gutterBottom sx={{ color: '#1565C0', fontWeight: 600 }}>
          Important Notes:
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          • All documents must be original or certified copies
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          • Documents not in English must be accompanied by certified translations
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          • Keep copies of all documents for your records
        </Typography>
        <Typography variant="body2" color="text.secondary">
          • Contact your attorney if you have questions about any requirements
        </Typography>
      </Paper>
    </Box>
  );
};

export default DocumentChecklist;
