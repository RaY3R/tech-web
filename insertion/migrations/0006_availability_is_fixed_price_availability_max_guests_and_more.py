# Generated by Django 5.0.6 on 2024-07-18 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insertion', '0005_insertion__metadata_insertion_features_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='is_fixed_price',
            field=models.BooleanField(default=True, verbose_name='Prezzo fisso'),
        ),
        migrations.AddField(
            model_name='availability',
            name='max_guests',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='availability',
            name='price_per_night',
            field=models.FloatField(default=0, verbose_name='Prezzo a notte (fisso)'),
        ),
        migrations.AddField(
            model_name='availability',
            name='price_per_night_per_person',
            field=models.FloatField(blank=True, default=0, verbose_name='Prezzo a notte per persona (in caso di prezzo variabile)'),
        ),
        migrations.AlterField(
            model_name='availability',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Attivo'),
        ),
    ]
