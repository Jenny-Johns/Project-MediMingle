from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate
from django.contrib.auth import authenticate, login
from .models import Doctor, Patient, tbl_user
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User  # Assuming you are using the built-in User model



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
        return redirect('signin')
    else:
       return render(request,'register.html')
        
 

@never_cache
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username=="jenny" and password=="jenny123":
            return redirect("adminpage")
        else:
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


@never_cache
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')

def logout(request):
    auth.logout(request)
    return redirect('/')


def patient_dashboard(request):
    doc = tbl_user.objects.filter(user_type='doctor').exclude(is_superuser=True)
    context={
        "doc":doc
    }
    return render(request,'patient_dashboard.html',context)

def doctor_dashboard(request):
    pat=tbl_user.objects.filter(user_type='patient').exclude(is_superuser=True)
    pat_count=pat.count()
    context={
        "pat":pat,
        "pat_count":pat_count
    }
    return render(request,'doctor_dashboard.html',context)    

def homepage(request):
    return render(request,'homepage.html')
def patient_profile(request):
    return render(request,'patient_profile.html')

def profile_settings(request):
    return render(request,'profile_settings.html')

def doctor_profile_settings(request):
    return render(request,'doctor_profile_settings.html')

def adminpage(request):
    users=tbl_user.objects.exclude(is_superuser='1')
    doctors = tbl_user.objects.filter(user_type='doctor').exclude(is_superuser=True)
    patients = tbl_user.objects.filter(user_type='patient').exclude(is_superuser=True)
    user_count=users.count()
    doc_count=doctors.count()
    pat_count=patients.count()
    context = {
        "doctors": doctors,
        "patients": patients,
        "users":users,
        "user_count":user_count,
        "doc_count":doc_count,
        "pat_count":pat_count
    }
    
    
    return render(request,'adminpage.html',context)

def delete_user(request, user_id):
    user = tbl_user.objects.get(id=user_id)
    user.delete()
    return redirect('adminpage')


def block_user(request, user_id):
    user = tbl_user.objects.get(id=user_id)
    user.blocked = True
    user.save()
    return redirect('adminpage')


def unblock_user(request, user_id):
    user = tbl_user.objects.get(id=user_id)
    user.blocked = False
    user.save()
    return redirect('adminpage')

def forgot_password(request):
    return render(request,'forgot_password.html')

def patient_list(request):
    pat=tbl_user.objects.filter(user_type='patient').exclude(is_superuser=True)
    context={
        "pat":pat
    }
    return render(request,'patient_list.html',context)

def doctor_list(request):
    doc = tbl_user.objects.filter(user_type='doctor').exclude(is_superuser=True)
    context={
        "doc":doc
    }
    return render(request,'doctor_list.html',context)

def login_view(request):
    return render(request,'login_view.html')