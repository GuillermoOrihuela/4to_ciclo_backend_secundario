from rest_framework import serializers

from .models import AdministracionMedicacion, MedicacionPaciente, RecetasPaciente


class RecetasPacienteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = RecetasPaciente
        fields = '__all__'


class RecetasPacienteSerializerEnfermeroJefe(serializers.ModelSerializer):
    class Meta:
        model = RecetasPaciente
        fields = '__all__'


class RecetasPacienteSerializerTecnicoEnfermero(serializers.ModelSerializer):
    class Meta:
        model = RecetasPaciente
        fields = [
            'id_receta',
            'id_paciente',
            'medico_prescriptor',
            'fecha_prescripcion',
            'fecha_vencimiento',
            'diagnostico_receta',
            'estado',
        ]


class RecetasPacienteSerializerNutricionista(serializers.ModelSerializer):
    class Meta:
        model = RecetasPaciente
        fields = ['id_receta', 'id_paciente', 'diagnostico_receta', 'estado']
        read_only_fields = fields


class MedicacionPacienteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = MedicacionPaciente
        fields = '__all__'


class MedicacionPacienteSerializerEnfermeroJefe(serializers.ModelSerializer):
    class Meta:
        model = MedicacionPaciente
        fields = '__all__'


class MedicacionPacienteSerializerTecnicoEnfermero(serializers.ModelSerializer):
    class Meta:
        model = MedicacionPaciente
        fields = [
            'id_medicacion',
            'id_paciente',
            'id_receta',
            'nombre_medicamento',
            'tipo',
            'dosis',
            'frecuencia',
            'via_administracion',
            'horarios_aplicacion',
            'duracion_dias',
            'cantidad_disponible',
            'unidad_medida',
            'fecha_vencimiento',
        ]


class MedicacionPacienteSerializerNutricionista(serializers.ModelSerializer):
    class Meta:
        model = MedicacionPaciente
        fields = [
            'id_medicacion',
            'id_paciente',
            'nombre_medicamento',
            'dosis',
            'frecuencia',
            'via_administracion',
            'horarios_aplicacion',
        ]
        read_only_fields = fields


class AdministracionMedicacionSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = AdministracionMedicacion
        fields = '__all__'
        read_only_fields = ['id_personal_entrega']


class AdministracionMedicacionSerializerEnfermeroJefe(serializers.ModelSerializer):
    class Meta:
        model = AdministracionMedicacion
        fields = '__all__'
        read_only_fields = ['id_personal_entrega']


class AdministracionMedicacionSerializerTecnicoEnfermero(serializers.ModelSerializer):
    class Meta:
        model = AdministracionMedicacion
        fields = [
            'id_admin',
            'id_medicacion',
            'id_personal_entrega',
            'nombre_personal_entrega',
            'fecha_hora_programada',
            'fecha_hora_real',
            'cantidad_administrada',
            'estado',
            'motivo_rechazo',
        ]
        read_only_fields = ['id_personal_entrega']


class AdministracionMedicacionSerializerNutricionista(serializers.ModelSerializer):
    class Meta:
        model = AdministracionMedicacion
        fields = ['id_admin', 'id_medicacion', 'fecha_hora_programada', 'estado']
        read_only_fields = fields
