import React from 'react';
import {
  Container,
  Paper,
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  CardMedia,
  Button,
  Alert,
  Chip,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import Navigation from '../components/Navigation';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import DescriptionIcon from '@mui/icons-material/Description';
import GavelIcon from '@mui/icons-material/Gavel';
import HomeWorkIcon from '@mui/icons-material/HomeWork';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import NewReleasesIcon from '@mui/icons-material/NewReleases';

const DocumentGeneratorPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));
  
  const documentCategories = [
    {
      id: 'housing',
      title: t('documentGenerator.categories.housing', 'Housing Documents'),
      description: t(
        'documentGenerator.categories.housingDesc',
        'Eviction appeals, lease agreements, and tenant rights documents.'
      ),
      icon: <HomeWorkIcon fontSize={isMobile ? "medium" : "large"} />,
      color: '#4caf50',
      documents: [
        {
          id: 'rental-agreement',
          name: t('documentGenerator.documents.rentalAgreement', 'Rental Agreement'),
          new: true
        },
        {
          id: 'eviction_appeal',
          name: t('documentGenerator.documents.evictionAppeal', 'Eviction Appeal'),
        },
        {
          id: 'lease_termination',
          name: t('documentGenerator.documents.leaseTermination', 'Lease Termination Notice'),
        },
        {
          id: 'repair_request',
          name: t('documentGenerator.documents.repairRequest', 'Repair Request'),
        },
      ],
    },
    {
      id: 'legal',
      title: t('documentGenerator.categories.legal', 'Legal Forms'),
      description: t(
        'documentGenerator.categories.legalDesc',
        'Small claims, expungement requests, and power of attorney forms.'
      ),
      icon: <GavelIcon fontSize={isMobile ? "medium" : "large"} />,
      color: '#2196f3',
      documents: [
        {
          id: 'power-of-attorney',
          name: t('documentGenerator.documents.powerOfAttorney', 'Power of Attorney'),
          new: true
        },
        {
          id: 'small_claims',
          name: t('documentGenerator.documents.smallClaims', 'Small Claims Complaint'),
        },
        {
          id: 'expungement',
          name: t('documentGenerator.documents.expungement', 'Record Expungement'),
        },
        {
          id: 'demand-letter',
          name: t('documentGenerator.documents.demandLetter', 'Demand Letter'),
          new: true
        },
      ],
    },
    {
      id: 'family',
      title: t('documentGenerator.categories.family', 'Family Documents'),
      description: t(
        'documentGenerator.categories.familyDesc',
        'Child custody, divorce, and family support documents.'
      ),
      icon: <FamilyRestroomIcon fontSize={isMobile ? "medium" : "large"} />,
      color: '#ff9800',
      documents: [
        {
          id: 'child_custody',
          name: t('documentGenerator.documents.childCustody', 'Child Custody Agreement'),
        },
        {
          id: 'child_support',
          name: t('documentGenerator.documents.childSupport', 'Child Support Calculation'),
        },
        {
          id: 'divorce_petition',
          name: t('documentGenerator.documents.divorcePetition', 'Divorce Petition'),
        },
      ],
    },
    {
      id: 'business',
      title: t('documentGenerator.categories.business', 'Business Documents'),
      description: t(
        'documentGenerator.categories.businessDesc',
        'Business formation, contracts, and employment agreements.'
      ),
      icon: <BusinessCenterIcon fontSize={isMobile ? "medium" : "large"} />,
      color: '#9c27b0',
      documents: [
        {
          id: 'employment-contract',
          name: t('documentGenerator.documents.employmentContract', 'Employment Contract'),
          new: true
        },
        {
          id: 'llc_formation',
          name: t('documentGenerator.documents.llcFormation', 'LLC Formation'),
        },
        {
          id: 'non_disclosure',
          name: t('documentGenerator.documents.nonDisclosure', 'Non-Disclosure Agreement'),
        },
      ],
    },
    {
      id: 'accessibility',
      title: t('documentGenerator.categories.accessibility', 'Accessibility & Rights'),
      description: t(
        'documentGenerator.categories.accessibilityDesc',
        'ADA accommodation requests, discrimination complaints, and rights assertions.'
      ),
      icon: <AccessibilityNewIcon fontSize={isMobile ? "medium" : "large"} />,
      color: '#f44336',
      documents: [
        {
          id: 'ada_request',
          name: t('documentGenerator.documents.adaRequest', 'ADA Accommodation Request'),
        },
        {
          id: 'discrimination_complaint',
          name: t(
            'documentGenerator.documents.discriminationComplaint',
            'Discrimination Complaint'
          ),
        },
        {
          id: 'civil_rights',
          name: t('documentGenerator.documents.civilRights', 'Civil Rights Assertion'),
        },
      ],
    },
    {
      id: 'general',
      title: t('documentGenerator.categories.general', 'General Documents'),
      description: t(
        'documentGenerator.categories.generalDesc',
        'Wills, living wills, and other general legal documents.'
      ),
      icon: <DescriptionIcon fontSize={isMobile ? "medium" : "large"} />,
      color: '#607d8b',
      documents: [
        { 
          id: 'last-will-testament', 
          name: t('documentGenerator.documents.lastWillTestament', 'Last Will and Testament'),
          new: true
        },
        { 
          id: 'medical-power-of-attorney', 
          name: t('documentGenerator.documents.medicalPowerOfAttorney', 'Medical Power of Attorney'),
          new: true
        },
        { 
          id: 'immigration-assistance',
          name: t('documentGenerator.documents.immigrationAssistance', 'Immigration Assistance Form'),
          new: true
        },
        { 
          id: 'simple_will', 
          name: t('documentGenerator.documents.simpleWill', 'Simple Will') 
        },
        { 
          id: 'living_will', 
          name: t('documentGenerator.documents.livingWill', 'Living Will') 
        },
        {
          id: 'debt_collection',
          name: t('documentGenerator.documents.debtCollection', 'Debt Collection Dispute'),
        },
      ],
    },
  ];
  
  const handleCategorySelect = categoryId => {
    // Navigate to the document generator with the category as a parameter
    navigate(`/document-generator/category/${categoryId}`);
  };
  
  const handleDocumentSelect = (categoryId, documentId) => {
    // Navigate to the document form with the specific document type
    navigate(`/document-generator/form/${documentId}`);
  };
  
  return (
    <Box>
      <Navigation />
      <Container maxWidth="lg" sx={{ mt: { xs: 2, sm: 3, md: 4 }, mb: { xs: 4, sm: 6, md: 8 }, px: { xs: 2, sm: 3 } }}>
        <Box sx={{ mb: { xs: 2, sm: 3 } }}>
          <Typography 
            variant={isMobile ? "h5" : "h4"} 
            component="h1" 
            gutterBottom
            sx={{ fontWeight: 'bold' }}
          >
            {t('documentGenerator.pageTitle', 'Legal Document Generator')}
          </Typography>
          <Typography 
            variant={isMobile ? "body1" : "h6"} 
            color="text.secondary" 
            paragraph
            sx={{ mb: { xs: 1, sm: 2 } }}
          >
            {t(
              'documentGenerator.pageDescription',
              'Create professional legal documents in minutes. Select a category below to get started.'
            )}
          </Typography>
        </Box>
        
        <Alert
          severity="info"
          sx={{ 
            mb: { xs: 2, sm: 3, md: 4 },
            px: { xs: 1, sm: 2 },
            py: { xs: 1, sm: 1.5 }
          }}
          action={
            <Button
              color="primary"
              size={isMobile ? "small" : "medium"}
              variant="outlined"
              endIcon={<ArrowForwardIcon />}
              onClick={() => navigate('/document-templates')}
              sx={{ 
                minWidth: isMobile ? 'auto' : '120px',
                whiteSpace: 'nowrap',
                px: { xs: 1, sm: 2 }
              }}
            >
              {isMobile ? t('Try New') : t('Try New System')}
            </Button>
          }
        >
          <Typography variant={isMobile ? "subtitle2" : "subtitle1"}>
            {t('New Document Templates Available!')}
          </Typography>
          <Typography variant={isMobile ? "caption" : "body2"}>
            {t(
              "We've added new document templates including Last Will and Testament, Medical Power of Attorney, and more. Check out the categories below to see all available templates."
            )}
          </Typography>
        </Alert>
        
        <Grid container spacing={isMobile ? 2 : isTablet ? 3 : 4}>
          {documentCategories.map(category => (
            <Grid item xs={12} sm={6} md={4} key={category.id}>
              <Card
                elevation={2}
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: 6,
                  },
                  borderRadius: { xs: 1, sm: 2 }
                }}
              >
                <CardActionArea
                  onClick={() => handleCategorySelect(category.id)}
                  sx={{
                    flexGrow: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'stretch',
                  }}
                >
                  <Box
                    sx={{
                      p: { xs: 1.5, sm: 2, md: 3 },
                      display: 'flex',
                      justifyContent: 'center',
                      backgroundColor: category.color,
                      color: 'white',
                    }}
                  >
                    {category.icon}
                  </Box>
                  <CardContent sx={{ flexGrow: 1, p: { xs: 1.5, sm: 2 } }}>
                    <Typography 
                      variant={isMobile ? "h6" : "h5"} 
                      component="h2" 
                      gutterBottom
                      sx={{ fontSize: { xs: '1.1rem', sm: '1.25rem', md: '1.5rem' } }}
                    >
                      {category.title}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      color="text.secondary" 
                      paragraph
                      sx={{ 
                        fontSize: { xs: '0.8rem', sm: '0.875rem' },
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',
                        mb: 1
                      }}
                    >
                      {category.description}
                    </Typography>
                    <Typography 
                      variant="subtitle2" 
                      color="primary" 
                      gutterBottom
                      sx={{ 
                        fontSize: { xs: '0.75rem', sm: '0.875rem' },
                        fontWeight: 'bold',
                        mt: 1
                      }}
                    >
                      {t('documentGenerator.availableDocuments', 'Available Documents:')}
                    </Typography>
                    <Box component="ul" sx={{ pl: 2, mb: 0 }}>
                      {category.documents.slice(0, isMobile ? 3 : 4).map(doc => (
                        <Box 
                          component="li" 
                          key={doc.id} 
                          sx={{ 
                            mb: 0.5, 
                            display: 'flex', 
                            alignItems: 'center',
                            fontSize: { xs: '0.8rem', sm: '0.875rem' }
                          }}
                        >
                          <Typography 
                            variant="body2" 
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDocumentSelect(category.id, doc.id);
                            }} 
                            sx={{ 
                              cursor: 'pointer',
                              fontSize: 'inherit',
                              '&:hover': {
                                textDecoration: 'underline'
                              }
                            }}
                          >
                            {doc.name}
                          </Typography>
                          {doc.new && (
                            <Chip
                              icon={<NewReleasesIcon sx={{ fontSize: '0.75rem !important' }} />}
                              label="New"
                              size="small"
                              color="primary"
                              sx={{ 
                                ml: 0.5, 
                                height: { xs: 16, sm: 20 }, 
                                '& .MuiChip-label': { 
                                  px: 0.5,
                                  fontSize: { xs: '0.6rem', sm: '0.7rem' }
                                }
                              }}
                            />
                          )}
                        </Box>
                      ))}
                      {category.documents.length > (isMobile ? 3 : 4) && (
                        <Box component="li" sx={{ listStyle: 'none', mt: 0.5 }}>
                          <Typography 
                            variant="caption" 
                            color="primary"
                            sx={{ 
                              cursor: 'pointer',
                              fontSize: { xs: '0.7rem', sm: '0.75rem' }
                            }}
                          >
                            +{category.documents.length - (isMobile ? 3 : 4)} more...
                          </Typography>
                        </Box>
                      )}
                    </Box>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>
        
        <Box sx={{ mt: { xs: 3, sm: 4, md: 6 }, textAlign: 'center' }}>
          <Button
            variant="contained"
            color="primary"
            size={isMobile ? "medium" : "large"}
            onClick={() => navigate('/document-templates')}
            sx={{ px: { xs: 2, sm: 3, md: 4 } }}
          >
            {t('View All Templates')}
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default DocumentGeneratorPage;