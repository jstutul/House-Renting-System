from django.urls import path
from App_Account.views import (
    SignupView, LoginView,activateView,DashboardView,LogoutView,PasswordChange,ProfileView,
    ProfileUpdateView,RentListView,AddRentView,RentEditView,RentDeleteView,PendingRentListView,
    PendingRentPreviewiew,ApprovePendingRentListView,CancelPendingRentListView,RentedListView,
    RentedListDetailsView
    )

app_name = 'App_Account'

urlpatterns = [
    path('signup/', SignupView, name='signup'),
    path('login/', LoginView, name='login'),
    path('logout',LogoutView,name='logout'),
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',activateView, name='activate'),
    path('password-change/',PasswordChange,name="passwordchange"),
    path('dashboard/',DashboardView,name='dashboard'),
    path('profile/',ProfileView,name='profile'),
    path('profileupdate/',ProfileUpdateView,name='profileupdate'),


    ################### House OWner Part #######################
    path('rent-list',RentListView,name='rentlist'),
    path('add-rent',AddRentView,name='addrent'),
    path('edit-rent/<int:id>',RentEditView,name='editrent'),
    path('delete-rent/<int:id>',RentDeleteView,name='rentdelete'),

    path('rented-list',RentedListView,name='rentedlist'),
    path('rented-details/<int:id>',RentedListDetailsView,name='renteddetails'),

    ################### Renter Part #######################
    path('pending-rent-list',PendingRentListView,name='pendingrentlist'),
    path('pending-rent-view/<int:id>',PendingRentPreviewiew,name='pendingrentpreview'),
    path('pending-rent-approved/<int:id>',ApprovePendingRentListView,name='approvependingrent'),
    path('pending-rent-cancel/<int:id>',CancelPendingRentListView,name='cancelpendingrent'),
]
