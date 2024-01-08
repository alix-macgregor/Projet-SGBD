from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING

# Create your models here.


class Utilisateur(models.Model):
    id_util = models.AutoField(primary_key=True)
    util_nom = models.CharField(db_column="Util_nom", max_length=20)
    util_prenom = models.CharField(db_column="Util_prenom", max_length=20)  # Field name made lowercase.
    mail = models.CharField(db_column="Mail", max_length=30)  # Field name made lowercase.
    profil = models.TextField(db_column="Profil", default='')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "utilisateur"
        constraints = [
            models.UniqueConstraint(fields=["util_nom", "util_prenom"], name="util_nom_prenom")
        ]

    def __str__(self) :
        return self.util_nom + ' ' + self.util_prenom


class CategorieDeSoumission(models.Model):
    categorie = models.CharField(db_column='Nom', primary_key=True, max_length=20)  # Field name made lowercase.
    nombre_de_pages_max = models.IntegerField(db_column='Nombre_de_pages_max')  # Field name made lowercase.
    mep_police = models.CharField(db_column='Mep_Police', max_length=10)  # Field name made lowercase.
    mep_taille_de_caracteres = models.IntegerField(db_column='Mep_Taille_de_caracteres')  # Field name made lowercase.
    mep_type_de_logiciel = models.CharField(db_column='Mep_Type_de_logiciel', max_length=10)  # Field name made lowercase.
    date_limite_de_soumission_en_jours_avant_la_conference= models.IntegerField(db_column='Date_limite_de_soumission')  # Field name made lowercase.
    delai_de_notification_apres_soummission= models.IntegerField(db_column='Delai_de_notification')  # Field name made lowercase.
    date_limite_de_correction_avant_conference = models.IntegerField(db_column='Date_limite_de_correction_avant_conference')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "categorie_de_soumission"

    def __str__(self) :
        return self.categorie

