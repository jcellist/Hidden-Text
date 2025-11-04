import React, { useState, useCallback } from 'react';
import {
    Container, Typography, Box, Tabs, Tab,
    Button, TextField, Alert, CircularProgress,
    CssBaseline, createTheme, ThemeProvider, Paper
} from '@mui/material';
import { LockOutlined, LockOpenOutlined, CloudUpload, Message, Download, Visibility } from '@mui/icons-material';
import { encodeImage, decodeImage } from './backend.js';

const theme = createTheme({
    palette: {
        primary: {
            main: '#81C784',
            dark: '#4CAF50',
        },
        secondary: {
            main: '#FFFFFF',
        },
        background: {
            default: '#FAFAFA',
            paper: '#FFFFFF',
        },
    },
    typography: {
        fontFamily: 'Inter, Arial, sans-serif',
        h4: {
            fontWeight: 700,
            color: '#4CAF50',
        },
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: '10px',
                    textTransform: 'none',
                    fontWeight: 600,
                },
                containedPrimary: {
                    backgroundColor: '#81C784',
                    '&:hover': {
                        backgroundColor: '#4CAF50',
                    }
                }
            },
        },
        MuiTabs: {
            styleOverrides: {
                indicator: {
                    backgroundColor: '#4CAF50',
                },
            },
        },
        MuiAlert: {
            styleOverrides: {
                standardSuccess: {
                    backgroundColor: '#E8F5E9',
                    color: '#1B5E20',
                },
            },
        },
    }
});

const Notification = ({ open, message, severity, onClose }) => {
    if (!open) return null;
    const colorMap = {
        success: { bg: theme.palette.success?.light, border: theme.palette.primary.dark },
        error: { bg: theme.palette.error?.light, border: theme.palette.error.main },
        warning: { bg: theme.palette.warning?.light, border: theme.palette.warning.main },
        info: { bg: theme.palette.info?.light, border: theme.palette.info.main },
    };

    return (
        <Alert
            severity={severity}
            onClose={onClose}
            sx={{
                mt: 3,
                mb: 3,
                boxShadow: 3,
                transition: 'opacity 0.3s',
                border: `1px solid ${colorMap[severity]?.border || '#9e9e9e'}`,
                backgroundColor: colorMap[severity]?.bg || '#ffffff',
            }}
        >
            {message}
        </Alert>
    );
};

const EncodeSection = ({ setNotification }) => {
    const [imageFile, setImageFile] = useState(null);
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [encodedImageUrl, setEncodedImageUrl] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setImageFile(file);
        setEncodedImageUrl(null);
        if (file) {
            setNotification(`Arquivo selecionado: ${file.name}`, 'info');
        }
    };

    const handleEncode = async (e) => {
        e.preventDefault();
        if (!imageFile || !message) {
            setNotification('Por favor, selecione uma imagem e digite uma mensagem.', 'warning');
            return;
        }

        setIsLoading(true);
        setEncodedImageUrl(null);

        try {
            const imageBlob = await encodeImage(imageFile, message);
            const url = URL.createObjectURL(imageBlob);
            setEncodedImageUrl(url);
            setNotification('Codificação concluída! Clique em Baixar Imagem.', 'success');
        } catch (error) {
            console.error('Erro de Codificação:', error);
            setNotification(error.message, 'error');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box component="form" onSubmit={handleEncode} sx={{ display: 'grid', gap: 3, pt: 4 }}>
            <Typography variant="h6" sx={{ color: theme.palette.primary.dark, borderBottom: '2px solid #e0e0e0', pb: 1 }}>
                Selecione Imagem e Mensagem
            </Typography>

            <Button
                variant="outlined"
                component="label"
                startIcon={<CloudUpload />}
                fullWidth
                sx={{
                    height: 60,
                    fontSize: '1.1rem',
                    borderColor: theme.palette.primary.dark,
                    color: theme.palette.primary.dark,
                    '&:hover': {
                        borderColor: theme.palette.primary.dark,
                        backgroundColor: theme.palette.primary.light
                    }
                }}
            >
                {imageFile ? `Arquivo: ${imageFile.name}` : 'Carregar Imagem para Esconder'}
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    required
                    hidden
                />
            </Button>

            <TextField
                label="Mensagem Secreta para Codificar"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                fullWidth
                required
                multiline
                rows={3}
                variant="outlined"
                InputProps={{ startAdornment: <Message sx={{ mr: 1, color: theme.palette.primary.main }} /> }}
                helperText={`Caracteres: ${message.length}. Certifique-se de que a mensagem é curta.`}
            />

            <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
                fullWidth
                disabled={isLoading || !imageFile || !message}
                startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <LockOutlined />}
                sx={{ mt: 2, height: 56, fontSize: '1.2rem' }}
            >
                {isLoading ? 'Codificando...' : 'Codificar e Gerar Imagem'}
            </Button>

            {encodedImageUrl && (
                <Paper elevation={4} sx={{ mt: 3, p: 3, bgcolor: '#E8F5E9', border: `2px solid ${theme.palette.primary.dark}` }}>
                    <Typography variant="subtitle1" fontWeight="bold" color="primary" sx={{ mb: 2 }}>
                        Sucesso! Imagem Oculta Pronta
                    </Typography>
                    <Button
                        variant="contained"
                        color="primary"
                        component="a"
                        href={encodedImageUrl}
                        download="encoded_image.png"
                        startIcon={<Download />}
                        fullWidth
                        sx={{
                            fontSize: '1.1rem',
                            backgroundColor: theme.palette.primary.dark,
                            '&:hover': { backgroundColor: theme.palette.primary.main }
                        }}
                    >
                        Baixar Imagem Codificada (.png)
                    </Button>
                </Paper>
            )}
        </Box>
    );
};

