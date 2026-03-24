from people.models import HomeServices
from people.serializers import HomeServicesSerializer
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        summary="Listar serviços da casa",
        description="Retorna uma lista de todos os serviços internos prestados (ex: alimentação, higiene, etc). Permite busca pelo nome da pessoa vinculada."
    ),
    create=extend_schema(
        summary="Registrar serviço da casa",
        description="Cria um novo registro de serviço interno realizado para um paciente ou acompanhante."
    ),
    retrieve=extend_schema(
        summary="Detalhar serviço da casa",
        description="Exibe as informações detalhadas de um registro de serviço específico através do ID."
    ),
    update=extend_schema(
        summary="Atualizar serviço (Integral)",
        description="Substitui completamente os dados de um registro de serviço da casa."
    ),
    partial_update=extend_schema(
        summary="Atualizar serviço (Parcial)",
        description="Permite alterar campos específicos de um registro de serviço sem sobrescrever todos os dados."
    ),
    destroy=extend_schema(
        summary="Remover registro de serviço",
        description="Exclui um registro de serviço do sistema (utiliza exclusão lógica para preservar o histórico)."
    )
)

@extend_schema(tags=['Serviços da Casa'])

class HomeServicesViewSet(viewsets.ModelViewSet):
    queryset = HomeServices.objects.all()
    serializer_class = HomeServicesSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['person__name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]