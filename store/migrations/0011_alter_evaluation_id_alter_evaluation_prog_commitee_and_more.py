# Generated by Django 5.0.1 on 2024-01-09 09:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_rename_délai_de_notification_blabla'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='prog_commitee',
            field=models.ForeignKey(db_column='prog_commitee', on_delete=django.db.models.deletion.CASCADE, to='store.programcommitee'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='soumi_intitule',
            field=models.ForeignKey(db_column='Soumi_intitule', on_delete=django.db.models.deletion.CASCADE, to='store.soumission'),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='conf_intitule',
            field=models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.CASCADE, to='store.conference'),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='utilisateur',
            field=models.ForeignKey(db_column='utilisateur', on_delete=django.db.models.deletion.CASCADE, to='store.utilisateur'),
        ),
        migrations.AlterField(
            model_name='organisateur',
            name='conf_intitule',
            field=models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.CASCADE, to='store.conference'),
        ),
        migrations.AlterField(
            model_name='organisateur',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='organise',
            name='conf_intitule',
            field=models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.CASCADE, to='store.conference'),
        ),
        migrations.AlterField(
            model_name='organise',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='organise',
            name='prog_commitee',
            field=models.ForeignKey(db_column='prog_commitee', on_delete=django.db.models.deletion.CASCADE, to='store.programcommitee'),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='responsabilite',
            field=models.ForeignKey(db_column='Responsabilite', on_delete=django.db.models.deletion.CASCADE, to='store.responsabilite'),
        ),
        migrations.AlterField(
            model_name='responsablede',
            name='conf_intitule',
            field=models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.CASCADE, to='store.conference'),
        ),
        migrations.AlterField(
            model_name='responsablede',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='responsablede',
            name='responsable',
            field=models.ForeignKey(db_column='responsable', on_delete=django.db.models.deletion.CASCADE, to='store.responsable'),
        ),
        migrations.AlterField(
            model_name='session',
            name='conf_intitule',
            field=models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.CASCADE, to='store.conference'),
        ),
        migrations.AlterField(
            model_name='soumission',
            name='categorie',
            field=models.ForeignKey(db_column='categorie', on_delete=django.db.models.deletion.CASCADE, to='store.categoriedesoumission'),
        ),
        migrations.AlterField(
            model_name='soumission',
            name='session_intitule',
            field=models.ForeignKey(db_column='session_intitule', on_delete=django.db.models.deletion.CASCADE, to='store.session'),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='profil',
            field=models.TextField(db_column='Profil', default=''),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='conf_intitule',
            field=models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.CASCADE, to='store.conference'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='wk_intitule',
            field=models.OneToOneField(db_column='wk_intitule', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='store.soumission'),
        ),
    ]
