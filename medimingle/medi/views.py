from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate
from .models import tbl_user
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')
    
def register(request):
    if request.method =="POST":
        username=request.POST['username']
        #name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        user=tbl_user(username=username,email=email)
        user.set_password(password)
        user.save();
        messages.success(request, 'You are now registered and can log in')
        return redirect('signin')
    else:
       return render(request,'register.html')
        #user_type=request.POST['user_type']
        #username = email.split("@")[0]
        
        #user.user_type = user_type
        
        #login(request, username)
        
        #return redirect("login.html")
    
    
# views.py


def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            #print(user)
            login(request, user)
            return redirect('patient_dashboard')
        else:
            #messages.info(request,"Invalid Login")
            return redirect('signin')

    return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def patient_dashboard(request):
    return render(request,'patient_dashboard.html')    

def doctor_register(request):
    return render(request,'doctor_register.html')
