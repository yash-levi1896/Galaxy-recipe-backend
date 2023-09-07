from rest_framework.authtoken.models import Token
from django.http import JsonResponse

def token_auth_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Extract the token from the request header
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')

        if authorization_header:
            token = authorization_header.split()
            if len(token) == 2 and token[0].lower() == 'bearer':
                token = token[1]
                try:
                    # Authenticate the user using the token
                    user = Token.objects.get(key=token).user
                    request.user = user
                except Token.DoesNotExist:
                    request.user = None

        if not request.user:
            # Handle the case where the Authorization header is missing or invalid
            return JsonResponse({'msg':'Please Login !'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view








      
