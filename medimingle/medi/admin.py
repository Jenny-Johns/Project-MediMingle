from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Account,tbl_patient,tbl_doctor,tbl_qualification,tbl_experience,tbl_appointment,tbl_speciality,tbl_appointmentTime,tbl_prescriptionStatus # Import your custom user model

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    # Override the get_queryset method to filter out superusers
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Exclude superusers from the queryset
        return queryset.exclude(is_superuser=True)



# Register your custom UserAdmin class with your custom user model
admin.site.register(Account,AccountAdmin)
# Register the tbl_patient model
admin.site.register(tbl_patient)

# Register the tbl_doctor model
admin.site.register(tbl_doctor)
admin.site.register(tbl_speciality)
admin.site.register(tbl_qualification)
admin.site.register(tbl_experience)
admin.site.register(tbl_appointment)
# admin.site.register(tbl_login)
admin.site.register(tbl_prescriptionStatus)
admin.site.register(tbl_appointmentTime)
