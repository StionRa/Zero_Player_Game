# Generated by Django 4.2.2 on 2023-07-21 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_cat_dog_rewarditems_animal_reward_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animal',
            name='reward_items',
        ),
        migrations.DeleteModel(
            name='RewardItems',
        ),
    ]
