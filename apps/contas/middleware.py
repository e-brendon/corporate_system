from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, Resolver404


class ForcePasswordChangeMiddleware:
    """
    Redirect users flagged with `force_change_password` to the password change page
    until they update their credentials.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_names = {
            'password_change',
            'password_change_done',
            'logout',
            'login',
        }

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def process_request(self, request):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return None

        if not getattr(user, 'force_change_password', False):
            return None

        # Allow password change related views and logout
        try:
            match = resolve(request.path_info)
            if match.url_name in self.allowed_names:
                return None
        except Resolver404:
            return None

        # Allow access to static and media files
        if request.path.startswith(settings.STATIC_URL) or request.path.startswith(settings.MEDIA_URL):
            return None

        return redirect('password_change')
