from django.contrib import admin
from django.urls import path,include
from HouseRental.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name='home'),
    path('reset-password/',
         PasswordResetView.as_view(template_name='App_Account/password_reset_form.html'), name='password_reset'),
    path('reset-password/done/',
         PasswordResetDoneView.as_view(template_name='App_Account/password_reset_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='App_Account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='App_Account/password_reset_complete.html'),
         name='password_reset_complete'),
    path('account/',include('App_Account.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
