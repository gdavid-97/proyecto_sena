# Generated by Django 5.0.2 on 2024-03-12 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0007_alter_historial_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='comprar',
        ),
        migrations.AlterField(
            model_name='historial',
            name='fecha',
            field=models.DateField(),
        ),
        migrations.DeleteModel(
            name='usuario_historial',
        ),
    ]
