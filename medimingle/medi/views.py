from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate
from .models import tbl_user
from django.contrib import messages
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
        password=request.POST['password']
        user_type=request.POST['user_type']
        user=tbl_user(username=username,first_name=first_name,last_name=last_name,email=email,user_type=user_type)
        user.set_password(password)
        user.save()

        messages.success(request, 'You are now registered and can log in')
        return redirect('signin')
        
    else:
       return render(request,'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('homepage')
            elif user.user_type == 'doctor':
                return redirect('homepage')
            else:
                return redirect('homepage')
        else:
            return redirect('signin')

    return render(request, 'signin.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
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