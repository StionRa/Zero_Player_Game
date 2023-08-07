# Generated by Django 4.2.2 on 2023-08-02 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_delete_aicharacter'),
    ]

    operations = [
        migrations.CreateModel(
            name='AICharacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mood', models.CharField(default='neutral', max_length=100)),
                ('temperature', models.DecimalField(decimal_places=2, default=20.0, max_digits=5)),
                ('is_in_battle', models.BooleanField(default=False)),
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ai', to='game.character')),
            ],
        ),
    ]
