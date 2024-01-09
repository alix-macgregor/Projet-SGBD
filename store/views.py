# Importation
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from store.models import CategorieDeSoumission, Conference, Evaluation, Inscription, Organisateur, Organise, ProgramCommitee, Responsabilite, Responsable, ResponsableDe, Session, Utilisateur, Workshop, Soumission

# Vue qui permettent de séparer les différents types d'utilisateurs :
def index(request) :
    return render(request, 'store/index.html')

def index_type(request, type) :
    return render(request, f'{type}/index.html')

def process_type_util(request) :
    if request.method == 'POST':
        input = request.POST.get("select")
        return index_type(request, input)

    else:
        return HttpResponse('Invalid request method')

""" Espace Utilisateur """
# Permettent de passer du formulaire à l'espace personnel :
def process_form(request) :
    if request.method == 'POST' :
        input1 = request.POST.get('name')
        input2 = request.POST.get('surname')

        util = Utilisateur.objects.filter(util_nom=input1, util_prenom=input2)
        if len(util) == 0 :
            input3 = request.POST.get('email')
            if input3 == '' :
                return HttpResponse('Veuillez indiquer une adresse mail')

            util = Utilisateur(util_nom=input1, util_prenom=input2, mail=input3)
            util.save()
            util = Utilisateur.objects.filter(util_nom=input1, util_prenom=input2)

        id = util[0].id_util
        return accueil_perso(request, id)

    else:
        return HttpResponse('Invalid request method')

def accueil_perso(request, id_util) :
    util = Utilisateur.objects.filter(id_util=id_util)[0]

    if util.profil == 'null' :
        util.profil = ''
        util.save()

    if util.profil != '' :
        profil = util.profil.split(', ')
        tot_confs = []
        tot_wk = []
        for theme in profil :
            confs = Conference.objects.filter(conf_intitule__icontains=theme, date_de_debut__gt = timezone.now())
            workshops = Workshop.objects.filter(text_introductif__icontains=theme, date_de_debut__gt = timezone.now())
            if len(confs) != 0 :
                for conf in confs :
                    if conf not in tot_confs :
                        tot_confs.append(conf)

            if len(workshops) != 0 :
                for workshop in workshops :
                    if workshop not in tot_wk :
                        tot_wk.append(workshop)

    else :
        tot_confs = Conference.objects.filter(date_de_debut__gt = timezone.now())
        tot_wk = Workshop.objects.filter(date_de_debut__gt = timezone.now())

    return render(request, 'utilisateur/accueil_perso.html', context={"utilisateur":util, "confs":tot_confs, "workshops":tot_wk})

# Permettent d'effectuer les recherches :
def recherche(request, id_util) :
    util = Utilisateur.objects.filter(id_util=id_util)[0]

    if request.method == 'GET' :
        input = request.GET.get('query')
        if input != '' :
            search = input.split(' ')
            tot_confs = []
            tot_wk = []
            for theme in search :
                confs = Conference.objects.filter(Q(conf_intitule__icontains=theme)| Q(text_introductif__icontains=theme) | Q(loc_ville__icontains=theme) | Q(loc_pays__icontains=theme), date_de_debut__gt = timezone.now())
                workshops = Workshop.objects.filter(Q(text_introductif__icontains=theme) | Q(loc_ville__icontains=theme) | Q(loc_pays__icontains=theme), date_de_debut__gt = timezone.now())
                if len(confs) != 0 :
                    for conf in confs :
                        if conf not in tot_confs :
                            tot_confs.append(conf)

                if len(workshops) != 0 :
                    for workshop in workshops :
                        if workshop not in tot_wk :
                            tot_wk.append(workshop)

        else :
            tot_confs = Conference.objects.filter(date_de_debut__gt = timezone.now())
            tot_wk = Workshop.objects.filter(date_de_debut__gt = timezone.now())
        return render(request, 'utilisateur/recherche.html', context={"utilisateur":util, "confs":tot_confs, "workshops": tot_wk} )

    else :
        return HttpResponse('Invalid request method')

# Permettent à l'utilisateur de s'inscrire à une conférence
def inscription(request, conf_intitule, id_util) :
    session = Session.objects.filter(conf_intitule=conf_intitule)
    util = Utilisateur.objects.filter(id_util=id_util)[0]

    deja_inscrit = False

    for tuple in Inscription.objects.values_list('conf_intitule', 'utilisateur') :
        if (conf_intitule, id_util) == tuple :
            deja_inscrit = True

    if not deja_inscrit :
        themes = []
        for sess in session :
            for theme in sess.themes.split(', ') :
                if theme not in themes :
                    themes.append(theme)

        util.profil = ', '.join(themes)
        util.save()

        inscri = Inscription()
        inscri.conference = Conference.objects.filter(conf_intitule=conf_intitule)[0]
        inscri.utilisateur = Utilisateur.objects.filter(id_util=id_util)[0]
        inscri.conf_intitule = inscri.conference
        inscri.save()
        return render(request, 'utilisateur/inscription.html')

    else :
        return HttpResponse('Vous êtes déjà inscrit.e')

