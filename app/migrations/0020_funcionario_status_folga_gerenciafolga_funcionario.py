# Generated by Django 4.2 on 2023-08-03 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_gerenciafolga_data_inicio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='status_folga',
            field=models.IntegerField(default=0, verbose_name='Status de Folga'),
        ),
        migrations.AddField(
            model_name='gerenciafolga',
            name='funcionario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.funcionario'),
        ),
    ]
