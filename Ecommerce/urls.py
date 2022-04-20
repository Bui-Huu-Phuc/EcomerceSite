from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView,LoginView, LogoutView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('items.urls', namespace="items")),
    path('accounts/', include('accounts.urls', namespace="accounts")),

    path('accounts/', include('allauth.urls')),

    #Password reset form
    path('password-reset/', PasswordResetView.as_view(template_name="registration/password_reset.html"), name = "password_reset"),

    #Email sent success message
    path('password-reset-sent/', PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name = "password_reset_done"),

    #link to password reset page
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name = "password_reset_confirm"),

    #Pwd changed successfully message
    path('password-reset-completed/', PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name = "password_reset_complete"),

]