""" Espace Organisateur"""
# Crée un nouvel orga en forçant la création d'une conférence associée :
def new_orga(request, orga_nom, mail, adresse, conf_intitule) :
    conf = Conference.objects.filter(conf_intitule=conf_intitule)[0]
    nouvel_orga = Organisateur(orga_nom=orga_nom, mail=mail, adresse=adresse, conf_intitule=conf)
    nouvel_orga.save()

    return accueil_orga(request, orga_nom)


def nouvelle_conf_orga(request, orga_nom, mail, adresse) :
    if request.method == 'POST' :
        input1 = request.POST.get('conf_intitule')
        input2 = request.POST.get('text_introductif')
        input3 = request.POST.get('serie')
        input4 = request.POST.get('editeur_acte')
        input5 = request.POST.get('date_de_debut')
        input6 = request.POST.get('date_de_fin')
        input7 = request.POST.get('loc_ville')
        input8 = request.POST.get('loc_pays')

        nouvelle_conf = Conference(conf_intitule=input1,
                                   text_introductif=input2,
                                   serie=input3,
                                   editeur_actes=input4,
                                   date_de_debut=input5,
                                   date_de_fin=input6,
                                   loc_ville=input7,
                                   loc_pays=input8
                                   )
        nouvelle_conf.save()

        return new_orga(request, orga_nom, mail, adresse, input1)

    else :
        return HttpResponse('Invalid request method')

def process_form_orga(request) :
    if request.method == 'POST' :
        input1 = request.POST.get('name')

        orga = Organisateur.objects.filter(orga_nom=input1)
        if len(orga) == 0 :
            input2 = request.POST.get('email')
            input3 = request.POST.get('adresse')

            if input2 == '' or input3 == '' :
                return HttpResponse('Veuillez indiquer un mail et une adresse')

            return render(request, 'organisateur/nouvelle_conf_orga.html', context={'orga_nom':input1,'mail':input2, 'adresse':input3})

        return accueil_orga(request, input1)

    else:
        return HttpResponse('Invalid request method')

# Ajouter des conférences :
def ajouter_conf(request, orga_nom) :
    return render(request, 'organisateur/nouvelle_conf.html', context={'orga_nom':orga_nom})

def nouvelle_conf(request, orga_nom) :
    orga = Organisateur.objects.filter(orga_nom=orga_nom)[0]

    if request.method == 'POST' :
        input1 = request.POST.get('conf_intitule')
        input2 = request.POST.get('text_introductif')
        input3 = request.POST.get('serie')
        input4 = request.POST.get('editeur_acte')
        input5 = request.POST.get('date_de_debut')
        input6 = request.POST.get('date_de_fin')
        input7 = request.POST.get('loc_ville')
        input8 = request.POST.get('loc_pays')

        nouvelle_conf = Conference(conf_intitule=input1,
                                   text_introductif=input2,
                                   serie=input3,
                                   editeur_actes=input4,
                                   date_de_debut=input5,
                                   date_de_fin=input6,
                                   loc_ville=input7,
                                   loc_pays=input8
                                   )
        nouvelle_conf.save()

        nouvel_orga = Organisateur(orga_nom=orga_nom, mail=orga.mail, adresse=orga.adresse, conf_intitule=nouvelle_conf)
        nouvel_orga.save()

        return accueil_orga(request, orga_nom)

    else :
        return HttpResponse('Invalid request method')

# Affiche les conférences qu'il organise
def accueil_orga(request, orga_nom) :
    orgas = Organisateur.objects.filter(orga_nom=orga_nom)

    confs = [Conference.objects.filter(conf_intitule=orga.conf_intitule)[0] for orga in orgas]

    orga = orgas[0]

    return render(request, 'organisateur/accueil_perso.html', context={"organisateur":orga, "confs":confs})

# Permet d'afficher la liste de tous les inscrits pour une conférence
def inscrits(request, conf_intitule) :
    inscriptions = Inscription.objects.filter(conf_intitule=conf_intitule)

    if len(inscriptions) != 0 :
        inscrits = []
        for inscription in inscriptions :
            id_util = inscription.utilisateur.id_util
            util = Utilisateur.objects.filter(id_util=id_util)[0]
            inscrits.append([util.util_prenom + ' ' + util.util_nom, util.profil])

        return render(request, 'store/inscrits.html', context={'inscrits':inscrits, "conf":conf_intitule})

    else :
        return HttpResponse("Pas d'inscrits")

