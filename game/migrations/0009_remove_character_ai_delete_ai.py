# Generated by Django 4.2.2 on 2023-06-30 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_alter_ai_current_x_alter_ai_current_y'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='ai',
        ),
        migrations.DeleteModel(
            name='AI',
        ),
    ]