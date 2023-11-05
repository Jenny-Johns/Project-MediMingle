from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate
from .models import Account,tbl_appointment,tbl_appointmentTime,tbl_doctor,tbl_experience,tbl_patient,tbl_prescriptionStatus,tbl_qualification,tbl_speciality
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views
def index(request):
    return render(request,'index.html')
    
def register(request):
    if request.method =="POST":
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        password=request.POST['password']
        user_type=request.POST['user_type']
        user=Account.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email)
        user.user_type = user_type

        user.phone_number = phone_number
        user.set_password(password)
        user.save()

        messages.success(request, 'You are now registered and can log in')
        return redirect('signin')
        
    else:
       return render(request,'register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email=email, password = password)
        
        if user is not None:
            auth.login(request, user)
            current_user=Account.objects.get(id=request.user.id)
            
            if user.is_superuser:
                return redirect('homepage')
            
            elif user.user_type == 'doctor':
                doctor_exists =tbl_doctor.objects.filter(user=current_user)
                if doctor_exists:
                    return redirect('doctor_dashboard')
                else:
                    doctor = tbl_doctor(user=current_user)
                    doctor.save
                    return redirect('doctor_dashboard')
            else:
                patient_exists = tbl_patient.objects.filter(user=current_user)
                if patient_exists:
                    return redirect('patient_dashboard')
                else:
                    patient = tbl_patient(user=current_user)
                    patient.save()
                    return redirect('patient_dashboard')
        else:
            messages.success(request, 'Invalid Credentials')
            return redirect('signin')

    return render(request, 'signin.html')

@login_required(login_url='login')
def user_logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('home')

def patient_dashboard(request):
    return render(request,'patient_dashboard.html')

def doctor_dashboard(request):
    return render(request,'doctor_dashboard.html')    

def doctor_register(request):
    return render(request,'doctor_register.html')

def homepage(request):
    return render(request,'homepage.html')

def patient_profile(request):
    return render(request,'patient_profile.html')

def forgot_password(request):
    return render(request,'forgot_password.html')