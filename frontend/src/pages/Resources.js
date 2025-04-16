import React from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  Chip,
  Paper,
  InputAdornment,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import DescriptionIcon from '@mui/icons-material/Description';
import SchoolIcon from '@mui/icons-material/School';
import GavelIcon from '@mui/icons-material/Gavel';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import PageLayout from '../components/PageLayout';

function Resources() {
  return (
    <PageLayout
      title="Legal Resources"
      description="Access free legal resources, documents, and educational materials"
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <TextField
            fullWidth
            placeholder="Search resources..."
            variant="outlined"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon color="action" />
                </InputAdornment>
              ),
              sx: {
                bgcolor: 'white',
                borderRadius: 2,
                '& fieldset': {
                  borderColor: 'divider',
                },
              },
            }}
          />
        </Box>

        <Typography variant="h5" component="h2" sx={{ mb: 3, fontWeight: 600 }}>
          <Box component="span" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <DescriptionIcon color="primary" />
            Document Resources
          </Box>
        </Typography>

        <Grid container spacing={3} sx={{ mb: 6 }}>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Legal Forms Library
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 2 }}>
                  Access common legal forms and documents
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Chip label="Forms" sx={{ mr: 1, mb: 1 }} />
                  <Chip label="Templates" sx={{ mb: 1 }} />
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{
                    borderRadius: 2,
                    textTransform: 'none',
                    py: 1,
                  }}
                >
                  Access Documents
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Court Documents
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 2 }}>
                  Standard court filing templates and examples
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Chip label="Court" sx={{ mr: 1, mb: 1 }} />
                  <Chip label="Forms" sx={{ mb: 1 }} />
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{
                    borderRadius: 2,
                    textTransform: 'none',
                    py: 1,
                  }}
                >
                  Access Documents
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Legal Guides
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 2 }}>
                  Step-by-step guides for legal procedures
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Chip label="Guides" sx={{ mr: 1, mb: 1 }} />
                  <Chip label="Education" sx={{ mb: 1 }} />
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{
                    borderRadius: 2,
                    textTransform: 'none',
                    py: 1,
                  }}
                >
                  Access Documents
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Typography variant="h5" component="h2" sx={{ mb: 3, fontWeight: 600 }}>
          <Box component="span" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <SchoolIcon color="primary" />
            Educational Resources
          </Box>
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Know Your Rights
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 2 }}>
                  Essential information about legal rights and protections
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Chip label="Rights" sx={{ mr: 1, mb: 1 }} />
                  <Chip label="Legal" sx={{ mb: 1 }} />
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{
                    borderRadius: 2,
                    textTransform: 'none',
                    py: 1,
                  }}
                >
                  Learn More
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Legal Procedures
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 2 }}>
                  Understanding court procedures and legal processes
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Chip label="Procedures" sx={{ mr: 1, mb: 1 }} />
                  <Chip label="Court" sx={{ mb: 1 }} />
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{
                    borderRadius: 2,
                    textTransform: 'none',
                    py: 1,
                  }}
                >
                  Learn More
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 3, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Legal Terms
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 2 }}>
                  Dictionary of common legal terms and definitions
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Chip label="Terms" sx={{ mr: 1, mb: 1 }} />
                  <Chip label="Dictionary" sx={{ mb: 1 }} />
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{
                    borderRadius: 2,
                    textTransform: 'none',
                    py: 1,
                  }}
                >
                  Learn More
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </PageLayout>
  );
}

export default Resources;
