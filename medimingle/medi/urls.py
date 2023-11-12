
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    path('',views.index,name='home'),
    path('user_login/',views.user_login,name='signin'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout, name='logout'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    #path('homepage/patient_dashboard/',views.homepage,name='homepage'),
    #path('homepage/adminpage/',views.homepage,name='homepage'),
    #path('patient_dashboard/homepage/',views.homepage,name='homepage'),
    #path('doctor_dashboard/homepage/',views.homepage,name='homepage'),
    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('patient_profile/',views.patient_profile,name='patient_profile'),
    path('profile_settings/',views.profile_settings,name='profile_settings'),
    path('patient_dashboard/profile_settings/',views.profile_settings,name='profile_settings'),
    path('doctor_change_password/',views.doctor_change_password,name='doctor_change_password'),
    path('doctor_profile_settings/',views.doctor_profile_settings,name='doctor_profile_settings'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('patient_list',views.patient_list,name='patient_list'),
    path('doctor_list',views.doctor_list,name='doctor_list'),
    path('login_view',views.login_view,name='login_view'),
    path('patient_change_password/',views.patient_change_password,name='patient_change_password'),



   path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
   path('block_user/<int:user_id>/', views.block_user, name='block_user'),
   path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='signin.html')),
    path('accounts/profile/', auth_views.LoginView.as_view(template_name='patient_dashboard.html')),

    
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='reset_password'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),


]
