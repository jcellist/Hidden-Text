from PIL import Image

def load_image(path: str) -> Image.Image:
    """
    Loads an image from the given path and converts it to RGB mode.
    """
    try:
        """ Open and convert the image to RGB """
        image = Image.open(path).convert("RGB")
        print("Status: Image loaded successfully.")
        return image
    except FileNotFoundError:
        """ Handle missing file error """
        raise FileNotFoundError(f"ERROR: Image not found at path: {path}")
    except Exception as e:
        """ Handle any unexpected error """
        raise RuntimeError(f"ERROR: Could not open image. Details: {e}")

def save_image(image: Image.Image, path: str) -> None:
    """
    Saves the given image to the specified path in PNG format.
    """
    try:
        """ Save the image as PNG to preserve bit information """
        image.save(path, "PNG")
        print(f"Status: Image saved at {path}")
    except Exception as e:
        """ Handle any save-related errors """
        raise RuntimeError(f"ERROR: Could not save image. Details: {e}")