const DecodeSection = ({ setNotification }) => {
    const [imageFile, setImageFile] = useState(null);
    const [decodedMessage, setDecodedMessage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setImageFile(file);
        setDecodedMessage(null);
        if (file) {
            setNotification(`Arquivo selecionado: ${file.name}`, 'info');
        }
    };

    const handleDecode = async (e) => {
        e.preventDefault();
        if (!imageFile) {
            setNotification('Por favor, selecione a imagem codificada.', 'warning');
            return;
        }

        setIsLoading(true);
        setDecodedMessage(null);

        try {
            const message = await decodeImage(imageFile);
            setDecodedMessage(message);
            setNotification('Mensagem decodificada com sucesso!', 'success');
        } catch (error) {
            console.error('Erro de Decodificação:', error);
            setNotification(error.message, 'error');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box component="form" onSubmit={handleDecode} sx={{ display: 'grid', gap: 3, pt: 4 }}>
            <Typography variant="h6" sx={{ color: theme.palette.primary.dark, borderBottom: '2px solid #e0e0e0', pb: 1 }}>
                Carregar Imagem Codificada
            </Typography>

            <Button
                variant="outlined"
                component="label"
                startIcon={<CloudUpload />}
                fullWidth
                sx={{
                    height: 60,
                    fontSize: '1.1rem',
                    borderColor: theme.palette.primary.dark,
                    color: theme.palette.primary.dark,
                    '&:hover': {
                        borderColor: theme.palette.primary.dark,
                        backgroundColor: theme.palette.primary.light
                    }
                }}
            >
                {imageFile ? `Arquivo: ${imageFile.name}` : 'Carregar Imagem para Revelar'}
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    required
                    hidden
                />
            </Button>

            <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
                fullWidth
                disabled={isLoading || !imageFile}
                startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <LockOpenOutlined />}
                sx={{ mt: 2, height: 56, fontSize: '1.2rem' }}
            >
                {isLoading ? 'Decodificando...' : 'Decodificar e Revelar Mensagem'}
            </Button>

            {decodedMessage && (
                <Paper
                    elevation={4}
                    sx={{
                        mt: 3,
                        p: 3,
                        bgcolor: theme.palette.info.light,
                        border: `2px solid ${theme.palette.info.main}`
                    }}
                >
                    <Typography
                        variant="subtitle1"
                        fontWeight="bold"
                        color="info"
                        sx={{ mb: 1, display: 'flex', alignItems: 'center' }}
                    >
                        <Visibility sx={{ mr: 1 }} /> Mensagem Secreta Revelada:
                    </Typography>

                    <Box
                        sx={{
                            mt: 1,
                            p: 2,
                            bgcolor: '#ffffff',
                            borderRadius: 1,
                            border: '1px solid #bbdefb',
                            maxWidth: '100%',
                            overflowX: 'auto'
                        }}
                    >
                        <Typography
                            variant="body1"
                            sx={{
                                whiteSpace: 'pre-wrap',
                                wordBreak: 'break-word',
                                overflowWrap: 'break-word',
                                color: 'text.primary'
                            }}
                        >
                            {decodedMessage}
                        </Typography>
                    </Box>
                </Paper>
            )}
        </Box>
    );
};

const App = () => {
    const [tabValue, setTabValue] = useState(0);
    const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });

    const updateNotification = useCallback((message, severity = 'success') => {
        setNotification({ open: true, message, severity });
    }, []);

    const handleCloseNotification = () => {
        setNotification({ ...notification, open: false });
    };

    const handleTabChange = (event, newValue) => {
        setTabValue(newValue);
        handleCloseNotification();
    };

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Box
                sx={{
                    minHeight: '100vh',
                    backgroundColor: theme.palette.background.default,
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: { xs: 'flex-start', md: 'center' },
                    p: 2
                }}
            >
                <Paper
                    elevation={10}
                    sx={{
                        width: '100%',
                        maxWidth: '750px',
                        borderRadius: 3,
                        p: { xs: 2, md: 4 },
                        mt: { xs: 2, md: 0 }
                    }}
                >
                    <Typography
                        variant="h4"
                        component="h1"
                        align="center"
                        sx={{
                            pb: 2,
                            mb: 2,
                            borderBottom: `4px solid ${theme.palette.primary.dark}`,
                            letterSpacing: 1
                        }}
                    >
                        <LockOutlined sx={{ mr: 1, verticalAlign: 'middle', fontSize: '1.5em' }} />
                        Steganography Client
                    </Typography>

                    <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                        <Tabs value={tabValue} onChange={handleTabChange} centered>
                            <Tab label="Codificar (Esconder)" icon={<LockOutlined />} iconPosition="start" />
                            <Tab label="Decodificar (Revelar)" icon={<LockOpenOutlined />} iconPosition="start" />
                        </Tabs>
                    </Box>

                    <Box sx={{ p: 3, pb: 0 }}>
                        {tabValue === 0 && <EncodeSection setNotification={updateNotification} />}
                        {tabValue === 1 && <DecodeSection setNotification={updateNotification} />}
                    </Box>

                    <Notification
                        {...notification}
                        onClose={handleCloseNotification}
                    />
                </Paper>
            </Box>
        </ThemeProvider>
    );
};

export default App;
