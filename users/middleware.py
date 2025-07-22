from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

class JWTCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/'):
            try:
                # Extract from Authorization header
                auth = JWTAuthentication()
                header = auth.get_header(request)
                if header:
                    raw_token = auth.get_raw_token(header)
                    validated_token = auth.get_validated_token(raw_token)
                    request.user = auth.get_user(validated_token)
                    
            except AuthenticationFailed:
                # API routes require valid auth
                if request.path not in ['/api/auth/login/', '/api/auth/register/']:
                    raise

class RateLimitHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if hasattr(request, 'limiter'):
            remaining = request.limiter.limiter['remaining']
            reset = response.limiter['reset']

            response['X-RateLimit-Remaining'] = remaining
            response['X-RateLimit-Reset'] = reset

            if int(remaining) <= 0:
                response['Retry-After'] = reset

        return response