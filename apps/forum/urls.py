from django.urls import path
from forum import views
urlpatterns = [
    path('',views.lista_postagem_forum, name='lista-postagem-forum'),
    path('criar-postagem-forum/', views.criar_postagem_forum, name='criar-postagem-forum'),
    path('detalhe-postagem-forum/<int:id>/', views.detalhe_postagem_forum, name='detalhe-postagem-forum'),
    path('editar-postagem-forum/<int:id>/', views.editar_postagem_forum, name='editar-postagem-forum'),
    path('deletar-postagem-forum/<int:id>/', views.deletar_postagem_forum, name='deletar-postagem-forum'),
    path('postagens/<int:postagem_id>/comentarios/', views.criar_comentario_forum, name='criar-comentario-forum'),
    path('comentarios/<int:comentario_id>/editar/', views.editar_comentario_forum, name='editar-comentario-forum'),
    path('comentarios/<int:comentario_id>/deletar/', views.deletar_comentario_forum, name='deletar-comentario-forum'),
]
