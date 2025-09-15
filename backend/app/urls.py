from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    # Registrazione Utenti e JWT token management
    # Il primo utente che si registra diventa admin
    path('signon', views.RegisterView.as_view(), name='signon'),  # Per registrarsi e ottenere JWT Tokens
    path('signin', views.login_view, name='signin'), # Per fare il login e ottenere JWT Tokens
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),   # SimpleJWT route to refresh an expired token
    path('signout', views.logout_view, name='signout'),

    # Data endpoints
    path('deals', views.deals_list, name='deals_list'),
    path('dealDetail', views.deal_detail, name='deal_detail'),

    # User endpoints
    path('admin-exist', views.admin_exist, name='admin_exist'),

]