# Permet d'accéder à la liste des responsables
def responsables(request, conf_intitule) :
    organise = Organise.objects.filter(conf_intitule=conf_intitule)
    responsable_de = ResponsableDe.objects.filter(conf_intitule=conf_intitule)

    liste_pc_id = [pc.prog_commitee for pc in organise]
    liste_respo_id = [respo.responsable for respo in responsable_de]

    liste_pc = [ProgramCommitee.objects.filter(id_prog_commitee=pc.id_prog_commitee)[0] for pc in liste_pc_id]
    liste_respo = [Responsable.objects.filter(id_resp=respo.id_resp)[0] for respo in liste_respo_id]

    return render(request, 'organisateur/responsables.html', context={'conf':conf_intitule, 'responsables': liste_respo, 'pc':liste_pc})

# Permet d'ajouter des responsables dans une conférence
def ajouter(request, conf_intitule) :
    return render(request, 'organisateur/ajouter.html', context={'conf':conf_intitule})

def process_form_ajout(request, conf_intitule) :
    conf = Conference.objects.filter(conf_intitule=conf_intitule)[0]
    orga = Organisateur.objects.filter(conf_intitule=conf_intitule)[0]

    if request.method == 'POST' :
        input1 = request.POST.get('name')
        input2 = request.POST.get('surname')

        input5 = request.POST.get('select')

        # On sépare les programme commitee du reste
        if input5 == "Programme Commitee" :
            respo = ProgramCommitee.objects.filter(pc_nom=input1, pc_prenom=input2)

            # On vérifie que le responsable existe
            if len(respo) == 0 :
                input3 = request.POST.get('email')
                input4 = request.POST.get('adresse')

                if input2 == '' or input3 == '' :
                    return HttpResponse('Veuillez indiquer un mail et une adresse')


                new_respo = ProgramCommitee(pc_nom=input1, pc_prenom=input2, adresse_professionnelle=input4, mail=input3)
                new_respo.save()

                new_organise = Organise(conf_intitule=conf, prog_commitee=new_respo)
                new_organise.save()

                return accueil_orga(request, orga.orga_nom)

            else :
                # On vérifie que le responsable n'est pas déjà responsable de cette conférence
                respo = respo[0]
                deja_respo = False

                for tuple in Organise.objects.values_list('conf_intitule', 'prog_commitee') :
                    if (conf_intitule, respo.id_prog_commitee) == tuple :
                        deja_respo = True

                if deja_respo :
                    return HttpResponse('Cette personne est déjà responsable')

                else :
                    new_organise = Organise(conf_intitule=conf, prog_commitee=respo)
                    new_organise.save()

                    return accueil_orga(request, orga.orga_nom)

        else :
            # Et on fait la même chose avec les autres responsables
            respo = Responsable.objects.filter(resp_nom=input1, resp_prenom=input2)
            responsabilite = Responsabilite(responsabilite=input5)
            if len(respo) == 0 :
                input3 = request.POST.get('email')
                input4 = request.POST.get('adresse')

                if input2 == '' or input3 == '' :
                    return HttpResponse('Veuillez indiquer un mail et une adresse')

                new_respo = Responsable(resp_nom=input1, resp_prenom=input2, adresse_professionnelle=input4, mail=input3, responsabilite=responsabilite)
                new_respo.save()

                new_organise = ResponsableDe(conf_intitule=conf, responsable=new_respo)
                new_organise.save()

                return accueil_orga(request, orga.orga_nom)

            else :
                respo = respo[0]
                deja_respo = False

                for tuple in ResponsableDe.objects.values_list('conf_intitule', 'responsable') :
                    if (conf_intitule, respo.id_resp) == tuple :
                        deja_respo = True

                if deja_respo :
                    return HttpResponse('Cette personne est déjà responsable')

                else :
                    new_organise = Organise(conf_intitule=conf, prog_commitee=respo)
                    new_organise.save()

                    return accueil_orga(request, orga.orga_nom)

    else:
        return HttpResponse('Invalid request method')


