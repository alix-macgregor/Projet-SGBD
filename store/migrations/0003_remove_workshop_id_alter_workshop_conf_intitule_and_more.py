# Generated by Django 5.0 on 2023-12-13 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_conference_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshop',
            name='id',
        ),
        migrations.AlterField(
            model_name='workshop',
            name='conf_intitule',
            field=models.OneToOneField(db_column='Conf_intitule', on_delete=django.db.models.deletion.DO_NOTHING, to='store.conference'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='wk_intitule',
            field=models.OneToOneField(db_column='wk_intitule', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='store.soumission'),
        ),
    ]
