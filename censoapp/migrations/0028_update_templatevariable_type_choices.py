# Generated manually on 2025-12-19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('censoapp', '0027_templatevariable_variable_type_and_more'),
    ]

    operations = [
        # Actualizar las opciones del campo variable_type
        migrations.AlterField(
            model_name='templatevariable',
            name='variable_type',
            field=models.CharField(
                choices=[
                    ('person', 'Dato de Persona'),
                    ('family_card', 'Dato de Ficha Familiar'),
                    ('association', 'Dato de Asociación'),
                    ('organization', 'Dato de Organización'),
                ],
                default='person',
                help_text='Tipo de dato (Persona, Ficha Familiar, Asociación, Organización)',
                max_length=20,
                verbose_name='Tipo de Variable'
            ),
        ),
        # Actualizar descripción del campo variable_value
        migrations.AlterField(
            model_name='templatevariable',
            name='variable_value',
            field=models.CharField(
                help_text="Nombre del campo del modelo (ej: 'organization_territory', 'full_name')",
                max_length=200,
                verbose_name='Campo del Modelo'
            ),
        ),
        # Actualizar descripción del campo variable_name
        migrations.AlterField(
            model_name='templatevariable',
            name='variable_name',
            field=models.CharField(
                help_text="Nombre único sin llaves (ej: 'territorio', 'nombre_completo')",
                max_length=100,
                verbose_name='Nombre de la Variable'
            ),
        ),
        # Agregar ordering
        migrations.AlterModelOptions(
            name='templatevariable',
            options={
                'ordering': ['organization', 'variable_type', 'variable_name'],
                'verbose_name': 'Variable Personalizada',
                'verbose_name_plural': 'Variables Personalizadas'
            },
        ),
    ]

