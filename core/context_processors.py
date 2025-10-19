# from pages import models

import os


def context_social(request):
    user = getattr(request, 'user', None)
    can_manage_users = False
    if user and user.is_authenticated:
        can_manage_users = user.groups.filter(name__in=['administrador', 'colaborador']).exists()
    return {
        'social': 'Exibir este contexto em qualquer lugar!',
        'can_manage_users': can_manage_users,
        'app_name': os.getenv('APP_NAME', 'e-brendon'),
    }
