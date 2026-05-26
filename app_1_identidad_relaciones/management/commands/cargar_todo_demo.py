from django.core.management.base import BaseCommand
from app_1_identidad_relaciones.models import PacienteModel, FamiliarModel, RelacionPacienteFamiliarModel
from app_2_clinico_salud.models import HistoriaClinicaUnificada, EventosIncidentes
from django.utils import timezone

class Command(BaseCommand):
    help = 'Carga datos de ejemplo en todas las tablas del sistema'

    def handle(self, *args, **kwargs):
        # Paciente de ejemplo
        paciente, _ = PacienteModel.objects.get_or_create(
            dni='12345678',
            defaults={
                'nombres': 'Juan',
                'apellidos': 'Pérez',
                'fecha_nacimiento': '1980-05-10',
                'sexo': 'M',
            }
        )
        # Familiar de ejemplo
        familiar, _ = FamiliarModel.objects.get_or_create(
            dni='87654321',
            defaults={
                'nombres': 'Ana',
                'apellidos': 'García',
                'sexo': 'F',
            }
        )
        # Relación paciente-familiar
        relacion, _ = RelacionPacienteFamiliarModel.objects.get_or_create(
            id_paciente=paciente,
            id_familiar=familiar,
            defaults={
                'parentesco': 'Madre',
                'es_responsable_emergencia': 'SI',
            }
        )
        # Historia clínica
        historia = HistoriaClinicaUnificada.objects.create(
            id_paciente=paciente,
            diagnostico_inicial='Apendicitis aguda',
            alergias='Ninguna',
            tratamiento_actual='Observación y analgésicos',
            nutricion_asignada='Dieta blanda',
            creado_por='admin',
            actualizado_por='admin',
            fecha_creacion=timezone.now(),
            fecha_actualizacion=timezone.now(),
        )
        # Evento incidente
        evento = EventosIncidentes.objects.create(
            id_paciente=paciente,
            tipo_evento='Caída',
            descripcion='Paciente sufrió caída en baño',
            acciones_tomadas='Se realizó curación y monitoreo',
            gravedad='Media',
            fecha_evento='2026-04-26',
            hora_evento='10:30',
            creado_por='enfermero1',
            actualizado_por='enfermero1',
        )
        self.stdout.write(self.style.SUCCESS(f'Paciente creado: {paciente.nombres}'))
        self.stdout.write(self.style.SUCCESS(f'Familiar creado: {familiar.nombres}'))
        self.stdout.write(self.style.SUCCESS(f'Relación creada: {relacion.parentesco}'))
        self.stdout.write(self.style.SUCCESS(f'Historia creada: {historia.id_historia}'))
        self.stdout.write(self.style.SUCCESS(f'Evento creado: {evento.id_evento}'))
