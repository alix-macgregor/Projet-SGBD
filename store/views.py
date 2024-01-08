from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from store.models import Conference, Inscription, Organisateur, Organise, Session, Utilisateur, Workshop

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

    themes = []
    for sess in session :
        for theme in sess.themes.split(', ') :
            if theme not in themes :
                themes.append(theme)

    util.profil = ', '.join(themes)
    util.save()

    for tuple in Inscription.objects.values_list('conf_intitule', 'utilisateur') :
        if (conf_intitule, id_util) == tuple :
            deja_inscrit = True

    if not deja_inscrit :
        inscri = Inscription()
        inscri.conference = Conference.objects.filter(conf_intitule=conf_intitule)[0]
        inscri.utilisateur = Utilisateur.objects.filter(id_util=id_util)[0]
        inscri.conf_intitule = inscri.conference
        inscri.save()
        return render(request, 'utilisateur/inscription.html')

    else :
        return HttpResponse('Vous êtes déjà inscrit.e')

""" Espace Organisateur"""
# Crée un nouvel orga en forçant la création d'un conférence associée :
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

def accueil_orga(request, orga_nom) :
    orga = Organisateur.objects.filter(orga_nom=orga_nom)[0]

    conf = Conference.objects.filter(conf_intitule=orga.conf_intitule)[0]

    return render(request, 'organisateur/accueil_perso.html', context={"organisateur":orga, "confs":[conf]})

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
