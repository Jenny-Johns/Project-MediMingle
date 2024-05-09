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
    profile_image = models.ImageField(upload_to='doctor/',default='patient8.jpg')
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

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    reason_for_consultation = models.TextField()
    previous_medical_condition = models.TextField()
    diabetic_patient = models.CharField(max_length=3, choices=(('Yes', 'Yes'), ('No', 'No')))
    def __str__(self):
        return f'Medical history of {self.patient.user.first_name}'

class AppointmentTime(models.Model):
    day = models.CharField(max_length=50, null=True)
    from_to = models.CharField(max_length=50, null=True) 
    appointment_date = models.DateField(null=True)
    month = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=50, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    is_booked=models.BooleanField(default=False)
    def __str__(self):
        return self.date

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_time_slot = models.ForeignKey(AppointmentTime, on_delete=models.CASCADE,null=True)
    appointment_datetime=models.CharField(max_length=50, null=True)
    appointment_time=models.CharField(max_length=50, null=True)
    is_confirmed = models.BooleanField(default=False)
    medical_data_added = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.doctor} - {self.appointment_time_slot.appointment_date}"
 
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

class MedicalData(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE,null=True)
    reason_for_consultation = models.TextField()
    previous_medical_condition = models.TextField()
    any_other_illness = models.TextField()
    def __str__(self):
        return f'Medical data for {self.patient.user.first_name}'

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    medicine_name = models.CharField(max_length=100)
    intake_time_choices = [
        ('0-0-1', '0-0-1'),
        ('1-1-1', '1-1-1'),
        ('1-0-0', '1-0-0'),
        ('0-1-0', '0-1-0'),
        ('1-1-0', '1-1-0'),
        ('1-0-1', '1-0-1'),
    ]
    intake_time = models.CharField(max_length=10, choices=intake_time_choices)
    days = models.PositiveIntegerField()
    prescription_added_date = models.DateTimeField(auto_now_add=True)
    prescription_text = models.TextField(blank=True, null=True)
    is_uploaded = models.BooleanField(default=False)
    def __str__(self):
        return f"Prescription for {self.patient} by Dr. {self.doctor}"

class DoctorRating(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')))
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Rating of {self.doctor} by {self.patient}"
    