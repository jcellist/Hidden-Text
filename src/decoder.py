from PIL import Image
""" Import the end marker from the encoder to ensure consistency """
from src.encoder import MARCADOR_FIM


def bits_to_text(bit_sequence: str) -> str:
    """
    Converts a binary sequence (8-bit blocks) back into ASCII text.
    """
    message = ""
    """ Iterate over the sequence 8 bits at a time (1 byte = 1 character) """
    for i in range(0, len(bit_sequence), 8):
        byte_block = bit_sequence[i:i + 8]

        try:
            """ Convert binary to integer (base 2), then to a character """
            int_value = int(byte_block, 2)
            message += chr(int_value)
        except ValueError:
            """ Stop if the block cannot be converted (incomplete byte, etc.) """
            break

    return message


def decode_message(image: Image.Image) -> str:
    """
    Extracts the hidden text by reading the Least Significant Bit (LSB)
    of the Blue channel in each pixel until the end marker is found.
    """
    pixels = image.load()
    width, height = image.size
    bit_sequence = ""
    marker_len = len(MARCADOR_FIM)

    print("Status: Reading LSBs from the image...")

    for y in range(height):
        for x in range(width):
            R, G, B = pixels[x, y]

            """ Extract the LSB of the Blue channel """
            lsb = B & 1
            bit_sequence += str(lsb)

            """ Check if the end marker has been reached """
            if len(bit_sequence) >= marker_len and bit_sequence.endswith(MARCADOR_FIM):
                """ Return the decoded message (without the marker) """
                return bits_to_text(bit_sequence[:-marker_len])

    return "ERROR: Hidden message not found or incomplete."
