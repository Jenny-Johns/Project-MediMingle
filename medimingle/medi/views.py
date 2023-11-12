from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate
from django.contrib.auth import authenticate, login
from .models import Doctor, Patient, tbl_user
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User  
from django.contrib.auth.decorators import login_required
from .forms import UserProfileUpdateForm,ProfileUpdateForm
from .forms import  DoctorSpecializationForm, QualificationForm, ExperienceForm,DoctorForm
from django.views.decorators.http import require_POST


# Create your views here.
def index(request):
    return render(request,'index.html')

@never_cache   
def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
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
            messages.add_message(request,messages.SUCCESS,f"Welcome {first_name}, You are now registered and can login")
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
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password = password)
            if user is not None and user.is_active:
                login(request, user)
                request.session['username'] = user.username
                if user.is_superuser:
                    return redirect('adminpage')
                elif user.user_type == 'doctor':
                    return redirect('doctor_dashboard')
                else:
                    return redirect('patient_dashboard')
            elif user is not None and not user.is_active:
                messages.error(request, "Your account is inactive and you can't login")
                return redirect('signin')
            else:
                messages.info(request,"Username or Password is incorrect")
                return redirect('signin')
        response = render(request,"signin.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response


@never_cache
@login_required(login_url='signin')
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('signin')
    
@never_cache
@login_required(login_url='signin')
def logout(request):
    logout(request)
    return redirect('signin')

@never_cache   
@login_required(login_url='signin')
def patient_dashboard(request):
    doc = tbl_user.objects.filter(user_type='doctor').exclude(is_superuser=True)
    context={
        "doc":doc
    }
    return render(request,'patient_dashboard.html',context)

@never_cache   
@login_required(login_url='signin')
def doctor_dashboard(request):
    pat=tbl_user.objects.filter(user_type='patient').exclude(is_superuser=True)
    pat_count=pat.count()
    context={
        "pat":pat,
        "pat_count":pat_count
    }
    return render(request,'doctor_dashboard.html',context) 

@never_cache   
@login_required(login_url='signin')
def homepage(request):
    doct = tbl_user.objects.filter(user_type='doctor').exclude(is_superuser=True)
    context={
        "doct":doct
    }
    return render(request,'homepage.html',context)


@never_cache   
@login_required(login_url='signin')
def patient_profile(request):
    return render(request,'patient_profile.html')


@never_cache   
@login_required(login_url='signin')
def profile_settings(request):
    user = request.user  # Get the logged-in user
    try:
        patient_data = Patient.objects.get(user=user)
    except Patient.DoesNotExist:
        patient_data = None

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user)
        patient_form = UserProfileUpdateForm(request.POST, instance=patient_data)

        if user_form.is_valid():
            # Update the Patient model fields
            user_form.save()
            patient_form.save()
            messages.success(request,"Profile Updated")
            return redirect('patient_dashboard')  # Redirect back to the profile update page or another page
    else:
        user_form = ProfileUpdateForm(instance=user)
        patient_form = UserProfileUpdateForm(instance=patient_data)
    return render(request, 'profile_settings.html', {'user_form': user_form,'patient_form':patient_form})




@never_cache   
@login_required(login_url='signin')
# views.py
def doctor_profile_settings(request):
    user = request.user  # Get the logged-in user
    try:
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        doctor = None
    
    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        specialization_form = DoctorSpecializationForm(request.POST, instance=doctor.doctorspecialization_set.first())
        qualification_form = QualificationForm(request.POST, instance=doctor.qualification_set.first())
        experience_form = ExperienceForm(request.POST, instance=doctor.experience_set.first())

        if user_form.is_valid() and doctor_form.is_valid() and specialization_form.is_valid() and qualification_form.is_valid() and experience_form.is_valid():
            user_form.save()
            doctor_form.save()
            doctorspecialization = specialization_form.save(commit=False)
            doctorspecialization.doctor = doctor
            specialization_form.save()
            qualification = qualification_form.save(commit=False)
            qualification.doctor = doctor
            qualification.save()
            experience = experience_form.save(commit=False)
            experience.doctor = doctor
            experience.save()
            messages.success(request,"Profile Updated")           
            return redirect('doctor_dashboard')

    else:
        user_form = ProfileUpdateForm(instance=user)
        doctor_form = DoctorForm(instance=doctor)
        specialization_form = DoctorSpecializationForm(instance=doctor.doctorspecialization_set.first())
        qualification_form = QualificationForm(instance=doctor.qualification_set.first())
        experience_form = ExperienceForm(instance=doctor.experience_set.first())

    return render(request, 'doctor_profile_settings.html', {'user_form': user_form, 'doctor_form': doctor_form, 'specialization_form': specialization_form, 'qualification_form': qualification_form, 'experience_form': experience_form})


@never_cache
@login_required(login_url='signin')
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



@never_cache
@login_required(login_url='signin')
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



@never_cache
@login_required(login_url='signin')
def patient_list(request):
    pat=tbl_user.objects.filter(user_type='patient').exclude(is_superuser=True)
    context={
        "pat":pat
    }
    return render(request,'patient_list.html',context)



@never_cache
@login_required(login_url='signin')
def doctor_list(request):
    doc = tbl_user.objects.filter(user_type='doctor').exclude(is_superuser=True)
    context={
        "doc":doc
    }
    return render(request,'doctor_list.html',context)

def login_view(request):
    return render(request,'login_view.html')



@require_POST
def deactivate_user(request, user_id):
    user = get_object_or_404(tbl_user, id=user_id)
    user.is_active = False
    user.save()
    return redirect('adminpage')

@require_POST
def activate_user(request, user_id):
    user = get_object_or_404(tbl_user, id=user_id)
    user.is_active = True
    user.save()
    return redirect('adminpage')

@never_cache
@login_required
def doctor_change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('doctor_change_password')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('doctor_change_password')

        request.user.set_password(new_password)
        request.user.save()

        messages.success(request, 'Password changed successfully. Please login with your new password.')
        return redirect('signin')

    return render(request, 'doctor_change_password.html')




@never_cache
@login_required
def patient_change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('patient_change_password')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('patient_change_password')

        request.user.set_password(new_password)
        request.user.save()

        messages.success(request, 'Password changed successfully. Please login with your new password.')
        return redirect('signin')

    return render(request, 'patient_change_password.html')