from people.models import ProfessionalServices
from people.serializers import ProfessionalServicesSerializer
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        summary="Listar serviços profissionais",
        description="Retorna o histórico de atendimentos realizados por profissionais externos (médicos, fisioterapeutas, etc) para os residentes."
    ),
    create=extend_schema(
        summary="Registrar atendimento profissional",
        description="Cadastra um novo atendimento ou procedimento realizado por um profissional de saúde na Casa de Apoio."
    ),
    retrieve=extend_schema(
        summary="Detalhar atendimento profissional",
        description="Exibe os dados completos de um atendimento específico, incluindo o profissional responsável e a data."
    ),
    update=extend_schema(
        summary="Atualizar atendimento (Integral)",
        description="Substitui todos os campos de um registro de serviço profissional."
    ),
    partial_update=extend_schema(
        summary="Atualizar atendimento (Parcial)",
        description="Permite corrigir campos específicos de um atendimento já registrado."
    ),
    destroy=extend_schema(
        summary="Remover atendimento profissional",
        description="Exclui o registro do atendimento do sistema (mantendo o rastreio via exclusão lógica)."
    )
)

@extend_schema(tags=['Serviços Profissionais'])

class ProfessionalServicesViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalServices.objects.all()
    serializer_class = ProfessionalServicesSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['professional__name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]