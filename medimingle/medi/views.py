from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate
from .models import Doctor, Patient, tbl_user
from django.contrib import messages
from django.views.decorators.cache import never_cache


# Create your views here.
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
        user=tbl_user(username=username,first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,user_type=user_type)
        user.set_password(password)
        user.user_type = user_type
        user.phone_number = phone_number
        user.save();
        if user_type=='doctor':
            doctor=Doctor(user=user)
            doctor.save()
        else:
            patient=Patient(user=user)
            patient.save()
        messages.success(request, 'You are now registered and can log in')
        return redirect('signin')
    else:
       return render(request,'register.html')
        
    
    
# views.py


@never_cache
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            return redirect('signin')
    response = render(request,"signin.html")
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response

def admin_login(request):
    return render(request,'adminpage.html')
@never_cache
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')

def logout(request):
    auth.logout(request)
    return redirect('/')


def patient_dashboard(request):
    return render(request,'patient_dashboard.html')

def doctor_dashboard(request):
    return render(request,'doctor_dashboard.html')    

def homepage(request):
    return render(request,'homepage.html')
def patient_profile(request):
    return render(request,'patient_profile.html')

def profile_settings(request):
    return render(request,'profile_settings.html')

def doctor_profile_settings(request):
    return render(request,'doctor_profile_settings.html')

def adminpage(request):
    return render(request,'adminpage.html')

def forgot_password(request):
    return render(request,'forgot_password.html')
