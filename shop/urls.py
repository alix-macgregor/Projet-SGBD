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
from store.views import index, index_type, process_form, process_type_util, inscription, recherche

urlpatterns = [
    path('', index, name='index'),
    path('process_form', process_form, name = 'process_form'),
    path('process_type', process_type_util, name="process_type"),
    path('admin/', admin.site.urls),
    path('<str:type>', index_type, name="index_type"),
    path('inscription/<str:conf_intitule>/<int:id_util>', inscription, name='inscription'),
    path('recherche/<int:id_util>', recherche, name='recherche'),
]
