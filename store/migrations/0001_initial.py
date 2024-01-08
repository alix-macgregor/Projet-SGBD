# Generated by Django 5.0 on 2024-01-07 01:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('conf_intitule', models.CharField(db_column='Conf_intitule', max_length=100, primary_key=True, serialize=False)),
                ('date_de_debut', models.DateField(db_column='Date_de_debut')),
                ('date_de_fin', models.DateField(db_column='Date_de_fin')),
                ('loc_ville', models.CharField(db_column='Loc_Ville', max_length=15)),
                ('loc_pays', models.CharField(db_column='Loc_Pays', max_length=15)),
                ('serie', models.CharField(db_column='Serie', max_length=10)),
                ('text_introductif', models.TextField(db_column='Text_introductif')),
                ('editeur_actes', models.CharField(db_column='Editeur_actes', max_length=30)),
            ],
            options={
                'db_table': 'conference',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CategorieDeSoumission',
            fields=[
                ('categorie', models.CharField(db_column='Nom', max_length=20, primary_key=True, serialize=False)),
                ('nombre_de_pages_max', models.IntegerField(db_column='Nombre_de_pages_max')),
                ('mep_police', models.CharField(db_column='Mep_Police', max_length=10)),
                ('mep_taille_de_caracteres', models.IntegerField(db_column='Mep_Taille_de_caracteres')),
                ('mep_type_de_logiciel', models.CharField(db_column='Mep_Type_de_logiciel', max_length=10)),
                ('date_limite_de_soumission_en_jours_avant_la_conference', models.IntegerField(db_column='Date_limite_de_soumission')),
                ('delai_de_notification_apres_soummission', models.IntegerField(db_column='Delai_de_notification')),
                ('date_limite_de_correction_avant_conference', models.IntegerField(db_column='Date_limite_de_correction_avant_conference')),
            ],
            options={
                'db_table': 'categorie_de_soumission',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'evaluation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProgramCommitee',
            fields=[
                ('id_prog_commitee', models.AutoField(primary_key=True, serialize=False)),
                ('pc_nom', models.CharField(db_column='PC_nom', max_length=20)),
                ('pc_prenom', models.CharField(db_column='PC_prenom', max_length=30)),
                ('adresse_professionnelle', models.CharField(db_column='Adresse_Professionnelle', max_length=50)),
                ('mail', models.CharField(db_column='Mail', max_length=30)),
            ],
            options={
                'db_table': 'program_commitee',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Responsabilite',
            fields=[
                ('responsabilite', models.CharField(db_column='Responsabilite', max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'responsabilite',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Responsable',
            fields=[
                ('id_resp', models.AutoField(primary_key=True, serialize=False)),
                ('resp_nom', models.CharField(db_column='Resp_nom', max_length=20)),
                ('resp_prenom', models.CharField(db_column='Resp_prenom', max_length=30)),
                ('adresse_professionnelle', models.CharField(db_column='Adresse_Professionnelle', max_length=50)),
                ('mail', models.CharField(db_column='Mail', max_length=30)),
            ],
            options={
                'db_table': 'responsable',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ResponsableDe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'responsable_de',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('sess_intitule', models.CharField(db_column='Sess_intitule', max_length=100, primary_key=True, serialize=False)),
                ('themes', models.CharField(db_column='Themes', max_length=100)),
            ],
            options={
                'db_table': 'session',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Soumission',
            fields=[
                ('soumi_intitule', models.CharField(db_column='Soumi_intitule', max_length=100, primary_key=True, serialize=False)),
                ('date_de_soumission', models.DateField(db_column='Date_de_soumission')),
                ('etat', models.CharField(db_column='Etat', max_length=10)),
            ],
            options={
                'db_table': 'soumission',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id_util', models.AutoField(primary_key=True, serialize=False)),
                ('util_nom', models.CharField(db_column='Util_nom', max_length=20)),
                ('util_prenom', models.CharField(db_column='Util_prenom', max_length=20)),
                ('mail', models.CharField(db_column='Mail', max_length=30)),
                ('profil', models.TextField(db_column='Profil')),
            ],
            options={
                'db_table': 'utilisateur',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conf_intitule', models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.DO_NOTHING, to='store.conference')),
            ],
            options={
                'db_table': 'inscription',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Organisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orga_nom', models.CharField(db_column='Orga_nom', max_length=20)),
                ('adresse', models.CharField(db_column='Adresse', max_length=50)),
                ('mail', models.CharField(db_column='Mail', max_length=30)),
                ('conf_intitule', models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.DO_NOTHING, to='store.conference')),
            ],
            options={
                'db_table': 'organisateur',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Organise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conf_intitule', models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.DO_NOTHING, to='store.conference')),
            ],
            options={
                'db_table': 'organise',
                'managed': True,
            },
        ),
        migrations.AddConstraint(
            model_name='programcommitee',
            constraint=models.UniqueConstraint(fields=('pc_nom', 'pc_prenom'), name='pc_nom_prenom'),
        ),
        migrations.AddField(
            model_name='organise',
            name='prog_commitee',
            field=models.ForeignKey(db_column='prog_commitee', on_delete=django.db.models.deletion.DO_NOTHING, to='store.programcommitee'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='prog_commitee',
            field=models.ForeignKey(db_column='prog_commitee', on_delete=django.db.models.deletion.DO_NOTHING, to='store.programcommitee'),
        ),
        migrations.AddField(
            model_name='responsable',
            name='responsabilite',
            field=models.ForeignKey(db_column='Responsabilite', on_delete=django.db.models.deletion.DO_NOTHING, to='store.responsabilite'),
        ),
        migrations.AddField(
            model_name='responsablede',
            name='conf_intitule',
            field=models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.DO_NOTHING, to='store.conference'),
        ),
        migrations.AddField(
            model_name='responsablede',
            name='responsable',
            field=models.ForeignKey(db_column='responsable', on_delete=django.db.models.deletion.DO_NOTHING, to='store.responsable'),
        ),
        migrations.AddField(
            model_name='session',
            name='conf_intitule',
            field=models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.DO_NOTHING, to='store.conference'),
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('wk_intitule', models.OneToOneField(db_column='wk_intitule', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='store.soumission')),
                ('date_de_debut', models.DateField(db_column='Date_de_debut')),
                ('date_de_fin', models.DateField(db_column='Date_de_fin')),
                ('loc_ville', models.CharField(db_column='Loc_Ville', max_length=15)),
                ('loc_pays', models.CharField(db_column='Loc_Pays', max_length=15)),
                ('serie', models.CharField(db_column='Serie', max_length=10)),
                ('text_introductif', models.TextField(db_column='Text_introductif')),
                ('editeur_actes', models.CharField(db_column='Editeur_actes', max_length=30)),
            ],
            options={
                'db_table': 'workshop',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='soumission',
            name='categorie',
            field=models.ForeignKey(db_column='categorie', on_delete=django.db.models.deletion.DO_NOTHING, to='store.categoriedesoumission'),
        ),
        migrations.AddField(
            model_name='soumission',
            name='session_intitule',
            field=models.ForeignKey(db_column='session_intitule', on_delete=django.db.models.deletion.DO_NOTHING, to='store.session'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='soumi_intitule',
            field=models.ForeignKey(db_column='Soumi_intitule', on_delete=django.db.models.deletion.DO_NOTHING, to='store.soumission'),
        ),
        migrations.AddConstraint(
            model_name='utilisateur',
            constraint=models.UniqueConstraint(fields=('util_nom', 'util_prenom'), name='util_nom_prenom'),
        ),
        migrations.AddField(
            model_name='inscription',
            name='utilisateur',
            field=models.ForeignKey(db_column='utilisateur', on_delete=django.db.models.deletion.DO_NOTHING, to='store.utilisateur'),
        ),
        migrations.AddConstraint(
            model_name='organisateur',
            constraint=models.UniqueConstraint(fields=('orga_nom', 'conf_intitule'), name='orga_nom_conf_intitule'),
        ),
        migrations.AddConstraint(
            model_name='organise',
            constraint=models.UniqueConstraint(fields=('conf_intitule', 'prog_commitee'), name='conf_prog_commitee'),
        ),
        migrations.AddConstraint(
            model_name='responsable',
            constraint=models.UniqueConstraint(fields=('resp_nom', 'resp_prenom'), name='resp_nom_prenom'),
        ),
        migrations.AddConstraint(
            model_name='responsablede',
            constraint=models.UniqueConstraint(fields=('conf_intitule', 'responsable'), name='conf_responsable'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='conf_intitule',
            field=models.ForeignKey(db_column='Conf_intitule', on_delete=django.db.models.deletion.DO_NOTHING, to='store.conference'),
        ),
        migrations.AddConstraint(
            model_name='evaluation',
            constraint=models.UniqueConstraint(fields=('soumi_intitule', 'prog_commitee'), name='soumi_prog_commitee'),
        ),
        migrations.AddConstraint(
            model_name='inscription',
            constraint=models.UniqueConstraint(fields=('conf_intitule', 'utilisateur'), name='conf_utilisateur'),
        ),
    ]