from typing import Union
from PIL import Image

def codificar_mensagem(imagem: Image.Image, sequencia_bits: str) -> Image.Image:

    if not isinstance(sequencia_bits, str) or any(b not in "01" for b in sequencia_bits):
        raise ValueError("sequencia_bits deve ser uma string contendo apenas '0' e '1'.")

    if imagem.mode not in ("RGB", "RGBA"):
        imagem = imagem.convert("RGBA")

    pixels = imagem.load()        
    largura, altura = imagem.size
    capacidade = largura * altura  

    if len(sequencia_bits) > capacidade:
        print("A mensagem é muito longa para esta imagem!")
        print(f"Capacidade máxima: {capacidade} bits — Mensagem: {len(sequencia_bits)} bits.")
        return imagem 

    indice_bit = 0
    tamanho_bits = len(sequencia_bits)

    for y in range(altura):
        for x in range(largura):
            if indice_bit >= tamanho_bits:
                return imagem  

            pixel = pixels[x, y]

            if len(pixel) == 3:
                R, G, B = pixel
                A = None
            else:
                R, G, B, A = pixel

            bit_msg = int(sequencia_bits[indice_bit])  

            B_zerado = B & 254 

            B_final = B_zerado | bit_msg

            if A is None:
                pixels[x, y] = (R, G, B_final)
            else:
                pixels[x, y] = (R, G, B_final, A)

            indice_bit += 1

    return imagem