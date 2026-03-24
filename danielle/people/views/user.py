from rest_framework import generics
from django.contrib.auth.models import User
from people.serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

# --- AQUI ESTÃO AS CLASSES QUE O ERRO DISSE QUE NÃO ACHOU ---

@extend_schema(
    summary="Criar novo usuário",
    description="Permite o cadastro de novos usuários (operadores) no sistema.",
    tags=['Autenticação']
)
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

@extend_schema(
    summary="Dados do usuário atual",
    description="Retorna as informações do usuário autenticado que está realizando a requisição.",
    tags=['Autenticação']
)
class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

# --- SUA VIEW DE LOGIN QUE JÁ ESTAVA CERTA ---

class CustomObtainAuthToken(ObtainAuthToken):
    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        summary="Login (Obter Token)",
        description="Autentica um usuário através de username e senha, retornando o Token de acesso e o ID do usuário.",
        tags=['Autenticação']
    )
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'id': token.user_id,
        })