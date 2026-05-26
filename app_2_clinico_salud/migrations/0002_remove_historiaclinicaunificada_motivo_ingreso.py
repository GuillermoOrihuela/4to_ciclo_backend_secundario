from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_2_clinico_salud', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historiaclinicaunificada',
            name='motivo_ingreso',
        ),
    ]