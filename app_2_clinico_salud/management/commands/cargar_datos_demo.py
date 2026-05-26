from django.core.management.base import BaseCommand
from app_2_clinico_salud.models import HistoriaClinicaUnificada
from app_1_identidad_relaciones.models import PacienteModel
from django.utils import timezone

class Command(BaseCommand):
    help = 'Carga datos de ejemplo en HistoriaClinicaUnificada'

    def handle(self, *args, **kwargs):
        # Paciente de ejemplo
        paciente, _ = PacienteModel.objects.get_or_create(
            id_paciente='P001',
            defaults={
                'nombres': 'Juan',
                'apellidos': 'Pérez',
                'fecha_nacimiento': '1980-05-10',
                'genero': 'M',
                'documento_identidad': '12345678',
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
        evento = None
        try:
            from app_2_clinico_salud.models import EventosIncidentes
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
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creando evento: {e}'))
        self.stdout.write(self.style.SUCCESS(f'Historia creada: {historia.id_historia}'))
        if evento:
            self.stdout.write(self.style.SUCCESS(f'Evento creado: {evento.id_evento}'))