""" Espace Responsables """
# Permet à un responsable de se connecter aux conférences qu'il organise et diférencie les responsables lambda des programme commitee
def process_form_respo(request) :
    if request.method == 'POST' :
        input1 = request.POST.get('name')
        input2 = request.POST.get('surname')

        input5 = request.POST.get('select')

        if input5 == "Programme Commitee" :
            respo = ProgramCommitee.objects.filter(pc_nom=input1, pc_prenom=input2)
            if len(respo) == 0 :
                input3 = request.POST.get('email')
                input4 = request.POST.get('adresse')

                if input2 == '' or input3 == '' :
                    return HttpResponse('Veuillez indiquer un mail et une adresse')


                new_respo = ProgramCommitee(pc_nom=input1, pc_prenom=input2, adresse_professionnelle=input4, mail=input3)
                new_respo.save()

            return accueil_prog(request, input1, input2)

        else :
            respo = Responsable.objects.filter(resp_nom=input1, resp_prenom=input2)
            if len(respo) == 0 :
                input3 = request.POST.get('email')
                input4 = request.POST.get('adresse')

                if input2 == '' or input3 == '' :
                    return HttpResponse('Veuillez indiquer un mail et une adresse')

                new_respo = Responsable(resp_nom=input1, resp_prenom=input2, adresse_professionnelle=input4, mail=input3, responsabilite=input5)
                new_respo.save()

            return accueil_respo(request, input1, input2)

    else:
        return HttpResponse('Invalid request method')

# Encore une fois on diférencie les responsables lambda et les programmes commitees
def accueil_respo(request, respo_nom, respo_prenom) :
    respo = Responsable.objects.filter(resp_nom=respo_nom, resp_prenom=respo_prenom)[0]

    tot_confs = ResponsableDe.objects.filter(responsable=respo.id_resp)

    confs_intitule = [conf.conf_intitule for conf in tot_confs]

    confs = [Conference.objects.filter(conf_intitule=conf)[0] for conf in confs_intitule]

    return render(request, 'responsable/accueil_respo.html', context={"responsable":respo, "confs":confs})

def accueil_prog(request, pc_nom, pc_prenom) :
    respo = ProgramCommitee.objects.filter(pc_nom=pc_nom, pc_prenom=pc_prenom)[0]

    tot_confs = Organise.objects.filter(prog_commitee=respo.id_prog_commitee)

    confs_intitule = [conf.conf_intitule for conf in tot_confs]

    confs = [Conference.objects.filter(conf_intitule=conf)[0] for conf in confs_intitule]

    return render(request, 'responsable/accueil_pc.html', context={"responsable":respo, "confs":confs})

# Permet de donner la liste des soumissions
def soumission(request, conf_intitule):
    sess = Session.objects.filter(conf_intitule=conf_intitule)

    tot_sess = [session.sess_intitule for session in sess]

    tot_soumi = []
    for sess_intitule in tot_sess :
        soumissions = Soumission.objects.filter(session_intitule=sess_intitule)

        for soumission in soumissions :
            tot_soumi.append(soumission)

    return render(request, 'responsable/soumission.html', context={'conf_intitule':conf_intitule, 'soumissions':tot_soumi})

# Permettent de changer l'état des soumissions
def changer_etat(request, soumi_intitule, id_prog_commitee) :
    return render(request, 'responsable/changer_etat.html', context={'soumi_intitule':soumi_intitule, 'id_prog_commitee':id_prog_commitee})

def changer_etat_2(request, soumi_intitule, id_prog_commitee) :
    soumi = Soumission.objects.filter(soumi_intitule=soumi_intitule)[0]
    prog = ProgramCommitee.objects.filter(id_prog_commitee=id_prog_commitee)[0]

    if request.method == 'POST' :
        input = request.POST.get('select')

        soumi.etat = input
        soumi.save()

        eval = Evaluation(soumi_intitule=soumi, prog_commitee=prog)
        eval.save()
        return HttpResponse('Bien pris en compte')

    else :
        return HttpResponse('Invalid request method')

""" Espace d'ajout des soumissions"""
# doit être présent pour chaque type de personne => on met le bouton dans le template accueil
def soumettre(request) :
    sessions = Session.objects.all()
    categories = CategorieDeSoumission.objects.all()
    return render(request, 'store/soumission.html', context={'sessions':sessions, 'categories':categories})

def nouvelle_soumi(request) :
    if request.method == 'POST' :
        input1 = request.POST.get('soumi_intitule')
        input2 = request.POST.get('select')
        input3 = request.POST.get('select2')

        session = Session.objects.filter(sess_intitule=input2)[0]
        categorie = CategorieDeSoumission.objects.filter(categorie=input3)[0]

        nouvelle_soumission = Soumission(soumi_intitule=input1,
                                   session_intitule=session,
                                   date_de_soumission = timezone.now(),
                                   categorie=categorie,
                                   etat='En attente'
                                   )
        nouvelle_soumission.save()

        return index(request)

    else :
        return HttpResponse('Invalid request method')
