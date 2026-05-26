from django.db import models


class RecetasPaciente(models.Model):
    ESTADO_CHOICES = [
        ('Activa', 'Activa'),
        ('Vencida', 'Vencida'),
        ('Suspendida', 'Suspendida'),
    ]

    id_receta = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(
        'app_1_identidad_relaciones.PacienteModel',
        on_delete=models.CASCADE,
        related_name='recetas_paciente',
    )
    medico_prescriptor = models.CharField(max_length=150)
    fecha_prescripcion = models.DateField()
    fecha_vencimiento = models.DateField()
    diagnostico_receta = models.TextField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Activa')

    class Meta:
        db_table = 'tb_recetas_paciente'
        verbose_name = 'Receta de Paciente'
        verbose_name_plural = 'Recetas de Pacientes'
        ordering = ['-fecha_prescripcion']

    def __str__(self):
        return f"Receta {self.id_receta} - Paciente {self.id_paciente_id}"


class MedicacionPaciente(models.Model):
    TIPO_CHOICES = [
    ('Pastilla', 'Pastilla'),
    ('Capsula', 'Cápsula'),
    ('Tableta', 'Tableta'),
    ('Comprimido', 'Comprimido'),
    ('Jarabe', 'Jarabe'),
    ('Suspension', 'Suspensión'),
    ('Solucion_Oral', 'Solución Oral'),
    ('Gotas_Orales', 'Gotas Orales'),
    ('Inyectable', 'Inyectable'),
    ('Ampolla', 'Ampolla'),
    ('Vial', 'Vial'),
    ('Suero', 'Suero'),
    ('Crema', 'Crema'),
    ('Pomada', 'Pomada'),
    ('Gel', 'Gel'),
    ('Parche', 'Parche'),
    ('Supositorio', 'Supositorio'),
    ('Ovulo', 'Óvulo'),
    ('Inhalador', 'Inhalador'),
    ('Nebulizacion', 'Nebulización'),
    ('Colirio', 'Colirio'),
    ('Gotas_Oticas', 'Gotas Óticas'),
    ('Spray_Nasal', 'Spray Nasal'),
    ('Polvo', 'Polvo'),
    ('Sobres', 'Sobres'),
    ]

    VIA_ADMINISTRACION_CHOICES = [
        ('Oral', 'Oral'),
        ('Topica', 'Topica'),
        ('IV', 'IV'),
    ]

    id_medicacion = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(
        'app_1_identidad_relaciones.PacienteModel',
        on_delete=models.CASCADE,
        related_name='medicaciones_paciente',
    )
    id_receta = models.ForeignKey(
        'RecetasPaciente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medicaciones',
    )
    nombre_medicamento = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    via_administracion = models.CharField(max_length=20, choices=VIA_ADMINISTRACION_CHOICES)
    horarios_aplicacion = models.CharField(max_length=200)
    duracion_dias = models.PositiveIntegerField()
    cantidad_disponible = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=50)
    proveedor_o_familiar = models.CharField(max_length=150)
    fecha_ingreso = models.DateField()
    fecha_vencimiento = models.DateField(blank=True, null=True)
    lote = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tb_medicacion_paciente'
        verbose_name = 'Medicacion de Paciente'
        verbose_name_plural = 'Medicaciones de Pacientes'
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return f"{self.nombre_medicamento} - Paciente {self.id_paciente_id}"


class AdministracionMedicacion(models.Model):
    ESTADO_CHOICES = [
        ('Entregado', 'Entregado'),
        ('Rechazado', 'Rechazado'),
        ('Omitido', 'Omitido'),
    ]

    id_admin = models.AutoField(primary_key=True)
    id_medicacion = models.ForeignKey(
        'MedicacionPaciente',
        on_delete=models.CASCADE,
        related_name='administraciones',
    )
    id_personal_entrega = models.CharField(max_length=128, blank=True, null=True)
    nombre_personal_entrega = models.CharField(max_length=200, blank=True, null=True)
    fecha_hora_programada = models.DateTimeField()
    fecha_hora_real = models.DateTimeField(blank=True, null=True)
    cantidad_administrada = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Entregado')
    motivo_rechazo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tb_administracion_medicacion'
        verbose_name = 'Administracion de Medicacion'
        verbose_name_plural = 'Administraciones de Medicacion'
        ordering = ['-fecha_hora_programada']

    def __str__(self):
        return f"Administracion {self.id_admin} - Estado {self.estado}"
