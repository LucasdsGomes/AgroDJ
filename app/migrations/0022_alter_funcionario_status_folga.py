# Generated by Django 4.2 on 2023-08-03 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_gerenciafolga_funcionario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='status_folga',
            field=models.CharField(default='0', max_length=100, verbose_name='Status de Folga'),
        ),
    ]
