// URL base usando APENAS /api/ para que o Vite Proxy redirecione para http://127.0.0.1:8000
const API_BASE_URL = '/api/'; 

/**
 * Lida com a resposta do fetch, tratando erros e retornando JSON ou Blob.
 */
const handleResponse = async (response, isBlob = false) => {
    if (!response.ok) {
        // Tenta ler o erro como JSON (assumindo que o backend envia JSON com erro)
        let errorData;
        try {
            errorData = await response.json();
        } catch (e) {
            // Se falhar ao ler JSON, assume erro genérico.
            errorData = { error: 'Erro de Servidor Inesperado (Não-JSON).' };
        }
        
        // Lança um erro com a mensagem do backend ou status.
        throw new Error(errorData.error || response.statusText || `Erro ${response.status}`);
    }
    
    // Retorna o conteúdo como Blob (para imagem) ou JSON (para mensagem decodificada)
    return isBlob ? response.blob() : response.json();
};

/**
 * Envia uma imagem e uma mensagem para codificação. Espera um Blob (imagem).
 */
export const encodeImage = async (imageFile, messageText) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('message', messageText);

    const response = await fetch(API_BASE_URL + 'encode/', {
        method: 'POST',
        body: formData,
    });
    
    return handleResponse(response, true); 
};

/**
 * Envia uma imagem codificada para decodificação. Espera um JSON com a mensagem.
 */
export const decodeImage = async (imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await fetch(API_BASE_URL + 'decode/', {
        method: 'POST',
        body: formData,
    });
    
    const data = await handleResponse(response);
    return data.message;
};