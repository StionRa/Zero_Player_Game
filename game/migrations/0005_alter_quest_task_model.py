# Generated by Django 4.2.2 on 2023-07-21 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_animalinventory_animalinventoryitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='task_model',
            field=models.CharField(choices=[('kill_animal', 'kill_animal'), ('find', 'find')], max_length=100),
        ),
    ]
