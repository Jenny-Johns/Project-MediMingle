# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django import forms
from .models import Doctor, DoctorSpecialization, Qualification, Experience
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
    class Meta:
        model = Patient
        fields = ['city','country','pin','gender','profile_image','blood_group','address']

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = tbl_user
        fields = ['first_name','last_name','email','phone_number']
    widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }




"""class UserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = tbl_user
        fields = ['first_name', 'last_name', 'email', 'phone_number']"""


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['city', 'profile_image', 'gender', 'description'] 
    
class DoctorSpecializationForm(forms.ModelForm):
    class Meta:
        model = DoctorSpecialization
        fields = ['specialized_category']

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['institution_name', 'qualification_degree', 'years_of_completion']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['hospital_name', 'worked_from', 'worked_to', 'designation']
