from typing import Union
from PIL import Image

def encode_message(image: Image.Image, bit_sequence: str) -> Image.Image:
    """
    Encodes a bit sequence into the image using the LSB (Least Significant Bit)
    of the Blue (B) channel. Preserves the alpha channel if present.
    
    Args:
        image (Image.Image): PIL image to encode.
        bit_sequence (str): Bit sequence (string containing only '0' and '1').

    Returns:
        Image.Image: Encoded image. If the message is too long, returns the 
                     original image unchanged.

    Raises:
        ValueError: If bit_sequence is not a string or contains characters other than '0' or '1'.
    """
    
    """
    Validate the bit sequence
    """
    if not isinstance(bit_sequence, str) or any(b not in "01" for b in bit_sequence):
        raise ValueError("bit_sequence must be a string containing only '0' and '1'.")

    """
    Convert image to RGBA if it is not RGB or RGBA
    """
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA")

    """
    Load pixels and calculate image capacity
    """
    pixels = image.load()        
    width, height = image.size
    capacity = width * height  # maximum capacity in bits (1 bit per pixel)

    """
    Check if the message fits in the image
    """
    if len(bit_sequence) > capacity:
        print("The message is too long for this image!")
        print(f"Maximum capacity: {capacity} bits — Message length: {len(bit_sequence)} bits.")
        return image 

    """
    Initialize index to track which bit is being encoded
    """
    bit_index = 0
    total_bits = len(bit_sequence)

    """
    Loop through all pixels to encode the message
    """
    for y in range(height):
        for x in range(width):
            if bit_index >= total_bits:
                return image  # message fully encoded

            pixel = pixels[x, y]

            """
            Separate RGB channels and preserve alpha if present
            """
            if len(pixel) == 3:
                R, G, B = pixel
                A = None
            else:
                R, G, B, A = pixel

            """
            Get the current bit of the message
            """
            bit = int(bit_sequence[bit_index])  

            """
            Clear the LSB of Blue and set it to the message bit
            """
            B_cleared = B & 254 
            B_final = B_cleared | bit

            """
            Update the pixel in the image with the new Blue channel
            """
            if A is None:
                pixels[x, y] = (R, G, B_final)
            else:
                pixels[x, y] = (R, G, B_final, A)

            """
            Move to the next bit
            """
            bit_index += 1

    return image

