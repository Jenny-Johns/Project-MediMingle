from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth

from django.contrib import messages
from .forms import UserRegistrationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Create your views here.
def index(request):
    return render(request,'index.html')

#def login(request):
    #return render(request,'login.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Login")
            return redirect('login')

    return render(request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
        
        #if user is not None:
            #auth.login(request, user)
           # current_user = Account.objects.get(id=request.user.id)
            

    
def register(request):
    if request.method =="POST":
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        user_type=request.POST['user_type']
        user=User.objects.create_user(firstname=firstname,lastname=lastname,email=email,password=password)
        user.user_type = user_type
        user.phone=phone
        user.save();
        messages.success(request, 'You are now registered and can log in')
        return redirect('login')
        #return redirect("login.html")
    else:
        return render(request,'register.html')
        
# views.py





def patient_dashboard(request):
    current_user = request.user
    context = {
        'patient':current_user
    }
    return render(request,'users/patient_dashboard.html', context)    


