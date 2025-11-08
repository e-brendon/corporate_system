from django.contrib import messages
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from forum.forms import PostagemForumForm, ComentarioPostagemForumForm
from forum import models
from base.utils import add_form_errors_to_messages
# Create your views here.

GRUPOS_GESTAO = ('administrador', 'colaborador')


def _usuario_gestor(user):
    return user.is_superuser or user.groups.filter(name__in=GRUPOS_GESTAO).exists()


def _pode_editar_comentario(user, comentario):
    if not user.is_authenticated:
        return False
    if _usuario_gestor(user):
        return True
    if comentario.usuario != user:
        return False
    limite = comentario.criado_em + timedelta(hours=24)
    return timezone.now() <= limite

# Lista de postagens 
def lista_postagem_forum(request):
    postagens = models.PostagemForum.objects.filter(ativo=True).select_related('usuario')
    context = {'postagens': postagens}
    return render(request, 'lista-postagens-forum.html', context)

# Cria postagens 
@login_required
def criar_postagem_forum(request):
    form = PostagemForumForm(user=request.user)
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.usuario = request.user
            if not _usuario_gestor(request.user):
                forum.data_publicacao = timezone.localtime().date()
            forum.save()
            form.save_m2m()
            # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
            messages.success(request, 'Seu Post foi cadastrado com sucesso!')
            return redirect('lista-postagem-forum')
        else:
            add_form_errors_to_messages(request, form)         
    return render(request, 'form-postagem-forum.html', {'form': form})

# Detalhes da postagem (ID)
def detalhe_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    comentarios = (
        postagem.comentarios.filter(parent__isnull=True)
        .select_related('usuario')
        .prefetch_related('respostas__usuario')
    )
    form = ComentarioPostagemForumForm()
    comentarios_editaveis = set()
    if request.user.is_authenticated:
        for comentario in postagem.comentarios.select_related('usuario'):
            if _pode_editar_comentario(request.user, comentario):
                comentarios_editaveis.add(comentario.id)
    context = {
        'postagem': postagem,
        'comentarios': comentarios,
        'form_comentario': form,
        'comentarios_editaveis': comentarios_editaveis,
        'usuario_gestor': _usuario_gestor(request.user),
    }
    return render(request, 'detalhe-postagem-forum.html', context)

# Editar postagem (ID)
@login_required 
def editar_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    if request.user != postagem.usuario and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para editar esta postagem.')
        return redirect('detalhe-postagem-forum', id=postagem.id)
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES, instance=postagem, user=request.user)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Seu Post '+ postagem.titulo +' foi atualizado com sucesso!')
            return redirect('editar-postagem-forum', id=postagem.id)
        else:
            add_form_errors_to_messages(request, form)
    else:
        form = PostagemForumForm(instance=postagem, user=request.user)
    return render(request, 'form-postagem-forum.html', {'form': form})

# remover postagem (ID)
@login_required
def deletar_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, 'Sua postagem '+ postagem.titulo +' foi removido com sucesso!')
        return redirect('lista-postagem-forum')
    return render(request, 'detalhe-postagem-forum.html', {'postagem': postagem})


@login_required
def criar_comentario_forum(request, postagem_id):
    postagem = get_object_or_404(models.PostagemForum, id=postagem_id)
    form = ComentarioPostagemForumForm(request.POST)
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.postagem = postagem
        comentario.usuario = request.user
        parent_id = request.POST.get('parent_id')
        if parent_id:
            comentario.parent = get_object_or_404(
                models.ComentarioPostagemForum,
                id=parent_id,
                postagem=postagem,
            )
        comentario.save()
        messages.success(request, 'Seu comentário foi publicado.')
    else:
        add_form_errors_to_messages(request, form)
    return redirect(f"{reverse('detalhe-postagem-forum', args=[postagem.id])}#comentarios")


@login_required
def editar_comentario_forum(request, comentario_id):
    comentario = get_object_or_404(models.ComentarioPostagemForum, id=comentario_id)
    if request.method != 'POST':
        return redirect(f"{reverse('detalhe-postagem-forum', args=[comentario.postagem_id])}#comentarios")
    if not _pode_editar_comentario(request.user, comentario):
        messages.error(request, 'Você não pode editar este comentário.')
        return redirect(f"{reverse('detalhe-postagem-forum', args=[comentario.postagem_id])}#comentarios")
    form = ComentarioPostagemForumForm(request.POST, instance=comentario)
    if form.is_valid():
        form.save()
        messages.success(request, 'Comentário atualizado com sucesso.')
    else:
        add_form_errors_to_messages(request, form)
    return redirect(f"{reverse('detalhe-postagem-forum', args=[comentario.postagem_id])}#comentarios")


@login_required
def deletar_comentario_forum(request, comentario_id):
    comentario = get_object_or_404(models.ComentarioPostagemForum, id=comentario_id)
    if request.method != 'POST':
        return redirect(f"{reverse('detalhe-postagem-forum', args=[comentario.postagem_id])}#comentarios")
    if not _usuario_gestor(request.user):
        messages.error(request, 'Apenas administradores podem deletar comentários.')
        return redirect(f"{reverse('detalhe-postagem-forum', args=[comentario.postagem_id])}#comentarios")
    comentario.delete()
    messages.success(request, 'Comentário removido.')
    return redirect(f"{reverse('detalhe-postagem-forum', args=[comentario.postagem_id])}#comentarios")
