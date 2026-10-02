from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_pagina, name= 'login_pagina'),
    path('inicio/', views.inicio, name= 'inicio'),
    path('agregar/', views.agregar_instrumento, name='agregar_instrumento'),
    path('editar/<int:id>/', views.editar_instrumento, name='editar_instrumento'),
    path('eliminar/<int:id>/', views.eliminar_instrumento, name='eliminar_instrumento'),
    path('api/login/', views.LoginView.as_view(), name='api_login'),
]