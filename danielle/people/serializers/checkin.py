from people.models import Checkin
from rest_framework import serializers
from people.models import PatientCompanionCheckin

class CheckinSerializer(serializers.ModelSerializer):
    companion_name = serializers.CharField(read_only=True)
    person_name = serializers.CharField(read_only=True)
    formatted_created_at = serializers.CharField(read_only=True)

    def validate(self, data):
        #Validação original (Acompanhante)
        if data.get('reason') == 'patient':
            if 'companion' not in data.keys():
                raise serializers.ValidationError({'companion': 'Todo paciente deve ter acompanhante.'})
            else:
                if not data['companion']:
                    raise serializers.ValidationError({'companion': 'Campo acompanhante não pode ser nulo.'})

        #Trava de Múltiplos Check-ins Ativos
        person = data.get('person', self.instance.person if self.instance else None)
        is_active = data.get('active', self.instance.active if self.instance else True)

        if person and is_active:
            query = Checkin.objects.filter(person=person, active=True)
            if self.instance:
                query = query.exclude(pk=self.instance.pk)

            if query.exists():
                raise serializers.ValidationError(
                    {'person': 'Esta pessoa já possui um check-in ativo. Faça o check-out antes de registrar uma nova entrada.'}
                )

        return data

    class Meta:
        model = Checkin
        exclude = ['updated_at', 'created_at']
        #Campos de Soft Delete
        read_only_fields = ('companion_name', 'person_name', 'formatted_created_at', 'is_deleted', 'deleted_at')

class PatientCompanionCheckinSerializer(serializers.ModelSerializer):
    companion_name = serializers.CharField(required=False, allow_blank=True)
    patient_name = serializers.CharField(required=False, allow_blank=True)
    formatted_created_at = serializers.CharField(required=False,
                                                 allow_blank=True)
