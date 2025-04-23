
from django.urls import path
from .api_views import ChangePasswordAPIView, LoginAPIView, PasswordResetRequestAPIView, PasswordResetConfirmAPIView


urlpatterns = [

    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='api-change-password'),

    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='api-password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='api-password-reset-confirm'),

]