from django.contrib import admin
from django.contrib.auth.models import User
from .models import tbl_user,Doctor,Patient,Experience,DoctorSpecialization,Qualification,PrescriptionStatus,AppointmentTime

# Register your models here.
admin.site.register(tbl_user) 
admin.site.register(Doctor) 
admin.site.register(Patient)
admin.site.register(Experience)
admin.site.register(Qualification)
admin.site.register(PrescriptionStatus)
admin.site.register(DoctorSpecialization)
admin.site.register(AppointmentTime)
#admin.site.register()
