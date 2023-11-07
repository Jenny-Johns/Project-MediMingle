from datetime import datetime
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
    city  = models.CharField(max_length=50,null=True,blank=True)
    profile_image = models.ImageField(upload_to='doctors/%Y/%m/%d/',default='default.png')
    gender = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    date_joined = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.user.first_name
    # Add fields specific to doctors, e.g., specialty, qualifications, etc.
class DoctorSpecialization(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    specialized_category  = models.CharField(max_length=50, null=True)
    
    
    def __str__(self):
        return self.specialized_category


class Qualification(models.Model):
    institution_name  = models.CharField(max_length=50, null=True)
    qualification_degree = models.CharField(max_length=50, null=True)
    years_of_completion = models.DateField(null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.institution_name

class Experience(models.Model):
    hospital_name = models.CharField(max_length=50, null=True)
    worked_from = models.DateField(null=True)
    worked_to = models.DateField(null=True)
    designation = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.hospital_name

class Patient(models.Model):
    user = models.OneToOneField(tbl_user, on_delete=models.CASCADE)
    
    profile_image = models.ImageField(null=True,blank=True)
    city  = models.CharField(max_length=100, null=True,blank=True)
    state  = models.CharField(max_length=100, null=True)
    country  = models.CharField(max_length=100, null=True)
    gender  = models.CharField(max_length=50, null=True)
    blood_group  = models.CharField(max_length=50, null=True)
    date_joined = models.DateTimeField(default=datetime.now, blank=True)
    date_of_birth = models.DateField(null=True)
    address=models.TextField(null=True)
    pin=models.CharField(max_length=6,null=True)

    def __str__(self):
        return self.user.first_name

class PrescriptionStatus(models.Model):
    is_uploaded= models.BooleanField(default=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    def __int__(self):
        return self.id
    # Add fields specific to patients, e.g., medical history, contact information, etc.
