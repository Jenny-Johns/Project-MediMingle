from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import tbl_user, tbl_patient, tbl_doctor
from django.utils import timezone

@receiver(post_save, sender=tbl_user)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'patient':
            tbl_patient.objects.create(
                patient_name='',  # Add the default patient name here
                patient_contno=0,  # Add the default contact number here
                patient_email='',  # Add the default email here
                patient_gender='',  # Add the default gender here
                patient_add='',    # Add the default address here
                patient_age=0,     # Add the default age here
                patient_medhis='', # Add the default medical history here
                creation_date=timezone.now(),
                updation_date=timezone.now(),
            )
            
        elif instance.user_type == 'doctor':
            tbl_doctor.objects.create(
                firstname='',       # Add the default first name here
                lastname='',        # Add the default last name here
                dob=timezone.now(), # Add the default date of birth here
                email='',           # Add the default email here
                gender='',          # Add the default gender here
                phone=0,            # Add the default phone number here
                address='',         # Add the default address here
                qualification='',   # Add the default qualification here
                consultancy_fees=0, # Add the default consultancy fees here
                password='',        # Add the default password here
                user_status='',     # Add the default user status here
            )
