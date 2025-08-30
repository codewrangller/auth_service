from django.urls import path, include
from . import views



core_urls = [
   path('login/', views.LoginView.as_view(), name='rest_login'),
   path('register/', views.RegisterView.as_view(), name='register'),
   path('password/reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
   path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]


urlpatterns = [
   path('api/v1/', include(core_urls)),
]
