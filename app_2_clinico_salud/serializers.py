from rest_framework import serializers
from .models import HistoriaClinicaUnificada, EventosIncidentes

# Serializers para HistoriaClinicaUnificada

# Serializers para HistoriaClinicaUnificada actualizados
class HistoriaClinicaUnificadaSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinicaUnificada
        fields = [
            'id_historia', 'id_paciente', 'diagnostico_inicial',
            'alergias', 'tratamiento_actual', 'nutricion_asignada',
            'creado_por', 'actualizado_por', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['creado_por', 'actualizado_por', 'fecha_creacion', 'fecha_actualizacion']

class HistoriaClinicaUnificadaSerializerEnfermeroJefe(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinicaUnificada
        exclude = []
        read_only_fields = ['creado_por', 'actualizado_por', 'fecha_creacion', 'fecha_actualizacion']

class HistoriaClinicaUnificadaSerializerTecnicoEnfermero(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinicaUnificada
        exclude = ['nutricion_asignada']
        read_only_fields = ['creado_por', 'actualizado_por', 'fecha_creacion', 'fecha_actualizacion']

class HistoriaClinicaUnificadaSerializerNutricionista(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinicaUnificada
        exclude = ['diagnostico_inicial', 'tratamiento_actual']
        read_only_fields = ['creado_por', 'actualizado_por', 'fecha_creacion', 'fecha_actualizacion']

class HistoriaClinicaUnificadaSerializerCocineros(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinicaUnificada
        fields = ['id_historia', 'id_paciente', 'nutricion_asignada', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['creado_por', 'actualizado_por', 'fecha_creacion', 'fecha_actualizacion']

class HistoriaClinicaUnificadaSerializerMantenimiento(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinicaUnificada
        fields = ['id_historia', 'id_paciente', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['creado_por', 'actualizado_por', 'fecha_creacion', 'fecha_actualizacion']


# Serializers para EventosIncidentes
class EventosIncidentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventosIncidentes
        fields = '__all__'
        read_only_fields = ['creado_por', 'actualizado_por']
