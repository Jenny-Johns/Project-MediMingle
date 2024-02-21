from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class tbl_user(AbstractUser):
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=15, null=True)
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),('doctor', 'Doctor'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='patient',  
    )
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    status= models.BooleanField(default=False)
    # username = models.CharField(max_length=150, unique=False, blank=True)

    def __str__(self):
        return self.email

class Doctor(models.Model):
    user = models.OneToOneField(tbl_user, on_delete=models.CASCADE)
    city  = models.CharField(max_length=50,null=True,blank=True)
    profile_image = models.ImageField(upload_to='doctor/',default='default.png')
    gender = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    date_joined = models.DateTimeField(default=datetime.now, blank=True)
    consulting_fee = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    registration_number = models.CharField(max_length=50, null=True, blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)
    def __str__(self):
        return self.user.first_name
    


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
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.hospital_name



class Patient(models.Model):
    user = models.OneToOneField(tbl_user, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='patient/',default='default.png')
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


    


class MedicalRecords(models.Model):
    medical_insurance =  models.FileField(upload_to='insurance/%Y/% m/% d/')
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        verbose_name_plural = "MedicalRecords"

    def __str__(self):
        return self.patient.user.first_name


class MedicalHistory(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    reason =  models.CharField(max_length=200, blank=True)
    ever_had = models.CharField(max_length=200,blank=True)
    
    weight = models.CharField(max_length=20, null=True)
    age = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=20, null=True)
    blood_group  = models.CharField(max_length=50, null=True)
    previous_operation = models.CharField(max_length=200,blank=True)
    current_medication = models.CharField(max_length=200,blank=True)
    other_illness = models.CharField(max_length=200,blank=True)
    other_information = models.CharField(max_length=200,blank=True)
    is_processing = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now, blank=True)

    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name_plural = "MedicalHistories"



class Prescription(models.Model):
    name =  models.CharField(max_length=50, null=True)
    quantity  = models.CharField(max_length=50, null=True)
    days = models.CharField(max_length=50, null=True)
    morning = models.CharField(max_length=10, null=True)
    afternoon = models.CharField(max_length=10, null=True)
    evening = models.CharField(max_length=10, null=True)
    night = models.CharField(max_length=10, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)
    uploaded_date = models.DateTimeField(default=datetime.now, blank=True)
    




class AppointmentTime(models.Model):
    day = models.CharField(max_length=50, null=True)
    time_from = models.CharField(max_length=50, null=True)
    time_to = models.CharField(max_length=50, null=True)
    from_to = models.CharField(max_length=50, null=True)
    appointment_date = models.DateField(null=True)
    month = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=50, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.day

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_datetime = models.CharField(max_length=20,null=True)
    is_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.appointment_datetime
    
class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.timestamp
    



class Billing(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    is_bill_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Billing for {self.doctor} by {self.patient}"
    
# class Payment(models.Model):
#     billing = models.ForeignKey(Billing, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField(auto_now_add=True)

    