import React from 'react';
import ReactDOM from 'react-dom/client';
// Importando o componente principal 'App' a partir do seu arquivo 'steganography.jsx'
import App from './steganography.jsx'; 
import { createTheme, ThemeProvider, CssBaseline } from '@mui/material';

// Tema básico do MUI para aplicar globalmente
const theme = createTheme({});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline /> {/* Para resetar o CSS e usar o padrão MUI */}
      <App />
    </ThemeProvider>
  </React.StrictMode>
);