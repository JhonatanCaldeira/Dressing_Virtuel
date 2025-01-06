from django.http import HttpRequest

def client_authenticated(request: HttpRequest):
    """
    Adds 'client_authenticated' to the template context.
    """
    return {'client_authenticated': bool(request.session.get('client_id'))}
