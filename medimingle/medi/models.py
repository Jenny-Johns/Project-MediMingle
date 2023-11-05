from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class tbl_user(AbstractUser):
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=15, null=True)
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),('doctor', 'Doctor'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='patient',  # You can set a default value if needed
    )
    #user_type = models.CharField(max_length=10,default='patient')  # Add a field for user type

    def __str__(self):
        return self.username

class Doctor(models.Model):
    user = models.OneToOneField(tbl_user, on_delete=models.CASCADE)
    # Add fields specific to doctors, e.g., specialty, qualifications, etc.

class Patient(models.Model):
    user = models.OneToOneField(tbl_user, on_delete=models.CASCADE)
    # Add fields specific to patients, e.g., medical history, contact information, etc.
