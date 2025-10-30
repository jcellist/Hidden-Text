from PIL import Image

""" End marker used to indicate where the hidden message stops """
MARCADOR_FIM = "00000000"

def text_to_bits(message: str) -> str:
    """
    Converts a text string into a binary sequence (8 bits per character).
    """
    """ Convert each character into its 8-bit binary representation """
    return "".join(format(ord(char), "08b") for char in message)

def encode_message(image: Image.Image, message: str) -> Image.Image:
    """
    Encodes a text message into the LSB of the blue channel of the given image.
    """
    """ Convert message to bits and append the end marker """
    bit_sequence = text_to_bits(message) + MARCADOR_FIM

    """ Get image data and prepare pixel map """
    pixels = image.load()
    width, height = image.size
    total_pixels = width * height

    """ Check message capacity """
    if len(bit_sequence) > total_pixels:
        raise ValueError("ERROR: Message too long for the image capacity.")

    print("Status: Encoding message into image...")

    """ Encode each bit into the blue channel of the pixels """
    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >= len(bit_sequence):
                """ Stop if the entire message has been encoded """
                return image

            R, G, B = pixels[x, y]
            """ Replace the least significant bit of the blue channel """
            new_B = (B & 254) | int(bit_sequence[bit_index])
            pixels[x, y] = (R, G, new_B)
            bit_index += 1

    return image
