# Generated by Django 4.2 on 2023-08-01 04:18

import cpf_field.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_funcionario_area_interesse_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='area_interesse',
            field=models.CharField(blank=True, choices=[('c', 'Contabilidade'), ('p', 'Plantio'), ('l', 'Colheita'), ('d', 'Distribuição'), ('i', 'Insumos')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='complemento',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='confirmpassword',
            field=models.CharField(max_length=50, null=True),
        ),
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
            name='endereco',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='funcao_exercida',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='logradouro',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='nome',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='password',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='salario',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]