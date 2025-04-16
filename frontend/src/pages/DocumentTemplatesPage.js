import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Box,
  TextField,
  InputAdornment,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tabs,
  Tab,
  Divider,
  Paper,
  useMediaQuery,
  Alert,
  Button,
  Badge,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useTheme } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import SearchIcon from '@mui/icons-material/Search';
import FilterListIcon from '@mui/icons-material/FilterList';
import InfoIcon from '@mui/icons-material/Info';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import NewReleasesIcon from '@mui/icons-material/NewReleases';
import LabelImportantIcon from '@mui/icons-material/LabelImportant';
import DocumentTemplateCard from '../components/DocumentTemplateCard';
import { documentTemplates, getAllTemplateCategories } from '../data/documentTemplateLibrary';
const DocumentTemplatesPage = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  // Get all template categories
  const allCategories = getAllTemplateCategories();
  // State
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedAccessLevel, setSelectedAccessLevel] = useState('all');
  const [showNewOnly, setShowNewOnly] = useState(false);
  const [filteredTemplates, setFilteredTemplates] = useState(documentTemplates);
  const [showInfoBanner, setShowInfoBanner] = useState(true);
  // Mock user access level - in a real app, this would come from auth context
  const userAccessLevel = 'free'; // Changed from 'registered' to 'free'
  // Get new templates
  const newTemplates = documentTemplates.filter(template => template.isNew);
  // Filter templates based on search, category, access level, and new status
  useEffect(() => {
    let filtered = [...documentTemplates];
    // Filter by search term
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(
        template =>
          template.name.toLowerCase().includes(term) ||
          template.description.toLowerCase().includes(term) ||
          (template.tags && template.tags.some(tag => tag.toLowerCase().includes(term)))
      );
    }
    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(template => template.category === selectedCategory);
    }
    // Filter by access level
    if (selectedAccessLevel !== 'all') {
      filtered = filtered.filter(template => template.accessLevel === selectedAccessLevel);
    }
    // Filter by new status
    if (showNewOnly) {
      filtered = filtered.filter(template => template.isNew);
    }
    setFilteredTemplates(filtered);
  }, [searchTerm, selectedCategory, selectedAccessLevel, showNewOnly]);
  // Handle search input change
  const handleSearchChange = event => {
    setSearchTerm(event.target.value);
  };
  // Handle category filter change
  const handleCategoryChange = event => {
    setSelectedCategory(event.target.value);
  };
  // Handle access level filter change
  const handleAccessLevelChange = event => {
    setSelectedAccessLevel(event.target.value);
  };
  // Toggle new templates filter
  const handleToggleNewOnly = () => {
    setShowNewOnly(!showNewOnly);
  };
  // Clear all filters
  const handleClearFilters = () => {
    setSearchTerm('');
    setSelectedCategory('all');
    setSelectedAccessLevel('all');
    setShowNewOnly(false);
  };
  const handleInfoBannerClose = () => {
    setShowInfoBanner(false);
  };
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {showInfoBanner && (
        <Alert
          severity="info"
          icon={<InfoIcon />}
          sx={{ mb: 4 }}
          onClose={handleInfoBannerClose}
          action={
            <Button
              color="primary"
              size="small"
              variant="outlined"
              startIcon={<PersonAddIcon />}
              onClick={() => navigate('/register')}
            >
              {t('Create Free Account')}
            </Button>
          }
        >
          <Typography variant="subtitle1">{t('Most templates are freely available!')}</Typography>
          <Typography variant="body2">
            {t(
              'Create a free account to save your documents, track your progress, and access additional templates. No payment required.'
            )}
          </Typography>
        </Alert>
      )}
      <Box
        sx={{
          mb: 4,
          display: 'flex',
          alignItems: 'center',
          flexWrap: 'wrap',
          justifyContent: 'space-between',
        }}
      >
        <div>
          <Typography variant="h4" component="h1" gutterBottom>
            {t('Document Templates')}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            {t('Browse our library of legal document templates for various situations.')}
          </Typography>
        </div>
        {newTemplates.length > 0 && (
          <Chip
            icon={<NewReleasesIcon />}
            label={`${newTemplates.length} New Templates Added!`}
            color="secondary"
            sx={{
              height: 'auto',
              py: 1,
              mt: { xs: 2, md: 0 },
              borderRadius: '16px',
              fontSize: '1rem',
              fontWeight: 'bold',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            }}
            onClick={() => setShowNewOnly(true)}
          />
        )}
      </Box>
      {/* New Templates Banner - Only show if there are new templates and not filtering */}
      {newTemplates.length > 0 &&
        !showNewOnly &&
        searchTerm === '' &&
        selectedCategory === 'all' &&
        selectedAccessLevel === 'all' && (
          <Paper
            elevation={3}
            sx={{
              p: 3,
              mb: 4,
              borderRadius: '8px',
              background: 'linear-gradient(45deg, #6a1b9a 30%, #9c27b0 90%)',
              color: 'white',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                right: 0,
                width: '150px',
                height: '150px',
                background:
                  'radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%)',
                borderRadius: '0 0 0 100%',
              }}
            />
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <NewReleasesIcon sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2" fontWeight="bold">
                {t('Just Added: New Document Templates!')}
              </Typography>
            </Box>
            <Typography variant="body1" sx={{ mb: 2, maxWidth: '80%' }}>
              {t(
                "We've expanded our template library with 10 new templates covering immigration, civil rights, business, healthcare, and more!"
              )}
            </Typography>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => setShowNewOnly(true)}
              startIcon={<LabelImportantIcon />}
              sx={{
                bgcolor: 'white',
                color: '#6a1b9a',
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.9)',
                },
              }}
            >
              {t('View New Templates')}
            </Button>
          </Paper>
        )}
      <Paper sx={{ p: 3, mb: 4, borderRadius: '8px' }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder={t('Search templates...')}
              value={searchTerm}
              onChange={handleSearchChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth variant="outlined">
              <InputLabel id="category-select-label">{t('Category')}</InputLabel>
              <Select
                labelId="category-select-label"
                value={selectedCategory}
                onChange={handleCategoryChange}
                label={t('Category')}
              >
                <MenuItem value="all">{t('All Categories')}</MenuItem>
                {allCategories.map(category => (
                  <MenuItem key={category} value={category}>
                    {category}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth variant="outlined">
              <InputLabel id="access-select-label">{t('Access Level')}</InputLabel>
              <Select
                labelId="access-select-label"
                value={selectedAccessLevel}
                onChange={handleAccessLevelChange}
                label={t('Access Level')}
              >
                <MenuItem value="all">{t('All Levels')}</MenuItem>
                <MenuItem value="free">{t('Free')}</MenuItem>
                <MenuItem value="registered">{t('Account Required')}</MenuItem>
                <MenuItem value="premium">{t('Premium')}</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        <Box display="flex" alignItems="center" mt={2} flexWrap="wrap">
          <FilterListIcon fontSize="small" sx={{ mr: 1 }} />
          <Typography variant="body2" sx={{ mr: 2 }}>
            {t('Filters:')}
          </Typography>
          {searchTerm && (
            <Chip
              label={`${t('Search')}: ${searchTerm}`}
              size="small"
              onDelete={() => setSearchTerm('')}
              sx={{ mr: 1, mb: { xs: 1, md: 0 } }}
            />
          )}
          {selectedCategory !== 'all' && (
            <Chip
              label={`${t('Category')}: ${selectedCategory}`}
              size="small"
              onDelete={() => setSelectedCategory('all')}
              sx={{ mr: 1, mb: { xs: 1, md: 0 } }}
            />
          )}
          {selectedAccessLevel !== 'all' && (
            <Chip
              label={`${t('Access')}: ${
                selectedAccessLevel === 'free'
                  ? t('Free')
                  : selectedAccessLevel === 'registered'
                    ? t('Account Required')
                    : t('Premium')
              }`}
              size="small"
              onDelete={() => setSelectedAccessLevel('all')}
              sx={{ mr: 1, mb: { xs: 1, md: 0 } }}
            />
          )}
          <Chip
            icon={<NewReleasesIcon />}
            label={t('New Templates Only')}
            size="small"
            color={showNewOnly ? 'secondary' : 'default'}
            onClick={handleToggleNewOnly}
            sx={{ mr: 1, mb: { xs: 1, md: 0 } }}
          />
          {(searchTerm ||
            selectedCategory !== 'all' ||
            selectedAccessLevel !== 'all' ||
            showNewOnly) && (
            <Chip
              label={t('Clear All')}
              size="small"
              onClick={handleClearFilters}
              variant="outlined"
              sx={{ mb: { xs: 1, md: 0 } }}
            />
          )}
        </Box>
      </Paper>
      {filteredTemplates.length === 0 ? (
        <Box textAlign="center" py={8}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            {t('No templates found matching your criteria')}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {t('Try adjusting your filters or search term')}
          </Typography>
        </Box>
      ) : (
        <>
          {/* New Templates Section - Only show when there are new templates in the filtered results */}
          {filteredTemplates.some(template => template.isNew) && !showNewOnly && (
            <>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 6, mb: 2 }}>
                <NewReleasesIcon color="secondary" sx={{ mr: 1 }} />
                <Typography variant="h5" component="h2">
                  {t('New Templates')}
                </Typography>
              </Box>
              <Grid container spacing={3}>
                {filteredTemplates
                  .filter(template => template.isNew)
                  .map(template => (
                    <Grid item xs={12} sm={6} md={4} key={template.id}>
                      <Badge
                        badgeContent="NEW"
                        color="secondary"
                        sx={{
                          width: '100%',
                          '& .MuiBadge-badge': {
                            fontSize: '0.75rem',
                            fontWeight: 'bold',
                            padding: '0 6px',
                            height: '24px',
                            borderRadius: '12px',
                          },
                        }}
                      >
                        <DocumentTemplateCard
                          template={template}
                          userAccessLevel={userAccessLevel}
                        />
                      </Badge>
                    </Grid>
                  ))}
              </Grid>
              <Divider sx={{ my: 6 }} />
            </>
          )}
          {/* Featured Templates Section - If not showing new-only */}
          {!showNewOnly && filteredTemplates.some(template => template.featured) && (
            <>
              <Typography variant="h5" component="h2" gutterBottom>
                {t('Featured Templates')}
              </Typography>
              <Grid container spacing={3} mb={4}>
                {filteredTemplates
                  .filter(template => template.featured)
                  .map(template => (
                    <Grid item xs={12} sm={6} md={4} key={template.id}>
                      <DocumentTemplateCard template={template} userAccessLevel={userAccessLevel} />
                    </Grid>
                  ))}
              </Grid>
              <Divider sx={{ my: 4 }} />
            </>
          )}
          {/* All Templates Section */}
          <Typography variant="h5" component="h2" gutterBottom>
            {t('All Templates')}
          </Typography>
          <Grid container spacing={3}>
            {filteredTemplates.map(template => (
              <Grid item xs={12} sm={6} md={4} key={template.id}>
                <DocumentTemplateCard template={template} userAccessLevel={userAccessLevel} />
              </Grid>
            ))}
          </Grid>
        </>
      )}
    </Container>
  );
};
export default DocumentTemplatesPage;