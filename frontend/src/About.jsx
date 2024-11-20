import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const About = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #1e293b, #334155)',
        color: 'text.primary',
        p: 2,
      }}
    >
      <Paper
        sx={{
          maxWidth: 800,
          p: 4,
          borderRadius: 2,
          boxShadow: 3,
          backgroundColor: 'background.paper',
        }}
      >
        <Typography variant="h1" gutterBottom color="text.primary">
          About Us
        </Typography>
        <Typography variant="h2" gutterBottom color="secondary">
          Our Mission and Values
        </Typography>
        <Typography variant="body1" gutterBottom>
          We are committed to providing the best services to our customers.
          Our dedication to excellence and passion for innovation sets us apart.
        </Typography>
        <Typography
          variant="h2"
          sx={{
            fontStyle: 'italic',
            borderLeft: 4,
            borderColor: 'primary.main',
            pl: 2,
            mt: 4,
          }}
          color="primary"
        >
          "Quality is never an accident. It is always the result of intelligent effort."
        </Typography>
      </Paper>
    </Box>
  );
};

export default About;
