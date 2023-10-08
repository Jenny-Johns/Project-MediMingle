from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import tbl_user,tbl_patient,tbl_doctor,tbl_specialty  # Import your custom user model

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')  # Customize the list display fields
    list_filter = ('is_staff', 'is_superuser')  # Add 'is_superuser' to the list filter

    # Override the get_queryset method to filter out superusers
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Exclude superusers from the queryset
        return queryset.exclude(is_superuser=True)

# Register your custom UserAdmin class with your custom user model
admin.site.register(tbl_user, CustomUserAdmin)
# Register the tbl_patient model
admin.site.register(tbl_patient)

# Register the tbl_doctor model
admin.site.register(tbl_doctor)
admin.site.register(tbl_specialty)