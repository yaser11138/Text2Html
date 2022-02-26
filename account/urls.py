from django.urls import path,include
from .views import signup,login,verification,logout_view,ResetPasswordView
from django.contrib.auth import urls
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("signup/", signup),
    path("login/", login),
    path("verification/<slug:id>/", verification),
    path('logout/', logout_view),
    path("reset/",ResetPasswordView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password-rese-conformationt.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password-rese-done.html'),
         name='password_reset_complete'),


]