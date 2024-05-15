from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin


class AuthenticateSessionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            return
        user = auth.authenticate(request)
        if hasattr(user, 'backend'):
            request._cached_user = user
            auth.login(
                request, user, user.backend)
