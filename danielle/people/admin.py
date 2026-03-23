from django.contrib import admin
from people.models import Checkin
from people.models import Person
from people.models import Checkout
from people.models import HomeServices
from people.models import ProfessionalServices
import csv
from django.http import HttpResponse

admin.site.site_header = "Gestão de pessoas"
admin.site.site_title = "Gestão fácil!"
admin.site.index_title = "Bem vindo! "

@admin.action(description='Exportar selecionados para CSV (Relatório)')
def export_to_csv(modeladmin, request, queryset):
    
    #Pega as colunas da tabela
    meta = modeladmin.model._meta
    header_names = [field.verbose_name.title() for field in meta.fields]

    #Prepara o arquivo de resposta que o navegador vai fazer o download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}-relatorio.csv'
    response.write(b'\xef\xbb\xbf')

    #Cria o escritor do CSV
    writer = csv.writer(response, delimiter=';') 

    #Escreve o cabeçalho 
    writer.writerow(header_names)

    #Escreve os dados de cada linha que o usuário selecionou
    for obj in queryset:
        row = [str(getattr(obj, field.name)) for field in meta.fields]
        writer.writerow(row)

    return response

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'born_date')
    list_filter = ['gender', 'state']
    search_fields = ['name', 'cpf']
    search_help_text = 'Pesquise pelo Nome ou CPF.'
    exclude = ['is_deleted', 'deleted_at']
    actions = [export_to_csv]
    fieldsets = [('Identificação', {
        'fields': [
            'name', 'mother_name', 'born_date', 'cpf', ('rg', 'rg_ssp'),
            'gender'
        ]
    }),
                 ('Endereço', {
                     'fields': [
                         'address_line_1', 'address_line_2', 'neighbourhood',
                         'state', 'city', 'postal_code', 'residence_type'
                     ]
                 }),
                 ('Contato', {
                     'fields': [
                         'email', ('ddd_private_phone', 'private_phone'),
                         ('ddd_message_phone', 'message_phone')
                     ]
                 }),
                 ('Outras informações', {
                     'fields': ['observation', 'death_date'],
                     'classes': ('collapse', ),
                 })]


class CheckinAdmin(admin.ModelAdmin):
    list_display = ('person', 'reason', 'created_at')
    list_filter = ['reason']
    search_fields = ['person__name', 'person__cpf']
    search_help_text = 'Pesquise pelo Nome ou CPF.'
    exclude = ['is_deleted', 'deleted_at']
    actions = [export_to_csv]
    fieldsets = [('Identificação', {
        'fields': ['person', 'reason']
    }),
                 ('Preencher se paciente:', {
                     'fields': [
                         'companion',
                         ('chemotherapy', 'radiotherapy', 'surgery',
                          'appointment', 'exams', 'other'), 'ca_number',
                         'social_vacancy'
                     ]
                 }),
                 ('Outras informações', {
                     'fields': ['observation', 'active'],
                     'classes': ('collapse', ),
                 })]


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('checkin', 'created_at')
    search_fields = ['checkin__person__name', 'checkin__person__cpf']
    search_help_text = 'Pesquise pelo Nome ou CPF.'
    exclude = ['is_deleted', 'deleted_at']
    actions = [export_to_csv]

class HomeServicesAdmin(admin.ModelAdmin):
    list_display = ('person', 'breakfast', 'lunch', 'snack', 'dinner',
                    'shower', 'sleep', 'created_at')
    search_fields = ['person__name', 'person__cpf']
    search_help_text = 'Pesquise pelo Nome ou CPF.'
    exclude = ['is_deleted', 'deleted_at']
    actions = [export_to_csv]

class ProfessionalServicesAdmin(admin.ModelAdmin):
    list_display = ('professional', 'title', 'description', 'created_at')
    search_fields = ['professional__name', 'professional__cpf']
    search_help_text = 'Pesquise pelo Nome ou CPF do profissional.'
    exclude = ['is_deleted', 'deleted_at']
    actions = [export_to_csv]


admin.site.register(Person, PersonAdmin)
admin.site.register(Checkin, CheckinAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(HomeServices, HomeServicesAdmin)
admin.site.register(ProfessionalServices, ProfessionalServicesAdmin)
