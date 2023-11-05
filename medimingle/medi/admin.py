from django.contrib import admin
from django.contrib.auth.models import User
from .models import tbl_user,Doctor,Patient

# Register your models here.
admin.site.register(tbl_user) 
admin.site.register(Doctor) 
admin.site.register(Patient)# Remove `, admin` from here
