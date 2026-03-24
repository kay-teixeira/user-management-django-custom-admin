from django.shortcuts import render
from people.models import Person, Checkin

def gerencial_dashboard(request):
    """
    View responsável por calcular as métricas e filtrar a tabela do dashboard.
    """
    total_pessoas = Person.objects.count()
    checkins_ativos = Checkin.objects.filter(active=True).count()
    
    #Histórico de Atendimentos
    total_pacientes = Checkin.objects.filter(reason='patient').count()
    total_acompanhantes = Checkin.objects.filter(reason='companion').count()
    total_profissionais = Checkin.objects.filter(reason='professional').count()
    
    #Filtros da tabela
    checkins = Checkin.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    tipo_query = request.GET.get('tipo', 'todos')

    if search_query:
        checkins = checkins.filter(person__name__icontains=search_query)

    if tipo_query and tipo_query != 'todos':
        checkins = checkins.filter(reason=tipo_query)

    # Limita para não quebrar a tela se tiverem 1000 registros
    ultimos_checkins = checkins[:10]

    context = {
        'total_pessoas': total_pessoas,
        'checkins_ativos': checkins_ativos,
        'total_pacientes': total_pacientes,
        'total_acompanhantes': total_acompanhantes,
        'total_profissionais': total_profissionais,
        'ultimos_checkins': ultimos_checkins,
        'search_query': search_query,
        'tipo_query': tipo_query,
    }
    
    return render(request, 'dashboard.html', context)