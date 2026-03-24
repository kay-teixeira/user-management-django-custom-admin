from people.models import Person
from people.serializers import PersonSerializer
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        summary="Listar pessoas",
        description="Retorna a lista de todas as pessoas cadastradas no sistema (pacientes, acompanhantes, profissionais, etc). Permite realizar busca textual pelo nome."
    ),
    create=extend_schema(
        summary="Cadastrar pessoa",
        description="Adiciona um novo registro de pessoa no banco de dados da Casa de Apoio."
    ),
    retrieve=extend_schema(
        summary="Detalhar pessoa",
        description="Retorna os dados completos e específicos de uma pessoa através do seu ID."
    ),
    update=extend_schema(
        summary="Atualizar pessoa (Integral)",
        description="Substitui integralmente todos os dados do cadastro de uma pessoa."
    ),
    partial_update=extend_schema(
        summary="Atualizar pessoa (Parcial)",
        description="Atualiza campos específicos do cadastro de uma pessoa sem a necessidade de enviar o objeto inteiro."
    ),
    destroy=extend_schema(
        summary="Remover pessoa",
        description="Exclui o registro de uma pessoa do sistema."
    )
)

@extend_schema(tags=['Gestão de Pessoas'])


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [IsAuthenticated]
