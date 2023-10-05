
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name='home'),
    path('patient_login/',views.patient_login,name='signin'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout, name='logout'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('doctor_register/',views.doctor_register,name='doctor_register'),

]
