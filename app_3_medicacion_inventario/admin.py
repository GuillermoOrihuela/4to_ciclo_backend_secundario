from django.contrib import admin
from .models import AdministracionMedicacion, MedicacionPaciente, RecetasPaciente


@admin.register(RecetasPaciente)
class RecetasPacienteAdmin(admin.ModelAdmin):
	list_display = ('id_receta', 'id_paciente', 'medico_prescriptor', 'estado', 'fecha_prescripcion', 'fecha_vencimiento')
	list_filter = ('estado', 'fecha_prescripcion', 'fecha_vencimiento')
	search_fields = ('id_paciente__nombres', 'id_paciente__apellidos', 'medico_prescriptor', 'diagnostico_receta')


@admin.register(MedicacionPaciente)
class MedicacionPacienteAdmin(admin.ModelAdmin):
	list_display = ('id_medicacion', 'id_paciente', 'nombre_medicamento', 'tipo', 'cantidad_disponible', 'unidad_medida', 'fecha_vencimiento')
	list_filter = ('tipo', 'via_administracion', 'fecha_ingreso', 'fecha_vencimiento')
	search_fields = ('id_paciente__nombres', 'id_paciente__apellidos', 'nombre_medicamento', 'proveedor_o_familiar', 'lote')


@admin.register(AdministracionMedicacion)
class AdministracionMedicacionAdmin(admin.ModelAdmin):
	list_display = ('id_admin', 'id_medicacion', 'id_personal_entrega', 'fecha_hora_programada', 'fecha_hora_real', 'estado', 'cantidad_administrada')
	list_filter = ('estado', 'fecha_hora_programada')
	search_fields = ('id_medicacion__nombre_medicamento', 'motivo_rechazo')
