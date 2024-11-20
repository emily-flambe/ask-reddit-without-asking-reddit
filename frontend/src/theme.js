import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#60a5fa', // Match your soft cyan
    },
    secondary: {
      main: '#94a3b8', // Muted gray-blue
    },
    background: {
      default: '#1e293b', // Dark blue gradient
      paper: '#1f2937', // Deep slate
    },
    text: {
      primary: '#e5e7eb', // Soft white
      secondary: '#cbd5e1', // Light slate
    },
  },
  typography: {
    h1: {
      fontSize: '2.8rem',
      fontWeight: 700,
    },
    h2: {
      fontSize: '1.3rem',
      fontStyle: 'italic',
    },
    body1: {
      fontSize: '1.2rem',
      lineHeight: 1.8,
    },
  },
});

export default theme;
