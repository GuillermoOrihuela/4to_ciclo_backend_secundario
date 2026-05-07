from django.db import models
from .config_identidad_relacion import (
    ESTADO_CIVIL_CHOICES, 
    ESTADO_PACIENTE_CHOICES, 
    SEXO_CHOICES,
    PARENTESCO_CHOICES,
    RESPONSABLE_CHOICES
)

class PacienteModel(models.Model):
    
    id_paciente = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=15, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    distrito = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to='pacientes/fotos/', blank=True, null=True)
    imagen_dni = models.ImageField(upload_to='pacientes/dni/', blank=True, null=True)
    estado_civil = models.CharField(max_length=15, choices=ESTADO_CIVIL_CHOICES, blank=True, null=True)
    estado_paciente = models.CharField(max_length=15, choices=ESTADO_PACIENTE_CHOICES, default='ACTIVO')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} - {self.dni}"

    class Meta:
        db_table = 'tb_paciente'
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-fecha_creacion']



class FamiliarModel(models.Model):
   
    id_familiar = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=15, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    movil = models.CharField(max_length=20, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    distrito = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    imagen_dni = models.ImageField(upload_to='familiares/dni/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} - {self.dni}"
    
    class Meta:
        db_table = 'tb_familiar'
        verbose_name = "Familiar"
        verbose_name_plural = "Familiares"
        ordering = ['-fecha_creacion']
    


class RelacionPacienteFamiliarModel(models.Model):

    id_relacion = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(
        'PacienteModel',
        on_delete=models.CASCADE,
        related_name='relaciones_familiares'
    )
    id_familiar = models.ForeignKey(
        'FamiliarModel',
        on_delete=models.CASCADE,
        related_name='relaciones_pacientes'
    )
    parentesco = models.CharField(max_length=20, choices=PARENTESCO_CHOICES)
    es_responsable_emergencia = models.CharField(max_length=2, choices=RESPONSABLE_CHOICES, default='NO')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_paciente.nombres} - {self.id_familiar.nombres} ({self.parentesco})"
    

    class Meta:
        db_table = 'tb_relacion_paciente_familiar'
        ordering = ['-fecha_creacion']



