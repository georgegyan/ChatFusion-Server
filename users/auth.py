from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

def blacklist_token(refresh_token):
    token = RefreshToken(refresh_token)
    token.blacklist()
    cache.set(f"blacklisted_{refresh_token}", True, timeout=60*60*24*7)
    