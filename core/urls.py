from django.contrib import admin
from django.urls import path
from users.views import RegisterView, LoginView, LogoutView, TokenRefreshView, ProtectedLoginView, VerifyEmailView, PasswordPolicyView
from chat.views import MessageHistory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/login/', ProtectedLoginView.as_view(), name='login'),
    path('api/auth/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),  
    path('api/auth/check-password/', PasswordPolicyView.as_view(), name='check_password'),
    path('api/chat/<uuid:conversation_id>/history/', MessageHistory.as_view()),
]
