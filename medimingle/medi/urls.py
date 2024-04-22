
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views 
from .views import activate_account
from .views import update_consulting_fee


urlpatterns = [
    path('',views.index,name='home'),
    path('user_login/',views.user_login,name='signin'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout, name='logout'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('homepage/',views.homepage,name='homepage'),
    #path('homepage/adminpage/',views.homepage,name='homepage'),
    #path('patient_dashboard/homepage/',views.homepage,name='homepage'),
    #path('doctor_dashboard/homepage/',views.homepage,name='homepage'),

    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    # path('doctor_specialization/',views.doctor_specialization, name='doctor_specialization'),
    # path('history/', views.history, name='history'),
    path('doctors/',views.doctors, name='doctors'),
    path('doctors/<int:doctor_id>/', views.view_doctor_profile, name='doctor_profile'),
    path('profile/<int:doctor_id>/', views.profile, name='profile'),
    path('booking/<int:doctor_id>/', views.booking, name='booking'),
    path('doctor_search/', views.doctor_search, name='doctor_search'),
    path('schedule_timings',views.schedule_timings,name='schedule_timings'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('patient_profile/',views.patient_profile,name='patient_profile'),
    path('profile_settings/',views.profile_settings,name='profile_settings'),
    path('patient_dashboard/profile_settings/',views.profile_settings,name='profile_settings'),
    path('doctor_change_password/',views.doctor_change_password,name='doctor_change_password'),
    path('doctor_profile_settings/',views.doctor_profile_settings,name='doctor_profile_settings'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('patient_list',views.patient_list,name='patient_list'),
    path('doctor_list',views.doctor_list,name='doctor_list'),
    path('appointment_list',views.appointment_list,name='appointment_list'),

    path('total_user_list',views.total_user_list,name='total_user_list'),
    # path('login_view',views.login_view,name='login_view'),
    path('patient_change_password/',views.patient_change_password,name='patient_change_password'),
    # path('slot_select/<int:doctor_id>/', views.slot_select, name='slot_select'),
    path('doctor/<int:doctor_id>/', views.view_doctor_details, name='view_doctor_details'),
    path('pat_doc_view/<int:doctor_id>/', views.pat_doc_view, name='pat_doc_view'),
    path('pat_doc_view_home/<int:doctor_id>/', views.pat_doc_view, name='pat_doc_view_home'),
    path('view_slot',views.view_slot,name='view_slot'),
    path('delete_slot/<int:slot_id>/', views.delete_slot, name='delete_slot'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='account_activation'),
    path('update_consulting_fee/<int:user_id>/', views.update_consulting_fee, name='update_consulting_fee'),
path('reschedule_appointment/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),

    path('success',views.success,name='success'),
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
    path('deactivate_user_pat/<int:user_id>/', views.deactivate_user_pat, name='deactivate_user_pat'),
    path('activate_user_pat/<int:user_id>/', views.activate_user_pat, name='activate_user_pat'),

    path('doc_suggest/',views.doc_suggest,name="doc_suggest"),
    path('doc_suggest2/',views.doc_suggest2,name="doc_suggest2"),

     path('add_doctor/', views.add_doctor, name='add_doctor'),


    path('confirm_booking/<int:doctor_id>/', views.confirm_booking, name='confirm_booking'),
    path('confirm_appointment/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),

    path('view_due_details/', views.view_due_details, name='view_due_details'),
    path('make_payment/<int:billing_id>/', views.make_payment, name='make_payment'),

    path('generate-receipt/<int:bill_id>/', views.generate_receipt, name='generate_receipt'),
    path('generate-receipt/', views.generate_receipt, name='generate_receipt'),
    path('generate-receipt-pdf/<int:bill_id>/', views.generate_receipt_pdf, name='generate_receipt_pdf'),
    path('edit_slot/<int:slot_id>/', views.edit_slot, name='edit_slot'),
    path('delete_slot/<int:slot_id>/', views.delete_slot, name='delete_slot'),
    path('my_doctors/', views.my_doctors, name='my_doctors'),
    path('medical_data/', views.medical_data, name='medical_data'),
    path('patients/<int:patient_id>/', views.patient_details, name='patient_details'),
path('add_medical_data/', views.add_medical_data, name='add_medical_data'),

path('add_medical_data/<int:appointment_id>/', views.add_medical_data, name='add_medical_data'),
    path('view_medical_data/<int:appointment_id>/', views.view_medical_data, name='view_medical_data'),
   path('view_medical_history/', views.view_medical_history, name='view_medical_history'),
   
path('my_patients/', views.my_patients, name='my_patients'),

    # path('add_prescription/<int:appointment_id>/', views.add_prescription, name='add_prescription'),
    # path('view_prescription/<int:appointment_id>/', views.view_prescription, name='view_prescription'),
    # path('edit_prescription/<int:prescription_id>/', views.edit_prescription, name='edit_prescription'),
    # path('add_prescription/<int:patient_id>/', views.add_prescription, name='add_prescription'),

path('add_prescription/<int:patient_id>/<int:appointment_id>/', views.add_prescription, name='add_prescription'),
    path('view_prescription/<int:patient_id>/', views.view_prescription, name='view_prescription'),
path('view_prescriptions/<int:doctor_id>/', views.view_prescriptions, name='view_prescriptions'),
path('add_rating/<int:doctor_id>/', views.add_rating, name='add_rating'),
]
