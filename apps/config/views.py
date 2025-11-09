from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import OperationalError, ProgrammingError
from django.shortcuts import render, redirect

from forum.models import PostagemForum
from django.db.models import Count, Q

from config.forms import EmpresaContatoForm, HomePageConfigForm
from config.models import EmpresaContato, HomePageConfig

GRUPOS_GESTAO = ['administrador', 'colaborador']


def _usuario_gestor(user):
    return user.is_superuser or user.groups.filter(name__in=GRUPOS_GESTAO).exists()

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


@login_required
def editar_informacoes_empresa(request):
    if not _usuario_gestor(request.user):
        messages.error(request, 'Você não tem permissão para alterar essas informações.')
        return redirect('configuracao')
    try:
        contato = EmpresaContato.obter_unico()
    except (OperationalError, ProgrammingError):
        messages.error(request, 'Tabela de contatos da empresa não encontrada. Execute as migrações pendentes.')
        return redirect('configuracao')
    if request.method == 'POST':
        form = EmpresaContatoForm(request.POST, instance=contato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informações salvas com sucesso!')
            return redirect('configuracao')
        else:
            messages.error(request, 'Corrija os erros abaixo antes de salvar.')
    else:
        form = EmpresaContatoForm(instance=contato)
    return render(request, 'empresa-contato-form.html', {'form': form})


@login_required
def configurar_pagina_inicial(request):
    if not _usuario_gestor(request.user):
        messages.error(request, 'Você não tem permissão para alterar essas informações.')
        return redirect('configuracao')
    config = HomePageConfig.obter_unico()
    if request.method == 'POST':
        form = HomePageConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações da página inicial salvas com sucesso!')
            return redirect('configuracao')
        else:
            messages.error(request, 'Corrija os erros abaixo antes de salvar.')
    else:
        form = HomePageConfigForm(instance=config)
    return render(request, 'homepage-config-form.html', {'form': form})
