import React from 'react';
import { Box, Container, Typography, Grid } from '@mui/material';
import { motion } from 'framer-motion';

const TrustSignals = () => {
  const partners = [
    {
      name: "Legal Aid Society",
      logo: "/images/partners/legal-aid-society.png",
      alt: "Legal Aid Society Logo"
    },
    {
      name: "Pro Bono Net",
      logo: "/images/partners/pro-bono-net.png",
      alt: "Pro Bono Net Logo"
    },
    {
      name: "American Bar Association",
      logo: "/images/partners/aba.png",
      alt: "American Bar Association Logo"
    }
  ];

  return (
    <Box sx={{ py: 6, bgcolor: 'background.default' }}>
      <Container maxWidth="lg">
        <Typography
          variant="h6"
          align="center"
          color="text.secondary"
          gutterBottom
          sx={{ mb: 4 }}
        >
          Trusted By Leading Organizations
        </Typography>
        <Grid
          container
          spacing={4}
          justifyContent="center"
          alignItems="center"
        >
          {partners.map((partner, index) => (
            <Grid item key={partner.name}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
              >
                <Box
                  component="img"
                  src={partner.logo}
                  alt={partner.alt}
                  sx={{
                    height: 60,
                    filter: 'grayscale(100%)',
                    opacity: 0.7,
                    transition: 'all 0.3s ease-in-out',
                    '&:hover': {
                      filter: 'grayscale(0%)',
                      opacity: 1,
                      transform: 'scale(1.05)'
                    }
                  }}
                />
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default TrustSignals; 