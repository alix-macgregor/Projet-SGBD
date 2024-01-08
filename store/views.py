from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from store.models import Conference, Inscription, Session, Utilisateur, Workshop

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
        input3 = request.POST.get('email')

        util = Utilisateur.objects.filter(util_nom=input1, util_prenom=input2)
        if len(util) == 0 :
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
