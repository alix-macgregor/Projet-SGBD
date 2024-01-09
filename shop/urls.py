"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store.views import ajouter, ajouter_conf, index, inscrits, nouvelle_conf, nouvelle_conf_orga, nouvelle_soumi, process_form, process_form_ajout, process_form_orga, process_type_util, inscription, recherche, nouvelle_conf_orga, process_form_respo, responsables, soumettre, soumission, changer_etat, changer_etat_2

urlpatterns = [
    # url pour les administrateur du site
    path('admin/', admin.site.urls),

    # urls communes à tout type de personnes (orga, util, respo, prog comité)
    path('', index, name='index'),
    path('process_type', process_type_util, name="process_type"),
    path('soumission', soumettre, name='soumettre'),
    path('nouvelle_soumi', nouvelle_soumi, name='nouvelle_soumi'),

    # urls spécifiques aux utilisateurs
    path('utilisateur/process_form', process_form, name = 'process_form'),
    path('utilisateur/inscription/<str:conf_intitule>/<int:id_util>', inscription, name='inscription'),
    path('utilisateur/recherche/<int:id_util>', recherche, name='recherche'),

    # urls spécifiques aux organisateurs
    path('organisateur/process_form_orga', process_form_orga, name = 'process_form_orga'),
    path('organisateur/nouvelle_conférence/<str:orga_nom>/<str:mail>/<str:adresse>', nouvelle_conf_orga, name='nouvelle_conf_orga'),
    path('organisateur/ajouter_conf/<str:orga_nom>', ajouter_conf, name='ajouter_conf'),
    path('organisateur/nouvelle_conf/<str:orga_nom>', nouvelle_conf, name='nouvelle_conf'),
    path('organisateur/inscrits/<str:conf_intitule>', inscrits, name='inscrits'),
    path('organisateur/responsables/<str:conf_intitule>', responsables, name='responsables'),
    path('organisateur/ajouter/<str:conf_intitule>', ajouter, name = 'ajouter'),
    path('organisateur/ajouter2/<str:conf_intitule>', process_form_ajout, name = 'process_form_ajout'),

    # urls spécifiques aux responsables
    path('responsable/process_form_respo', process_form_respo, name= 'process_form_respo'),
    path('responsable/soumissions/<str:conf_intitule>', soumission, name='soumissions'),
    path('responsable/changer_etat/<str:soumi_intitule>', changer_etat, name='changer_etat'),
    path('responsable/changer_etat2/<str:soumi_intitule>', changer_etat_2, name='changer_etat_2'),

]
