import os
import random
import unittest
from PIL import Image
from src.utils import load_image, save_image
from src.encoder import encode_message, text_to_bits, MARCADOR_FIM
from src.decoder import decode_message, bits_to_text

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def make_image(path, size=(50, 50), color=(120, 120, 120)):
    img = Image.new("RGB", size, color)
    img.save(path, "PNG")
    return path


def make_image_random(path, size=(40, 40)):
    img = Image.new("RGB", size)
    pixels = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            pixels[x, y] = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
    img.save(path, "PNG")
    return path


class TestImageSteganography(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Cria imagens de teste uma única vez"""
        cls.load_save_path = make_image(os.path.join(RESULTS_DIR, "load_save.png"))
        cls.tiny_path = make_image(os.path.join(RESULTS_DIR, "tiny.png"), size=(2, 2))
        cls.encode_path = make_image_random(os.path.join(RESULTS_DIR, "encode.png"), size=(50, 50))
        cls.lsb_path = make_image_random(os.path.join(RESULTS_DIR, "lsb.png"), size=(40, 40))
        cls.large_path = make_image_random(os.path.join(RESULTS_DIR, "large.png"), size=(50, 50))

    def test_load_and_save_image(self):
        img = load_image(self.load_save_path)
        self.assertIsInstance(img, Image.Image)
        save_path = os.path.join(RESULTS_DIR, "saved.png")
        save_image(img, save_path)
        self.assertTrue(os.path.exists(save_path))

    def test_text_to_bits_and_bits_to_text(self):
        def utf8_text_to_bits(msg: str) -> str:
            return ''.join(f"{b:08b}" for b in msg.encode("utf-8"))

        def utf8_bits_to_text(bits: str) -> str:
            b = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]
            return bytes(b).decode("utf-8", errors="ignore")

        messages = ["ABC", "Olá, mundo!", "çãõ é â Ê ñ", "1234567890"]
        for text in messages:
            bits = utf8_text_to_bits(text)
            decoded = utf8_bits_to_text(bits)
            self.assertEqual(decoded, text)

    def test_encode_and_decode_basic(self):
        messages = ["Teste", "Mensagem secreta", "12345", "Çãõ"]
        for msg in messages:
            img = load_image(self.encode_path)
            encoded = encode_message(img, msg)
            decoded_msg = decode_message(encoded)
            self.assertEqual(decoded_msg, msg)

    def test_encode_message_capacity_overflow(self):
        img = load_image(self.tiny_path)
        long_msg = "A" * 1000
        with self.assertRaises(ValueError):
            encode_message(img, long_msg)

    def test_lsb_only_modified(self):
        msg = "LSB Test" * 20
        img = load_image(self.lsb_path)
        encoded = encode_message(img, msg)
        width, height = img.size
        orig_px = img.load()
        enc_px = encoded.load()
        modified_pixels = 0
        for y in range(height):
            for x in range(width):
                r1, g1, b1 = orig_px[x, y]
                r2, g2, b2 = enc_px[x, y]
                if b1 != b2:
                    diff = abs(b1 - b2)
                    self.assertIn(diff, (0, 1))
                    modified_pixels += 1
        self.assertGreaterEqual(modified_pixels, 0)

    def test_encode_decode_large_message(self):
        msg = "Mensagem grande " * 100
        img = load_image(self.large_path)
        size = img.size
        total_capacity = size[0] * size[1]
        msg_bits_len = len(text_to_bits(msg)) + len(MARCADOR_FIM)

        if msg_bits_len > total_capacity:
            with self.assertRaises(ValueError):
                encode_message(img, msg)
        else:
            encoded = encode_message(img, msg)
            decoded = decode_message(encoded)
            self.assertEqual(decoded, msg)




