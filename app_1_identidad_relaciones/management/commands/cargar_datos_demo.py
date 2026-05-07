from django.core.management.base import BaseCommand
from app_1_identidad_relaciones.models import PacienteModel, FamiliarModel
from datetime import date

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para Paciente y Familiar'

    def handle(self, *args, **kwargs):
        # Pacientes
        pacientes = [
            dict(dni='12345678', nombres='Juan', apellidos='Pérez', fecha_nacimiento=date(1980, 5, 10), sexo='M', direccion='Av. Siempre Viva 123', distrito='Lima', ciudad='Lima', estado_civil='CASADO', estado_paciente='ACTIVO'),
            dict(dni='87654321', nombres='Ana', apellidos='García', fecha_nacimiento=date(1990, 8, 22), sexo='F', direccion='Calle Falsa 456', distrito='Miraflores', ciudad='Lima', estado_civil='SOLTERA', estado_paciente='HOSPITALIZADO'),
        ]
        for p in pacientes:
            PacienteModel.objects.get_or_create(dni=p['dni'], defaults=p)

        # Familiares
        familiares = [
            dict(dni='11223344', nombres='Carlos', apellidos='Pérez', sexo='M', movil='987654321', direccion='Av. Siempre Viva 123', distrito='Lima', ciudad='Lima'),
            dict(dni='44332211', nombres='Lucía', apellidos='García', sexo='F', movil='912345678', direccion='Calle Falsa 456', distrito='Miraflores', ciudad='Lima'),
        ]
        for f in familiares:
            FamiliarModel.objects.get_or_create(dni=f['dni'], defaults=f)

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo creados para Paciente y Familiar'))
