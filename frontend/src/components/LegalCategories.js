import { Box, Button, Typography, ButtonGroup, Card, CardContent } from '@mui/material';
import GavelIcon from '@mui/icons-material/Gavel';
import BusinessIcon from '@mui/icons-material/Business';
import HomeIcon from '@mui/icons-material/Home';
import WorkIcon from '@mui/icons-material/Work';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import FlightIcon from '@mui/icons-material/Flight';
import PropTypes from 'prop-types';
const categories = [
  {
    id: 'civil_rights',
    name: 'Civil Rights',
    icon: <GavelIcon />,
    color: '#1976d2',
    questions: [
      'What are my basic civil rights?',
      'How can I file a discrimination complaint?',
      'What should I do if my rights are violated?',
    ],
  },
  {
    id: 'business_law',
    name: 'Business Law',
    icon: <BusinessIcon />,
    color: '#2e7d32',
    questions: [
      'How do I register a new business?',
      'What contracts do I need for my startup?',
      'How do I protect my intellectual property?',
    ],
  },
  {
    id: 'housing',
    name: 'Housing',
    icon: <HomeIcon />,
    color: '#ed6c02',
    questions: [
      'What are my rights as a tenant?',
      'How do I handle a landlord dispute?',
      "What's the eviction process in my state?",
    ],
  },
  {
    id: 'employment',
    name: 'Employment',
    icon: <WorkIcon />,
    color: '#9c27b0',
    questions: [
      'What are my workplace rights?',
      'How do I file a workplace complaint?',
      "What's included in employment contracts?",
    ],
  },
  {
    id: 'family_law',
    name: 'Family Law',
    icon: <FamilyRestroomIcon />,
    color: '#d32f2f',
    questions: [
      'How does divorce process work?',
      'What are child custody rights?',
      'How do I file for child support?',
    ],
  },
  {
    id: 'immigration',
    name: 'Immigration',
    icon: <FlightIcon />,
    color: '#0288d1',
    questions: [
      'How do I apply for a visa?',
      "What's the citizenship process?",
      'What are my rights as an immigrant?',
    ],
  },
];
const LegalCategories = ({ onCategorySelect, onQuestionSelect, selectedCategory }) => {
  return (
    <Box sx={{ width: '100%', mb: 4 }}>
      <Typography variant="h6" gutterBottom>
        Select a Category
      </Typography>
      <ButtonGroup
        variant="outlined"
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 1,
          mb: 3,
        }}
      >
        {categories.map(category => (
          <Button
            key={category.id}
            onClick={() => onCategorySelect(category)}
            startIcon={category.icon}
            sx={{
              borderColor: selectedCategory?.id === category.id ? category.color : 'divider',
              color: selectedCategory?.id === category.id ? category.color : 'text.primary',
              bgcolor: selectedCategory?.id === category.id ? `${category.color}10` : 'transparent',
              '&:hover': {
                bgcolor: `${category.color}20`,
                borderColor: category.color,
              },
            }}
          >
            {category.name}
          </Button>
        ))}
      </ButtonGroup>
      {selectedCategory && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Suggested Questions
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {selectedCategory.questions.map((question, index) => (
                <Button
                  key={index}
                  variant="text"
                  onClick={() => onQuestionSelect(question)}
                  sx={{
                    justifyContent: 'flex-start',
                    color: 'primary.main',
                    textAlign: 'left',
                    '&:hover': {
                      bgcolor: 'primary.lighter',
                    },
                  }}
                >
                  {question}
                </Button>
              ))}
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

// Define PropTypes
LegalCategories.propTypes = {
  /** TODO: Add description */
  onCategorySelect: PropTypes.any,
  /** TODO: Add description */
  onQuestionSelect: PropTypes.any,
  /** TODO: Add description */
  selectedCategory: PropTypes.any,
};

export default LegalCategories;