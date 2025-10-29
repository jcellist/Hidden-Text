from PIL import Image
""" Importa o marcador do encoder para garantir consistência """
from src.encoder import MARCADOR_FIM 

def bits_para_texto(sequencia_bits: str) -> str:
    """Converte a sequência binária (blocos de 8 bits) de volta para texto ASCII."""
    mensagem = ""
    """ Itera de 8 em 8 bits (o tamanho de um caractere) """
    for i in range(0, len(sequencia_bits), 8):
        bloco_8_bits = sequencia_bits[i:i + 8]
        
        try:
            """ Converte o binário para inteiro (base 2) e depois para caractere """
            valor_inteiro = int(bloco_8_bits, 2) 
            mensagem += chr(valor_inteiro)
        except ValueError:
            break
            
    return mensagem

def decodificar_mensagem(imagem: Image.Image) -> str:
    """
    Extrai o texto escondido lendo o LSB do canal Azul de cada pixel até
    encontrar o marcador de fim.
    """
    pixels = imagem.load()
    largura, altura = imagem.size
    sequencia_bits_total = ""
    marcador_len = len(MARCADOR_FIM)
    
    print("Status: Lendo LSBs da imagem...")

    for y in range(altura):
        for x in range(largura):
            R, G, B = pixels[x, y]
            
            """ Extração do LSB do canal Azul """
            lsb = B & 1 
            sequencia_bits_total += str(lsb)
            
            """ Checagem eficiente do marcador de fim """
            if len(sequencia_bits_total) >= marcador_len and sequencia_bits_total.endswith(MARCADOR_FIM):
                """ Retorna a mensagem já convertida para texto, removendo o marcador """
                return bits_para_texto(sequencia_bits_total[:-marcador_len])

    return "ERRO: Mensagem oculta não encontrada ou não terminada."