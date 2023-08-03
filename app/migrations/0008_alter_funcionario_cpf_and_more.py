# Generated by Django 4.2 on 2023-07-31 17:33

import cpf_field.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_funcionario_salario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='cpf',
            field=cpf_field.models.CPFField(max_length=14),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='data_nascimento',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='salario',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
