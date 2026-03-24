from people.models import Checkin
from people.models import PatientCompanionCheckin
from people.serializers import CheckinSerializer
from people.serializers import PatientCompanionCheckinSerializer
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        summary="Listar check-ins",
        description="Retorna uma lista de todos os check-ins realizados na Casa de Apoio. Permite busca por nome da pessoa e filtro por status (ativo/inativo)."
    ),
    create=extend_schema(
        summary="Registrar novo check-in",
        description="Cria um novo registro de entrada para um paciente ou acompanhante na instituição."
    ),
    retrieve=extend_schema(
        summary="Detalhar check-in",
        description="Retorna os detalhes completos de um check-in específico através do seu ID."
    ),
    update=extend_schema(
        summary="Atualizar check-in (Integral)",
        description="Substitui integralmente todos os dados de um registro de estadia."
    ),
    partial_update=extend_schema(
        summary="Atualizar check-in (Parcial)",
        description="Atualiza parcialmente um registro. Muito utilizado para realizar o Check-out alterando a flag 'active' para falso."
    ),
    destroy=extend_schema(
        summary="Excluir check-in",
        description="Remove um registro de check-in do sistema (utiliza a exclusão lógica, mantendo o histórico no banco)."
    )
)
@extend_schema(tags=['Gestão de Check-ins']) 
class CheckinViewSet(viewsets.ModelViewSet):
    queryset = Checkin.objects.all()
    serializer_class = CheckinSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['person__name']
    filterset_fields = ['active']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]

@extend_schema_view(
    list=extend_schema(summary="Listar check-ins de acompanhantes"), 
    create=extend_schema(summary="Registrar check-in de acompanhante"),
    retrieve=extend_schema(summary="Detalhar check-in de acompanhante"),
    update=extend_schema(summary="Atualizar acompanhante (Integral)"),
    partial_update=extend_schema(summary="Atualizar acompanhante (Parcial)"),
    destroy=extend_schema(summary="Remover check-in de acompanhante"),
)
@extend_schema(tags=['Gestão de Check-ins']) 
class PatientCompanionCheckinViewSet(viewsets.ModelViewSet): 
    queryset = PatientCompanionCheckin.objects.all()
    serializer_class = PatientCompanionCheckinSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['patient__name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]