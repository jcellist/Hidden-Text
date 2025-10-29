from src.utils import load_image, save_image
from src.encoder import encode_message
from src.decoder import decode_message
import sys

def main_menu() -> None:
    """
    Displays the main menu and controls user interaction for encoding/decoding messages.
    """
    while True:
        """ Display main options """
        print("\n=== LSB Steganography Tool ===")
        print("1. Encode message into image")
        print("2. Decode message from image")
        print("3. Exit")

        choice = input("\nChoose an option (1/2/3): ").strip()

        if choice == "1":
            """ Encode mode """
            input_path = input("Enter input image path: ").strip()
            output_path = input("Enter output image path: ").strip()
            message = input("Enter the message to hide: ").strip()

            if not input_path or not output_path or not message:
                print("ERROR: All fields are required.")
                continue

            try:
                image = load_image(input_path)
                encoded_image = encode_message(image, message)
                save_image(encoded_image, output_path)
                print("SUCCESS: Message encoded and image saved.")
            except Exception as e:
                print(f"ERROR: {e}")

        elif choice == "2":
            """ Decode mode """
            input_path = input("Enter the image path to decode: ").strip()
            if not input_path:
                print("ERROR: Image path is required.")
                continue

            try:
                image = load_image(input_path)
                message = decode_message(image)
                print(f"\nDecoded message:\n{message}")
            except Exception as e:
                print(f"ERROR: {e}")

        elif choice == "3":
            """ Exit the program """
            print("Exiting program...")
            sys.exit(0)
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()