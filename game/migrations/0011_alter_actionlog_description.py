# Generated by Django 4.2.2 on 2023-07-01 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_actionlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionlog',
            name='description',
            field=models.TextField(default=0),
        ),
    ]
