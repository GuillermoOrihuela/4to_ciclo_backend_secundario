
from rest_framework import serializers
from .models import PacienteModel, FamiliarModel
# *****************SERIALIZADORES PARA RELACION PACIENTE-FAMILIAR***********************
from .models import RelacionPacienteFamiliarModel

# Admin: ve todo
class RelacionPacienteFamiliarSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = RelacionPacienteFamiliarModel
        fields = '__all__'

# Enfermero jefe: ve todo menos fechas
class RelacionPacienteFamiliarSerializerEnfermeroJefe(serializers.ModelSerializer):
    class Meta:
        model = RelacionPacienteFamiliarModel
        exclude = ['fecha_creacion', 'fecha_modificacion']

# Técnico enfermero: solo ve paciente, familiar y parentesco
class RelacionPacienteFamiliarSerializerTecnicoEnfermero(serializers.ModelSerializer):
    class Meta:
        model = RelacionPacienteFamiliarModel
        fields = ['id_relacion', 'id_paciente', 'id_familiar', 'parentesco']

# Nutricionista: solo ve paciente y familiar
class RelacionPacienteFamiliarSerializerNutricionista(serializers.ModelSerializer):
    class Meta:
        model = RelacionPacienteFamiliarModel
        fields = ['id_relacion', 'id_paciente', 'id_familiar']

# *****************FIN SERIALIZADORES PARA RELACION PACIENTE-FAMILIAR***********************



# *****************SERIALIZADORES PARA PACIENTE***********************

# Administrador: ve todos los campos
class PacienteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = PacienteModel
        fields = '__all__'

# Enfermero jefe: ve casi todo, excepto imágenes
class PacienteSerializerEnfermeroJefe(serializers.ModelSerializer):
    class Meta:
        model = PacienteModel
        exclude = ['imagen_dni']
        read_only_fields = [
            'dni', 'fecha_nacimiento', 'foto', 'fecha_creacion', 'fecha_modificacion'
        ]

# Técnico enfermero: acceso limitado
class PacienteSerializerTecnicoEnfermero(serializers.ModelSerializer):
    class Meta:
        model = PacienteModel
        fields = [
            'id_paciente', 'nombres',
            'apellidos', 'fecha_nacimiento',
            'sexo', 'estado_paciente',
            'direccion', 'distrito'
            ]
        

        read_only_fields = [
            'dni', 'nombres', 'apellidos',
            'fecha_nacimiento', 'sexo',
            'fecha_creacion', 'fecha_modificacion'
        ]

# Nutricionista: solo datos relevantes para dieta
class PacienteSerializerNutricionista(serializers.ModelSerializer):
    class Meta:
        model = PacienteModel
        fields = ['id_paciente', 'nombres', 'apellidos', 'estado_paciente']
        read_only_fields = fields  # todos son solo lectura

# *****************FIN SERIALIZADORES PARA PACIENTE FIN***********************


# *****************SERIALIZADORES PARA FAMILIAR***********************

# Administrador: acceso total
class FamiliarSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = FamiliarModel
        fields = '__all__'
        
        


# Enfermero jefe: ve todo menos imagen_dni, pero no modifica identidad ni fechas
class FamiliarSerializerEnfermeroJefe(serializers.ModelSerializer):
    class Meta:
        model = FamiliarModel
        exclude = ['imagen_dni']
        read_only_fields = [
            'dni', 'nombres', 'apellidos',
            'fecha_creacion', 'fecha_modificacion'
        ]


# Técnico enfermero: acceso limitado
class FamiliarSerializerTecnicoEnfermero(serializers.ModelSerializer):
    class Meta:
        model = FamiliarModel
        fields = [
            'id_familiar', 'nombres', 'apellidos',
            'sexo', 'direccion', 'distrito', 'ciudad'
        ]
        read_only_fields = [
            'dni', 'nombres', 'apellidos',
            'fecha_creacion', 'fecha_modificacion'
        ]


# Nutricionista: acceso a datos básicos y estado civil (si lo tuvieran)
class FamiliarSerializerNutricionista(serializers.ModelSerializer):
    class Meta:
        model = FamiliarModel
        fields = [
            'id_familiar', 'nombres', 'apellidos',
            'sexo', 'direccion', 'distrito', 'ciudad'
        ]
        read_only_fields = [
            'dni', 'nombres', 'apellidos',
            'fecha_creacion', 'fecha_modificacion'
        ]

# *****************FIN SERIALIZADORES PARA FAMILIAR FIN***********************