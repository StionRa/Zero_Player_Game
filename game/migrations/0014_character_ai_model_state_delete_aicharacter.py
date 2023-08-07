# Generated by Django 4.2.2 on 2023-08-03 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_aicharacter'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='ai_model_state',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='AICharacter',
        ),
    ]
