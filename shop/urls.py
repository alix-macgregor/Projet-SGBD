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
from store.views import index, inscrits, nouvelle_conf_orga, process_form, process_form_orga, process_type_util, inscription, recherche, nouvelle_conf_orga

urlpatterns = [
    # url pour les administrateur du site
    path('admin/', admin.site.urls),

    # urls communes à tout type de personnes (orga, util, respo, prog comité)
    path('', index, name='index'),
    path('process_type', process_type_util, name="process_type"),

    # urls spécifiques aux utilisateurs
    path('utilisateur/process_form', process_form, name = 'process_form'),
    path('utilisateur/inscription/<str:conf_intitule>/<int:id_util>', inscription, name='inscription'),
    path('utilisateur/recherche/<int:id_util>', recherche, name='recherche'),

    # urls spécifique aux organisateurs
    path('organisateur/process_form_orga', process_form_orga, name = 'process_form_orga'),
    path('organisateur/nouvelle_conférence/<str:orga_nom>/<str:mail>/<str:adresse>', nouvelle_conf_orga, name='nouvelle_conf_orga'),
    path('organisateur/inscrits/<str:conf_intitule>', inscrits, name='inscrits'),

]
