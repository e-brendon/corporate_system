# from pages import models

import os

from django.db import OperationalError, ProgrammingError

from config.models import EmpresaContato


def context_social(request):
    user = getattr(request, 'user', None)
    can_manage_users = False
    if user and user.is_authenticated:
        can_manage_users = user.groups.filter(name__in=['administrador', 'colaborador']).exists()
    contato = None
    try:
        contato = EmpresaContato.objects.first()
    except (OperationalError, ProgrammingError):
        contato = None
    return {
        'social': 'Exibir este contexto em qualquer lugar!',
        'can_manage_users': can_manage_users,
        'app_name': os.getenv('APP_NAME', 'x'),
        'author': os.getenv('AUTHOR', 'x'),
        'release': os.getenv('RELEASE', 'x'),
        'patch': os.getenv('PATCH', 'x'),
        'core': os.getenv('CORE', 'x'),
        'empresa_contato': contato,
    }
