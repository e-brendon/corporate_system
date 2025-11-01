from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from forum.models import PostagemForum

@login_required
def painel_view(request):
    return render(request, 'painel.html')

@login_required
def configuracao_view(request):
    return render(request, 'configuracao.html')

@login_required
def relatorio_view(request):
    return render(request, 'relatorio.html')

@login_required
def dashboard_lista_postagem_view(request):
    grupos_gestao = ['administrador', 'colaborador']
    usuario = request.user
    if usuario.is_superuser or usuario.groups.filter(name__in=grupos_gestao).exists():
        postagens = PostagemForum.objects.filter(ativo=True).select_related('usuario')
    else:
        postagens = PostagemForum.objects.filter(usuario=usuario).select_related('usuario')
    context = {'postagens': postagens}
    return render(request, 'dashboard/dash-lista-postagem-forum.html', context)
