from django.shortcuts import redirect
from django.urls import reverse

class ClientProfileAuthenticationMiddleware:
    """
    Middleware to ensure users are authenticated.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allowed Urls whitout authentication
        allowed_urls = [reverse('login_view'), reverse('create_user')]

        if request.path not in allowed_urls and not request.session.get('client_id'):
            return redirect('login_view')

        return self.get_response(request)
