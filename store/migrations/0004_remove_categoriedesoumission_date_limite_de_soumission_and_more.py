# Generated by Django 5.0 on 2024-01-03 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_workshop_id_alter_workshop_conf_intitule_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoriedesoumission',
            name='date_limite_de_soumission',
        ),
        migrations.AddField(
            model_name='categoriedesoumission',
            name='date_limite_de_soumission_avant_conf',
            field=models.IntegerField(db_column='Date_limite_de_soumission_avant_conf', default=2),
            preserve_default=False,
        ),
    ]
