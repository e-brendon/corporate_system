from django.urls import path 
from config import views

urlpatterns = [
    path('', views.painel_view, name='painel'),
    path('dashboard/lista-postagem/', views.dashboard_lista_postagem_view, name='dash-lista-postagem-forum'),
    path('configuracao/', views.configuracao_view, name='configuracao'),
    path('relatorio/', views.relatorio_view, name='relatorio'),
]
