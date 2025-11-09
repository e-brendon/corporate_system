from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from config.models import HomePageConfig
from forum import models as forum_models

# Create your views here.
def index(request):
    config = None
    try:
        config = HomePageConfig.obter_unico()
    except Exception:
        config = None

    latest_posts = []
    engaged_posts = []

    if config and (config.mostrar_ultimas_postagens or config.mostrar_postagens_interagidas):
        hoje = timezone.localdate()
        base_queryset = forum_models.PostagemForum.objects.filter(ativo=True).filter(
            Q(data_publicacao__isnull=True) | Q(data_publicacao__lte=hoje)
        ).select_related('usuario')

        if config.mostrar_ultimas_postagens:
            latest_posts = list(base_queryset.order_by('-data_criacao')[:5])

        if config.mostrar_postagens_interagidas:
            anotadas = list(
                base_queryset.annotate(total_interacoes=Count('comentarios')).order_by('-total_interacoes', '-data_criacao')[:5]
            )
            if anotadas and any(post.total_interacoes for post in anotadas):
                engaged_posts = anotadas
            else:
                engaged_posts = latest_posts or list(base_queryset.order_by('-data_criacao')[:5])

    for post in engaged_posts:
        if not hasattr(post, 'total_interacoes'):
            post.total_interacoes = 0

    context = {
        'homepage_config': config,
        'latest_posts': latest_posts,
        'engaged_posts': engaged_posts,
    }
    return render(request, 'index.html', context)


def contato(request):
    return render(request, 'contato.html')
