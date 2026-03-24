from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import serializers

class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text="Seu nome de usuário")
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Token de autenticação gerado")
    id = serializers.IntegerField(help_text="ID do usuário autenticado")

class CustomObtainAuthToken(ObtainAuthToken):
    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        summary="Login (Obter Token)",
        description="Autentica um usuário através de username e senha, retornando o Token de acesso e o ID do usuário para gestão das sessões.",
        tags=['Autenticação'],
        request=LoginRequestSerializer,  
        responses={200: LoginResponseSerializer} 
    )
    
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'id': token.user_id,
        })