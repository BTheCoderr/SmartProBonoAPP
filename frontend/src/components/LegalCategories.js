import React from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Chip
} from '@mui/material';
import GavelIcon from '@mui/icons-material/Gavel';
import HomeIcon from '@mui/icons-material/Home';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import WorkIcon from '@mui/icons-material/Work';
import ReceiptIcon from '@mui/icons-material/Receipt';
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import PublicIcon from '@mui/icons-material/Public';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';

// Legal categories and common questions
const legalCategories = [
  {
    id: 'housing',
    name: 'Housing & Tenants Rights',
    icon: <HomeIcon color="primary" />,
    description: 'Questions about renting, leasing, evictions and tenant rights',
    questions: [
      'What should I do if I received an eviction notice?',
      'What are my rights as a tenant?',
      'Can my landlord enter my apartment without permission?',
      'How do I get my security deposit back?',
      'What are the legal requirements for breaking a lease?'
    ]
  },
  {
    id: 'family',
    name: 'Family Law',
    icon: <FamilyRestroomIcon color="primary" />,
    description: 'Divorce, custody, support and other family matters',
    questions: [
      'How do I file for divorce?',
      'What factors affect child custody decisions?',
      'How is child support calculated?',
      'What is the difference between legal and physical custody?',
      'How do I modify an existing custody arrangement?'
    ]
  },
  {
    id: 'employment',
    name: 'Employment Law',
    icon: <WorkIcon color="primary" />,
    description: 'Workplace rights, discrimination, and compensation issues',
    questions: [
      'What counts as workplace discrimination?',
      'Am I entitled to overtime pay?',
      'Can I be fired without cause?',
      'What should I do if I face harassment at work?',
      'What are my rights regarding medical leave?'
    ]
  },
  {
    id: 'consumer',
    name: 'Consumer Rights',
    icon: <ReceiptIcon color="primary" />,
    description: 'Debt, contracts, and consumer protection issues',
    questions: [
      'How do I dispute a charge on my credit report?',
      'What can I do about aggressive debt collectors?',
      'Can I return a product after purchasing it?',
      'What are my rights when dealing with door-to-door salespeople?',
      'How do I file a complaint against a business?'
    ]
  },
  {
    id: 'traffic',
    name: 'Traffic & Vehicle',
    icon: <DirectionsCarIcon color="primary" />,
    description: 'Traffic violations, accidents, and vehicle regulations',
    questions: [
      'What should I do after a car accident?',
      'How do I fight a traffic ticket?',
      'What are my rights during a traffic stop?',
      'What information should I exchange after an accident?',
      'Do I need to report a minor accident?'
    ]
  },
  {
    id: 'courts',
    name: 'Court Procedures',
    icon: <AccountBalanceIcon color="primary" />,
    description: 'How courts work and common legal procedures',
    questions: [
      'How do I represent myself in small claims court?',
      'What happens at an arraignment?',
      'How do I respond to a summons?',
      'How do I file a legal document with the court?',
      'What is the difference between a hearing and a trial?'
    ]
  },
  {
    id: 'immigration',
    name: 'Immigration',
    icon: <PublicIcon color="primary" />,
    description: 'Visa applications, citizenship, and immigration status',
    questions: [
      'How do I apply for a green card?',
      'What is the naturalization process?',
      'What are my rights as an immigrant?',
      'How do I check my immigration case status?',
      'What should I do if I receive a notice to appear?'
    ]
  },
  {
    id: 'healthcare',
    name: 'Healthcare Law',
    icon: <HealthAndSafetyIcon color="primary" />,
    description: 'Medical billing, insurance, and patient rights',
    questions: [
      'What can I do about a denied insurance claim?',
      'How do I access my medical records?',
      'What are my rights regarding medical privacy?',
      'How do I appeal a health insurance decision?',
      'What should I do about a large medical bill?'
    ]
  }
];

const LegalCategories = ({ onCategorySelect, onQuestionSelect }) => {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Select a Legal Topic
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Choose a category or specific question to get started with legal assistance.
      </Typography>
      
      <Grid container spacing={3}>
        {legalCategories.map((category) => (
          <Grid item xs={12} sm={6} md={4} key={category.id}>
            <Paper 
              elevation={2}
              sx={{ 
                p: 2, 
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'all 0.2s',
                cursor: 'pointer',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4
                }
              }}
              onClick={() => onCategorySelect(category)}
            >
              <Box display="flex" alignItems="center" mb={1}>
                {category.icon}
                <Typography variant="subtitle1" component="h3" ml={1}>
                  {category.name}
                </Typography>
              </Box>
              
              <Typography variant="body2" color="text.secondary" mb={2}>
                {category.description}
              </Typography>
              
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ flexGrow: 1 }}>
                <Typography variant="caption" color="text.secondary" gutterBottom>
                  Common Questions:
                </Typography>
                <List dense disablePadding>
                  {category.questions.slice(0, 3).map((question, index) => (
                    <ListItem 
                      key={index}
                      disableGutters
                      sx={{ 
                        py: 0.5,
                        px: 0,
                        borderRadius: 1,
                        '&:hover': { 
                          backgroundColor: 'rgba(0, 0, 0, 0.03)',
                        }
                      }}
                      onClick={(e) => {
                        e.stopPropagation(); // Prevent triggering the parent click
                        onQuestionSelect(question);
                      }}
                    >
                      <ListItemIcon sx={{ minWidth: 28 }}>
                        <GavelIcon fontSize="small" color="action" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={question}
                        primaryTypographyProps={{ 
                          variant: 'body2',
                          noWrap: true,
                          title: question // Show full text on hover
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
              
              <Chip 
                label={`${category.questions.length} Questions`}
                size="small"
                color="primary"
                variant="outlined"
                sx={{ alignSelf: 'flex-start', mt: 1 }}
              />
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default LegalCategories; 