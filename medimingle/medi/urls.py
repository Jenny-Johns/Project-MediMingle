
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name='home'),
    path('homepage/',views.homepage,name='homepage'),
    path('user_login/',views.user_login,name='signin'),
    path('register/',views.register,name='register'),
    path('user_logout/',views.user_logout, name='logout'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('doctor_register/',views.doctor_register,name='doctor_register'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('patient_profile/',views.patient_profile,name='patient_profile'),
    

]
