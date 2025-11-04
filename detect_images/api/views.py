from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from PIL import Image
import io
from backend_project.steganography.encoder import encode_message
from backend_project.steganography.decoder import decode_message


@api_view(['POST'])
@parser_classes([MultiPartParser])
def encode_view(request):
    """ Endpoint: /api/encode/ - Codifica mensagem na imagem e retorna o arquivo. """
    try:
        image_file = request.FILES.get('image')
        message = request.data.get('message')

        if not image_file or not message:
            return Response(
                {"error": "Parâmetros 'image' (arquivo) e 'message' (texto) são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        image = Image.open(image_file).convert("RGB")
        encoded_image = encode_message(image, message)

        byte_arr = io.BytesIO()
        encoded_image.save(byte_arr, format='PNG')
        
        response = HttpResponse(byte_arr.getvalue(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="encoded_image.png"'
        response['Access-Control-Allow-Origin'] = '*' 
        
        return response

    except ValueError as e: 
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Erro interno no servidor ao codificar: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser])
def decode_view(request):
    """ Endpoint: /api/decode/ - Decodifica mensagem da imagem e retorna JSON. """
    try:
        image_file = request.FILES.get('image')

        if not image_file:
            return Response(
                {"error": "Parâmetro 'image' (arquivo) é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        image = Image.open(image_file).convert("RGB")
        message = decode_message(image)

        if not message:
            message = "Nenhuma mensagem secreta encontrada." 
        
        response = Response({"message": message}, status=status.HTTP_200_OK)
        
        response['Access-Control-Allow-Origin'] = '*'
        
        return response

    except Exception as e:
        return Response({"error": f"Erro interno no servidor ao decodificar: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
