from PIL import Image
""" Import the end marker from the encoder to ensure consistency """
from backend_project.steganography.encoder import MARCADOR_FIM


def text_to_bits(text: str) -> str:
    """
    Converts a text string into a binary sequence.
    This is used to get the binary representation of the END MARKER.
    """
    return ''.join(format(ord(char), '08b') for char in text)


def bits_to_text(bit_sequence: str) -> str:
    """
    Converts a binary sequence (8-bit blocks) back into ASCII text.
    """
    message = ""
    for i in range(0, len(bit_sequence), 8):
        byte_block = bit_sequence[i:i + 8]
        
        if len(byte_block) < 8:
            break

        try:
            int_value = int(byte_block, 2)
            message += chr(int_value)
        except ValueError:
            break

    return message


def decode_message(image: Image.Image) -> str:
    """
    Extracts the hidden text by reading the Least Significant Bit (LSB)
    of the Blue channel in each pixel until the end marker is found.
    """
    MARCADOR_FIM_BINARIO = text_to_bits(MARCADOR_FIM)
    marker_len_bits = len(MARCADOR_FIM_BINARIO)
    
    pixels = image.load()
    width, height = image.size
    bit_sequence = ""
    
    print("Status: Reading LSBs from the image...")

    for y in range(height):
        for x in range(width):
            R, G, B = pixels[x, y]

            """ Extrai o LSB do canal Blue """
            lsb = B & 1
            bit_sequence += str(lsb)

            """ CRUCIAL: Checa se a sequência de BITS extraída termina com o MARCADOR BINÁRIO """
            if len(bit_sequence) >= marker_len_bits and bit_sequence.endswith(MARCADOR_FIM_BINARIO):
                
                payload_bits = bit_sequence[:-marker_len_bits]
                
                decoded_text = bits_to_text(payload_bits)

                return decoded_text

    return "Nenhuma mensagem secreta encontrada ou a imagem está corrompida."
