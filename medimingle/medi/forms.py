# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django import forms
from .models import Doctor, DoctorSpecialization, MedicalHistory, Qualification, Experience
from django import forms
from .models import Patient,tbl_user




class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, help_text="Required. 20 characters or fewer.")
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    phone = forms.CharField(max_length=10, min_length=10, required=True, help_text="Required. 10 digits, no alphabets.")
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        min_length=8,
        help_text="Required. Minimum 8 characters with at least one special character, one number, and one alphabet."
    )
    user_type=forms.CharField(required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone) != 10 or int(phone[0]) <= 6:
            raise ValidationError("Phone number must be 10 digits, contain no alphabets, and start with a digit greater than 6.")
        return phone

    def clean_password(self):
        password = self.cleaned_data['password']
        if not re.search(r'[!@#$%^&*(),.?":{}|<>0-9a-zA-Z]', password):
            raise ValidationError("Password must contain at least one special character.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least one alphabet character.")
        return password





class UserProfileUpdateForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    CITY_CHOICES = [
        ('Thiruvananthapuram','Thiruvananthapuram'),
        ('Kollam','Kollam'),
        ('Pathanamthitta','Pathanamthitta'),
        ('Alappuzha','Alappuzha'),
        ('Kottayam','Kottayam'),
        ('Idukki','Idukki'),
        ('Ernakulam','Ernakulam'),
        ('Thrissur','Thrissur'),
        ('Palakkad','Palakkad'),
        ('Malappuram','Malappuram'),
        ('Kozhikode','Kozhikode'),
        ('Wayanad','Wayanad'),
        ('Kannur','Kannur'),
        ('Kasargod','Kasargod'),

    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('AB+', 'AB+'),
        ('O+', 'O+'),
        ('A-', 'A-'),
        ('B-', 'B-'),
        ('AB-', 'AB-'),
        ('O-', 'O-'),
    ]
    city = forms.ChoiceField(label='City', choices=CITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    state = forms.CharField(label='State', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    pin = forms.CharField(label='PIN', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PIN'}))
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(label='Profile Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    blood_group = forms.ChoiceField(label='Blood Group', choices=BLOOD_GROUP_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    date_of_birth = forms.DateField(label='DOB', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'DOB'}))

    class Meta:
        model = Patient
        fields = ['city','state', 'country', 'pin', 'gender', 'profile_image', 'blood_group', 'address','date_of_birth']


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))

    class Meta:
        model = tbl_user
        fields = ['first_name', 'last_name', 'email', 'phone_number']




class DoctorForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    CITY_CHOICES = [
        ('Thiruvananthapuram','Thiruvananthapuram'),
        ('Kollam','Kollam'),
        ('Pathanamthitta','Pathanamthitta'),
        ('Alappuzha','Alappuzha'),
        ('Kottayam','Kottayam'),
        ('Idukki','Idukki'),
        ('Ernakulam','Ernakulam'),
        ('Thrissur','Thrissur'),
        ('Palakkad','Palakkad'),
        ('Malappuram','Malappuram'),
        ('Kozhikode','Kozhikode'),
        ('Wayanad','Wayanad'),
        ('Kannur','Kannur'),
        ('Kasargod','Kasargod'),

    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.ChoiceField(label='City', choices=CITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(label='Profile Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    registration_number=forms.CharField(label='Registration Number',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Registration Number'}))
    certificate=forms.FileField(label='Certificate',widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder':'Certificate'}))

    class Meta:
        model = Doctor
        fields = ['city', 'profile_image', 'gender', 'registration_number','certificate','description']
 
    
class DoctorSpecializationForm(forms.ModelForm):
    SPECIALIZATION_CHOICES = [
        ('Cardiologist', 'Cardiologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Orthopedic Surgeon', 'Orthopedic Surgeon'),
        ('Pediatrician','Pediatrician'),
        ('Gynecologist','Gynecologist'),
        ('Pulmonologist','Pulmonologist'),
        ('Psychiatrist','Psychiatrist'),
        ('Psychologist','Psychologist'),
        ('Ophthalmologist','Ophthalmologist'),
        ('Dentist','Dentist'),


    ]

    specialized_category = forms.ChoiceField(choices=SPECIALIZATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = DoctorSpecialization
        fields = ['specialized_category']


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['institution_name', 'qualification_degree', 'years_of_completion']
        widgets = {
            'institution_name': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification_degree': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_completion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['hospital_name', 'worked_from', 'worked_to', 'designation']
        widgets = {
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'worked_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'worked_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ConsultingFeeForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['consulting_fee']

class DoctorAddForm(forms.ModelForm):
    class Meta:
        model = tbl_user
        fields = ['email','first_name','last_name','phone_number','password']
    