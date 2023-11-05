
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name='home'),
    path('user_login/',views.user_login,name='signin'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout, name='logout'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('homepage/',views.homepage,name='homepage'),
    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('patient_profile/',views.patient_profile,name='patient_profile'),
    path('profile_settings/',views.profile_settings,name='profile_settings'),
    path('doctor_profile_settings/',views.doctor_profile_settings,name='doctor_profile_settings'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('admin_login/',views.admin_login,name='admin_login'),
    

]
