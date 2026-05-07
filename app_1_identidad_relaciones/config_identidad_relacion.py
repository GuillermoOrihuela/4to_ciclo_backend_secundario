# Configuración de opciones para el módulo de identidad y relaciones

# Roles de usuario
ROLES_CHOICES = [
    ('administrador', 'Administrador'),
    ('enfermero jefe', 'Enfermero jefe'),
    ('tecnico enfermero', 'Tecnico enfermero'),
    ('nutricionista', 'Nutricionista'),
    ('cocineros', 'Cocineros'),
    ('mantenimiento', 'Mantenimiento'),
    ]


# Estados del paciente
ESTADO_PACIENTE_CHOICES = [
    ('REGISTRADO', 'Registrado'),
    ('ACTIVO', 'Activo'),
    ('HOSPITALIZADO', 'Hospitalizado'),
    ('EN_TRATAMIENTO', 'En tratamiento'),
    ('ALTA_MEDICA', 'Alta médica'),
    ('REFERIDO', 'Referido'),
    ('FALLECIDO', 'Fallecido'),
    ('INACTIVO', 'Inactivo'),
]

# Sexo
SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
]

# Estado civil
ESTADO_CIVIL_CHOICES = [
    ('SOLTERO', 'Soltero'),
    ('SOLTERA', 'Soltera'),
    ('CASADO', 'Casado'),
    ('CASADA', 'Casada'),
    ('DIVORCIADO', 'Divorciado'),
    ('DIVORCIADA', 'Divorciada'),
    ('VIUDO', 'Viudo'),
    ('VIUDA', 'Viuda'),
]

PARENTESCO_CHOICES = [
    ('PADRE', 'Padre'),
    ('MADRE', 'Madre'),
    ('HIJO', 'Hijo'),
    ('HIJA', 'Hija'),
    ('CONYUGE', 'Cónyuge'),
    ('HERMANO', 'Hermano'),
    ('HERMANA', 'Hermana'),
    ('ABUELO', 'Abuelo'),
    ('ABUELA', 'Abuela'),
    ('NIETO', 'Nieto'),
    ('NIETA', 'Nieta'),
    ('TIO', 'Tío'),
    ('TIA', 'Tía'),
    ('SOBRINO', 'Sobrino'),
    ('SOBRINA', 'Sobrina'),
    ('PRIMO', 'Primo'),
    ('PRIMA', 'Prima'),
    ('OTRO', 'Otro'),

    ]

RESPONSABLE_CHOICES = [
        ('SI', 'Sí'),
        ('NO', 'No'),
    ]