class Conference(models.Model):
    conf_intitule = models.CharField(db_column="Conf_intitule", primary_key=True, max_length=100)  # Field name made lowercase.
    date_de_debut = models.DateField(db_column="Date_de_debut")  # Field name made lowercase.
    date_de_fin = models.DateField(db_column="Date_de_fin")  # Field name made lowercase.
    loc_ville = models.CharField(db_column="Loc_Ville", max_length=15)  # Field name made lowercase.
    loc_pays = models.CharField(db_column="Loc_Pays", max_length=15)  # Field name made lowercase.
    serie = models.CharField(db_column="Serie", max_length=10)  # Field name made lowercase.
    text_introductif = models.TextField(db_column="Text_introductif")  # Field name made lowercase.
    editeur_actes = models.CharField(db_column="Editeur_actes", max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'conference'

    def __str__(self) :
        return self.conf_intitule


class Evaluation(models.Model):
    soumi_intitule = models.ForeignKey("Soumission", models.DO_NOTHING, db_column="Soumi_intitule")
    # Champs déjà présents dans la table 'Progam_Commitee'
    # pc_nom = models.ForeignKey('ProgramCommitee', models.DO_NOTHING, db_column='PC_nom')  # Field name made lowercase.
    # pc_prenom = models.ForeignKey('ProgramCommitee', models.DO_NOTHING, db_column='PC_prenom', to_field='pc_prenom', related_name='evaluation_pc_prenom_set')  # Field name made lowercase.
    prog_commitee = models.ForeignKey("ProgramCommitee", models.DO_NOTHING, db_column="prog_commitee")

    class Meta:
        managed = True
        db_table = "evaluation"
        constraints = [
            models.UniqueConstraint(fields=["soumi_intitule", "prog_commitee"], name="soumi_prog_commitee")
        ]

    def __str__(self) :
        return str(self.soumi_intitule) + " -- " + str(self.prog_commitee)

class Inscription(models.Model):
    conf_intitule = models.ForeignKey(Conference, models.DO_NOTHING, db_column="Conf_intitule")
    # Pas besoin de ces champs car ils sont déjà dans 'Utilisateur'
    # util_nom = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='Util_nom')  # Field name made lowercase.
    # util_prenom = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='Util_prenom', to_field='util_prenom', related_name='inscription_util_prenom_set')  # Field name made lowercase.
    utilisateur = models.ForeignKey(Utilisateur, models.DO_NOTHING, db_column="utilisateur")

    class Meta:
        managed = True
        db_table = "inscription"
        # unique_together = (('conf_intitule', 'util_nom', 'util_prenom'), ('conf_intitule', 'util_nom', 'util_prenom'),)
        constraints = [
            models.UniqueConstraint(fields=["conf_intitule", "utilisateur"], name="conf_utilisateur")
        ]

    def __str__(self) :
        return str(self.conf_intitule) + ' -- '+ str(self.utilisateur)

class Organisateur(models.Model):
    orga_nom = models.CharField(db_column='Orga_nom', max_length=20)  # Field name made lowercase.
    conf_intitule = models.ForeignKey(Conference, models.DO_NOTHING, db_column='Conf_intitule')  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=50)  # Field name made lowercase.
    mail = models.CharField(db_column='Mail', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'organisateur'
        constraints = [
            models.UniqueConstraint(fields=['orga_nom','conf_intitule'], name= 'orga_nom_conf_intitule')
        ]

    def __str__(self) :
        return self.orga_nom

class Organise(models.Model):
    conf_intitule = models.ForeignKey(Conference, models.DO_NOTHING, db_column="Conf_intitule")
    # Ces champs figures déjà dans la table 'Programm_Comitee'
    # pc_nom = models.ForeignKey('ProgramCommitee', models.DO_NOTHING, db_column='PC_nom')  # Field name made lowercase.
    # pc_prenom = models.ForeignKey('ProgramCommitee', models.DO_NOTHING, db_column='PC_prenom', to_field='pc_prenom', related_name='organise_pc_prenom_set')  # Field name made lowercase.
    prog_commitee = models.ForeignKey("ProgramCommitee", models.DO_NOTHING, db_column="prog_commitee")

    class Meta:
        managed = True
        db_table = "organise"
        # unique_together = (('conf_intitule', 'pc_nom', 'pc_prenom'), ('conf_intitule', 'pc_nom', 'pc_prenom'),)
        constraints = [
            models.UniqueConstraint(fields=["conf_intitule", "prog_commitee"], name="conf_prog_commitee")
        ]

    def __str__(self) :
        return str(self.conf_intitule) + ' --- ' + str(self.prog_commitee)
class ProgramCommitee(models.Model):
    id_prog_commitee = models.AutoField(primary_key=True)
    pc_nom = models.CharField(db_column="PC_nom", max_length=20)
    pc_prenom = models.CharField(db_column="PC_prenom", max_length=30)  # Field name made lowercase.
    adresse_professionnelle = models.CharField(db_column="Adresse_Professionnelle", max_length=50)  # Field name made lowercase.
    mail = models.CharField(db_column="Mail", max_length=30)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "program_commitee"
        # unique_together = (('pc_nom', 'pc_prenom'), ('pc_nom', 'pc_prenom'),)
        constraints = [
            models.UniqueConstraint(fields=["pc_nom", "pc_prenom"], name="pc_nom_prenom")
        ]
    def __str__(self) :
        return self.pc_nom + ' ' + self.pc_prenom

class Responsabilite(models.Model):
    responsabilite = models.CharField(db_column="Responsabilite", primary_key=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "responsabilite"

    def __str__(self) :
        return self.responsabilite

class Responsable(models.Model):
    id_resp = models.AutoField(primary_key=True)
    resp_nom = models.CharField(db_column="Resp_nom", max_length=20)
    resp_prenom = models.CharField(db_column="Resp_prenom", max_length=30)  # Field name made lowercase.
    adresse_professionnelle = models.CharField(db_column="Adresse_Professionnelle", max_length=50)  # Field name made lowercase.
    mail = models.CharField(db_column="Mail", max_length=30)  # Field name made lowercase.
    responsabilite = models.ForeignKey(Responsabilite, models.DO_NOTHING, db_column="Responsabilite")  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "responsable"
        # unique_together = (('resp_nom', 'resp_prenom'), ('resp_nom', 'resp_prenom'),)
        constraints = [
            models.UniqueConstraint(fields=["resp_nom", "resp_prenom"], name="resp_nom_prenom")
        ]
    def __str__(self) :
        return self.resp_nom + ' ' + self.resp_prenom + ' --- ' + str(self.responsabilite)

class ResponsableDe(models.Model):
    conf_intitule = models.ForeignKey(Conference, models.DO_NOTHING, db_column="Conf_intitule")
    # Ces champs sont déjà dans la table 'Reponsable'
    # resp_nom = models.ForeignKey(Responsable, models.DO_NOTHING, db_column='Resp_nom')  # Field name made lowercase.
    # resp_prenom = models.ForeignKey(Responsable, models.DO_NOTHING, db_column='Resp_prenom', to_field='resp_prenom', related_name='responsablede_resp_prenom_set')  # Field name made lowercase.
    responsable = models.ForeignKey(Responsable, models.DO_NOTHING, db_column="responsable")

    class Meta:
        managed = True
        db_table = "responsable_de"
        # unique_together = (('conf_intitule', 'resp_nom', 'resp_prenom'), ('conf_intitule', 'resp_nom', 'resp_prenom'),)
        constraints = [
            models.UniqueConstraint(fields=["conf_intitule", "responsable"], name="conf_responsable")
        ]
    def __str__(self) :
        return str(self.conf_intitule) + ' --- ' + str(self.responsable)


class Session(models.Model):
    sess_intitule = models.CharField(db_column="Sess_intitule", primary_key=True, max_length=100)  # Field name made lowercase.
    themes = models.CharField(db_column="Themes", max_length=100)  # Field name made lowercase.
    conf_intitule = models.ForeignKey(Conference, models.DO_NOTHING, db_column="Conf_intitule")  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "session"

    def __str__(self) :
        return self.sess_intitule

class Soumission(models.Model):
    soumi_intitule = models.CharField(db_column='Soumi_intitule', primary_key=True, max_length=100)  # Field name made lowercase.
    date_de_soumission = models.DateField(db_column='Date_de_soumission')  # Field name made lowercase.
    session_intitule = models.ForeignKey(Session, models.DO_NOTHING, db_column='session_intitule')
    etat = models.CharField(db_column='Etat', max_length=10 )
    categorie =  models.ForeignKey(CategorieDeSoumission, models.DO_NOTHING, db_column='categorie')
    # champs déjà renseignés dans la table 'Utilisateur'
    # util_nom = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='Util_nom')  # Field name made lowercase.
    # util_prenom = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='Util_prenom', to_field='util_prenom', related_name='soumission_util_prenom_set')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "soumission"

    def __str__(self) :
        return self.soumi_intitule


class Workshop(models.Model):
    wk_intitule = models.OneToOneField(Soumission, models.DO_NOTHING, db_column='wk_intitule', primary_key=True)  # Field name made lowercase.
    date_de_debut = models.DateField(db_column='Date_de_debut')  # Field name made lowercase.
    date_de_fin = models.DateField(db_column='Date_de_fin')  # Field name made lowercase.
    loc_ville = models.CharField(db_column='Loc_Ville', max_length=15)  # Field name made lowercase.
    loc_pays = models.CharField(db_column='Loc_Pays', max_length=15)  # Field name made lowercase.
    serie = models.CharField(db_column='Serie', max_length=10)  # Field name made lowercase.
    text_introductif = models.TextField(db_column='Text_introductif')  # Field name made lowercase.
    editeur_actes = models.CharField(db_column='Editeur_actes', max_length=30)  # Field name made lowercase.
    conf_intitule = models.ForeignKey(Conference, models.DO_NOTHING, db_column='Conf_intitule')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "workshop"

    def __str__(self) :
        return str(self.wk_intitule)
