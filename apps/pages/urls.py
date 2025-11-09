from django.urls import path
from pages import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contato/', views.contato, name='contato'),
]
