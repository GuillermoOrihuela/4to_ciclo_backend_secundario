from django.db import models

class HistoriaClinicaUnificada(models.Model):
    id_historia = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey('app_1_identidad_relaciones.PacienteModel', on_delete=models.CASCADE)

    motivo_ingreso = models.TextField(blank=True)
    diagnostico_inicial = models.TextField(blank=True)
    alergias = models.TextField(blank=True)
    tratamiento_actual = models.TextField(blank=True)
    nutricion_asignada = models.TextField(blank=True)
    creado_por = models.CharField(max_length=128, blank=True, default='')
    actualizado_por = models.CharField(max_length=128, blank=True, default='')
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True,  blank=True, null=True)

    class Meta:
        db_table = 'tb_historia_clinica_unificada'


class EventosIncidentes(models.Model):
    id_evento = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey('app_1_identidad_relaciones.PacienteModel', on_delete=models.CASCADE)
    creado_por = models.CharField(max_length=128, blank=True, default='')
    actualizado_por = models.CharField(max_length=128, blank=True, default='')
    tipo_evento = models.CharField(max_length=50, choices=[('Caída','Caída'),('Emergencia Médica','Emergencia Médica'),('Conflicto','Conflicto'),('Otro','Otro')])
    descripcion = models.TextField()
    acciones_tomadas = models.TextField(blank=True)
    gravedad = models.CharField(max_length=10, choices=[('Baja','Baja'),('Media','Media'),('Alta','Alta')])
    fecha_evento = models.DateField()
    hora_evento = models.TimeField()

    class Meta:
        db_table = 'tb_eventos_incidentes'
        ordering = ['-fecha_evento', '-hora_evento']
