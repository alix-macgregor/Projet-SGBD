# Generated by Django 5.0 on 2024-01-04 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_categoriedesoumission_date_limite_de_soumission_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoriedesoumission',
            name='date_limite_de_correction',
        ),
        migrations.RemoveField(
            model_name='categoriedesoumission',
            name='date_limite_de_soumission_avant_conf',
        ),
        migrations.AddField(
            model_name='categoriedesoumission',
            name='date_limite_de_correction_avant_conference',
            field=models.DateField(db_column='Date_limite_de_correction_avant_conference', default='04/01/2024'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categoriedesoumission',
            name='date_limite_de_soumission_en_jours_avant_la_conference',
            field=models.IntegerField(db_column='Date_limite_de_soumission', default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoriedesoumission',
            name='date_de_notification',
            field=models.IntegerField(db_column='Date_de_notification'),
        ),
    ]
