from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [


    # Registrazione Utenti e JWT token management
    # Il primo utente che si registra diventa admin
    path('register', views.RegisterView.as_view(), name='register'),  # Per registrarsi e ottenere JWT Tokens
    path('login', views.login_view, name='login'), # Per fare il login e ottenere JWT Tokens
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),   # SimpleJWT route to refresh an expired token
    
    # Data endpoints
    path('deals', views.deals_list, name='deals_list'),
    path('deals/<str:deal_id>/', views.deal_detail, name='deal_detail'),

    # User endpoints
    path('profile', views.user_profile, name='user_profile'),

]