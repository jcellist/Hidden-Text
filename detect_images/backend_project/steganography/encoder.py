from PIL import Image

MARCADOR_FIM = "###END###" 

def text_to_bits(message: str) -> str:
    """
    Converts a text string into a binary sequence (8 bits per character).
    """
    return "".join(format(ord(char), "08b") for char in message)

def encode_message(image: Image.Image, message: str) -> Image.Image:
    """
    Encodes a text message into the LSB of the blue channel of the given image.
    """
    bit_sequence = text_to_bits(message + MARCADOR_FIM)

    pixels = image.load()
    width, height = image.size
    total_pixels = width * height

    if len(bit_sequence) > total_pixels:
        raise ValueError("ERROR: Message too long for the image capacity.")

    print("Status: Encoding message into image...")

    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >= len(bit_sequence):
                return image

            R, G, B = pixels[x, y]
            
            bit_to_hide = int(bit_sequence[bit_index])
            
            new_B = (B & 254) | bit_to_hide
            pixels[x, y] = (R, G, new_B)
            bit_index += 1

    return image