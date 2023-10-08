"""from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class tbl_user(AbstractUser):
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.username
class custom_admin(AbstractUser):
    pass"""


from django.contrib.auth.models import AbstractUser
from django.db import models

class tbl_user(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

    # User type choices
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='patient',  # You can set a default value if needed
    )

class tbl_specialty(models.Model):
    spec_id = models.AutoField(primary_key=True)
    spec_name = models.CharField(max_length=100)
    spec_status = models.IntegerField()

    def __str__(self):
        return self.spec_name

class tbl_doctor(models.Model):
    doc_id = models.AutoField(primary_key=True)
    #login_id = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    #spec_id = models.ForeignKey(tbl_specialty, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField()
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')],null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    qualification = models.CharField(max_length=100,null=True, blank=True)
    consultancy_fees = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=50)
    user_status = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class tbl_patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    #doc_id = models.ForeignKey(tbl_doctor, on_delete=models.CASCADE)
    #login_id = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=50)
    patient_contno = models.IntegerField(null=True, blank=True)
    patient_email = models.EmailField()
    patient_gender = models.CharField(max_length=6,null=True, blank=True)
    patient_add = models.TextField(null=True, blank=True)
    patient_age = models.IntegerField(null=True, blank=True)
    patient_medhis = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    updation_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.patient_name

    


