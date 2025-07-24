from django.shortcuts import render
from django.contrib.auth import authenticate
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
from .auth import generate_tokens, blacklist_token
from .serializers import UserRegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.svae()
            user.send_verification_email() 
            tokens = generate_tokens(user)
            response = Response(tokens, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='refresh_token',
                value=tokens['refresh'],
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('useranme')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        tokens = generate_tokens(user)
        response = Response(
            {'access': tokens['access']},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=604800
        )

        return response

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                blacklist_token(refresh_token)
            
            response = Response(
                {'message': 'Successfully logged out'},
                status=status.HTTP_200_OK
            )
            response.delete_cookie('refresh_token')
            return response
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class RateLimitedResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(
            data={
                "error": "too_many_requests",
                "message": "You've made too many requests. Please try again later."
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
            *args,
            **kwargs
        )
@method_decorator(ratelimit(key='ip', rate='5/m', method='POST'), name='post')
class ProtectedLoginView(LoginView):
    pass 

class VerifyEmailView(APIView):  
    def get(self, request, token):  
        try:  
            user = User.objects.get(verification_token=token)  
            if (timezone.now() - user.verification_sent_at).days > 3:  
                return Response(  
                    {'error': 'verification_expired'},  
                    status=status.HTTP_400_BAD_REQUEST  
                )  

            user.email_verified = True  
            user.verification_token = ''  
            user.save()  

            return Response(  
                {'message': 'Email successfully verified'},  
                status=status.HTTP_200_OK  
            )  

        except User.DoesNotExist:  
            return Response(  
                {'error': 'invalid_token'},  
                status=status.HTTP_400_BAD_REQUEST  
            )  