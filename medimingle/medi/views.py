import datetime
from tkinter import Canvas
from django.http import FileResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import Doctor, Patient, QuestionnaireResponse, tbl_user, AppointmentTime,DoctorSpecialization,MedicalHistory,Qualification,Experience,Appointment,Notification,Billing
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User  
from django.contrib.auth.decorators import login_required
from .forms import UserProfileUpdateForm,ProfileUpdateForm,ConsultingFeeForm
from .forms import  DoctorSpecializationForm, QualificationForm, ExperienceForm,DoctorForm,MedicalHistoryForm
from django.views.decorators.http import require_POST
from .choices import category, fromTimeChoice,toTimeChoice
from django.utils import timezone
from datetime import datetime
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string

# for pdf
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from easy_pdf.views import PDFTemplateView
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa
from django.http import HttpResponse


# for email verification
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from medi.tokens import account_activation_token
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from medi.tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import get_list_or_404
import razorpay
from datetime import datetime, timedelta
from django.utils.timezone import now


from django.db.models import Count
from datetime import date



from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.shortcuts import render, redirect
from .models import Appointment

from django.core.mail import send_mail
from django.utils.html import strip_tags


from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import Doctor
import random
import string

# views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import tbl_user, Doctor
from django.db import models
from django.db.models import Q
import secrets
import string
# Create your views here.

from django.db.models import Q
from django.shortcuts import render
from .models import Doctor

def index(request):
    if request.method == 'POST':
        query = request.POST.get('search_query')

        if query:
            doctors = Doctor.objects.filter(
                Q(user__first_name__icontains=query) | Q(user__email__icontains=query) |
                Q(city__icontains=query) | Q(gender__icontains=query) |
                Q(consulting_fee__icontains=query) | Q(doctorspecialization__specialized_category__icontains=query)
            )

            if doctors.exists():
                context = {'doctors': doctors, 'search_performed': True}
            else:
                context = {'no_record_message': 'No records found.', 'search_performed': True}
        else:
            # If the search query is empty, don't perform the search and don't show the message
            context = {'search_performed': False}
    else:
        # For GET requests, simply render the template without any context
        context = {'search_performed': False}

    return render(request, 'index.html', context)



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
            
            # Create tbl_user instance
            user = tbl_user.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, user_type=user_type)
            user.set_password(password)
            user.save()
            
            # Check if the user is registering as a doctor
            if user_type == 'doctor':
                # Create Doctor instance
                doctor = Doctor.objects.create(user=user)
            else:
                patient=Patient.objects.create(user=user)

            # user=tbl_user(username=username,first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,user_type=user_type)
            # user.set_password(password)
            # user.user_type = user_type
            # user.phone_number = phone_number
            # user.save();
            current_site = get_current_site(request)
            activation_link = f"{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}/"
            print(activation_link)

            # Send activation email
            subject = 'Activate Your Medimingle Account'
            message = f'Hi {user.first_name},\n\nClick the link below to activate your account:\n\n{activation_link}\n\nBest regards,\nThe Medimingle Team'
            send_mail(subject, message, 'medimingle@gmail.com', [user.email])
            messages.success(request, "You have registered successfully. Verify your email and login.")
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
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_active:
                    if user.is_superuser:
                        login(request, user)
                        request.session['username'] = user.username
                        return redirect('adminpage')

                    if user.is_email_verified:
                        login(request, user)
                        request.session['username'] = user.username
                        if user.user_type == 'doctor':
                            return redirect('doctor_dashboard')
                        else:
                            if user.user_type == 'patient':
                                return redirect('patient_dashboard')
                    else:
                        messages.warning(request, "Email not verified. Please verify your email and login.")
                else:
                    messages.error(request, "Admin has blocked your account.")
            else:
                messages.info(request, "Invalid Credentials")

        return render(request, "signin.html")


@never_cache
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        # Log the user in after email verification if needed
        # login(request, user)
        return redirect('signin')
    else:
        return redirect('activation_failed')
    

@never_cache
@login_required(login_url='signin')
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    
@never_cache
@login_required(login_url='signin')
def logout(request):
    logout(request)
    return redirect('index')

@never_cache   
@login_required(login_url='signin')
def patient_dashboard(request):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)
    appointments = Appointment.objects.filter(patient=request.user.patient)
    doc = tbl_user.objects.filter(user_type='doctor').exclude(is_superuser=True)
    notifications = Notification.objects.filter(patient=current_patient)
    n_count=notifications.count()
    bill=Billing.objects.filter(patient=current_patient)

    context={
        'patient': current_patient,
        'appointments':appointments,
        'n_count':n_count,
        'notifications': notifications,
        'doc':doc,
        'bill':bill

    }
    

    return render(request,'patient_dashboard.html',context)

@never_cache   
@login_required(login_url='signin')
# def doctor_dashboard(request):
#     current_user = request.user
#     current_doctor = get_object_or_404(Doctor, user=current_user)
#     specialization = DoctorSpecialization.objects.filter(doctor=current_doctor)
#     doctor_appointments = Appointment.objects.filter(doctor=request.user.doctor)
#     notifications = Notification.objects.filter(doctor=current_doctor)
#     n_count=notifications.count()
#     doctor_appointments = Appointment.objects.filter(doctor=current_doctor)
#     pat=tbl_user.objects.filter(user_type='patient').exclude(is_superuser=True)
#     pat_count=pat.count()
#     context={
#         "pat":pat,
#         "pat_count":pat_count,
#         "doctor": current_doctor,
#         'specialization':specialization,
#         'appointments': doctor_appointments,
#         'notifications': notifications,
#         "n_count":n_count

#     }
    
#     return render(request,'doctor_dashboard.html',context) 


def doctor_dashboard(request):
    current_user = request.user
    current_doctor = get_object_or_404(Doctor, user=current_user)
    specialization = DoctorSpecialization.objects.filter(doctor=current_doctor)
    
    # Fetch appointments from Appointment model related to the current doctor
    doctor_appointments = Appointment.objects.filter(doctor=current_doctor)
    
    notifications = Notification.objects.filter(doctor=current_doctor)
    n_count = notifications.count()

    pat = tbl_user.objects.filter(user_type='patient').exclude(is_superuser=True)
    pat_count = pat.count()

    context = {
        "pat": pat,
        "pat_count": pat_count,
        "doctor": current_doctor,
        'specialization': specialization,
        'appointments': doctor_appointments,
        'notifications': notifications,
        "n_count": n_count
    }
    
    return render(request, 'doctor_dashboard.html', context)


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
def doctors(request):
    doctors = Doctor.objects.all()

    context = {
        'doctors':doctors,
    }
    return render(request, 'doctors.html', context)

@never_cache   
@login_required(login_url='signin')
def patient_profile(request):
    return render(request,'patient_profile.html')


@never_cache   
@login_required(login_url='signin')
def profile_settings(request):
    user = request.user  # Get the logged-in user
    patient, created = Patient.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user)
        patient_form = UserProfileUpdateForm(request.POST, request.FILES, instance=patient)

        if user_form.is_valid() and patient_form.is_valid():
            user_form.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            messages.success(request, "Profile Updated")
            return redirect('profile_settings')  # Redirect back to the profile update page or another page
    else:
        user_form = ProfileUpdateForm(instance=user)
        patient_form = UserProfileUpdateForm(instance=patient)

    return render(request, 'profile_settings.html', {'user_form': user_form, 'patient_form': patient_form})

@never_cache   
@login_required(login_url='signin')
def doctor_profile_settings(request):
    user = request.user  
    doctor, created = Doctor.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        specialization_form = DoctorSpecializationForm(request.POST, instance=doctor.doctorspecialization_set.first())
        qualification_form = QualificationForm(request.POST, instance=doctor.qualification_set.first())
        experience_form = ExperienceForm(request.POST, instance=doctor.experience_set.first())

        if user_form.is_valid() and doctor_form.is_valid() and specialization_form.is_valid() and qualification_form.is_valid() and experience_form.is_valid():
            user_form.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            specialization = specialization_form.save(commit=False)
            specialization.doctor = doctor
            specialization.save()

            qualification = qualification_form.save(commit=False)
            qualification.doctor = doctor
            qualification.save()

            experience = experience_form.save(commit=False)
            experience.doctor = doctor
            experience.save()

            messages.success(request, "Profile Updated")
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
    appointment=Appointment.objects.all()
    user_count=users.count()
    doc_count=doctors.count()
    pat_count=patients.count()
    appoint_count=appointment.count()
    context = {
        "doctors": doctors,
        "patients": patients,
        "users":users,
        "user_count":user_count,
        "doc_count":doc_count,
        "pat_count":pat_count,
        "appoint_count":appoint_count
    }
    
    return render(request,'adminpage.html',context)

@never_cache
@login_required(login_url='signin')
def approve_doctor(request, doctor_id, status):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to perform this action.")

    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.status = status
    doctor.save()

    return redirect('doctor_list')


@never_cache
@login_required(login_url='signin')
def delete_user(request, user_id):
    user = tbl_user.objects.get(id=user_id)
    user.delete()
    return redirect('adminpage')

@never_cache
@login_required(login_url='signin')
def block_user(request, user_id):
    user = tbl_user.objects.get(id=user_id)
    user.blocked = True
    user.save()
    return redirect('adminpage')

@never_cache
@login_required(login_url='signin')
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
        "doc":doc,
    }
    return render(request,'doctor_list.html',context)


@never_cache
@login_required(login_url='signin')
def total_user_list(request):
    users = tbl_user.objects.exclude(is_superuser=True)
    context={
        "users":users
    }
    return render(request,'total_user_list.html',context)


@never_cache
@login_required(login_url='signin')
def appointment_list(request):
    users = Appointment.objects.all()
    context={
        "users":users
    }
    return render(request,'appointment_list.html',context)







@never_cache
@login_required(login_url='signin')
@require_POST
def deactivate_user(request, user_id):
    user = get_object_or_404(tbl_user, id=user_id)
    user.is_active = False
    user.save()
    return redirect('doctor_list')


@never_cache
@login_required(login_url='signin')
@require_POST
def activate_user(request, user_id):
    user = get_object_or_404(tbl_user, id=user_id)
    user.is_active = True
    user.save()
    return redirect('doctor_list')



@never_cache
@login_required(login_url='signin')
@require_POST
def deactivate_user_pat(request, user_id):
    user = get_object_or_404(tbl_user, id=user_id)
    user.is_active = False
    user.save()
    return redirect('patient_list')


@never_cache
@login_required(login_url='signin')
@require_POST
def activate_user_pat(request, user_id):
    user = get_object_or_404(tbl_user, id=user_id)
    user.is_active = True
    user.save()
    return redirect('patient_list')





@never_cache
@login_required(login_url='signin')
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
@login_required(login_url='signin')
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


@never_cache
@login_required(login_url='signin')
def pat_doc_view_home(request, doctor_id):
    doctor = get_object_or_404(tbl_user, id=doctor_id, user_type='doctor')
    doctor_details = {
        'basic_info': doctor,
        'profile': doctor.doctor,
        'specializations': DoctorSpecialization.objects.filter(doctor=doctor.doctor),
        'qualifications': Qualification.objects.filter(doctor=doctor.doctor),
        'experiences': Experience.objects.filter(doctor=doctor.doctor),
    }
    context = {'doctor_details': doctor_details}
    return render(request, 'pat_doc_view.html', context)

@never_cache
@login_required(login_url='signin')
def pat_doc_view(request, doctor_id):
    doctor = get_object_or_404(tbl_user, id=doctor_id, user_type='doctor')
    doctor_details = {
        'basic_info': doctor,
        'profile': doctor.doctor,
        'specializations': DoctorSpecialization.objects.filter(doctor=doctor.doctor),
        'qualifications': Qualification.objects.filter(doctor=doctor.doctor),
        'experiences': Experience.objects.filter(doctor=doctor.doctor),
    }
    context = {'doctor_details': doctor_details}
    return render(request, 'pat_doc_view.html', context)

@never_cache
@login_required(login_url='signin')
def view_doctor_details(request, doctor_id):
    doctor = get_object_or_404(tbl_user, id=doctor_id, user_type='doctor')
    doctor_details = {
        'basic_info': doctor,
        'profile': doctor.doctor,
        'specializations': DoctorSpecialization.objects.filter(doctor=doctor.doctor),
        'qualifications': Qualification.objects.filter(doctor=doctor.doctor),
        'experiences': Experience.objects.filter(doctor=doctor.doctor),
    }
    context = {'doctor_details': doctor_details}
    return render(request, 'view_doctor_details.html', context)

@never_cache
@login_required(login_url='signin')
def view_doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    specializations = doctor.doctorspecialization_set.all()
    qualifications = doctor.qualification_set.all()
    experiences = doctor.experience_set.all()
    return render(request, 'doctor_profile.html', {'doctor': doctor, 'specializations': specializations, 'qualifications': qualifications, 'experiences': experiences})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.dateparse import parse_date

from .models import AppointmentTime
from .models import Doctor  # Import the Doctor model if not imported already

# def schedule_timings(request):
#     doctor = get_object_or_404(Doctor, user=request.user)
#     if request.method == 'POST':
#         date_str = request.POST.get('date')
#         date = parse_date(date_str)  # Convert date string to date object
        
#         if not date:
#             messages.error(request, "Invalid date format.")
#             return redirect('schedule_timings')  # Redirect back to the same page
        
#         slots_selected = request.POST.getlist('slots')
        
#         if len(slots_selected) < 1 or len(slots_selected) > 10:
#             messages.error(request, "Please select slots.")
#             return redirect('schedule_timings')  # Redirect back to the same page
        
#         for slot_time in slots_selected:
#             # Create an AppointmentTime instance for each selected slot
#             appointment_time = AppointmentTime.objects.create(
#                 day=date.strftime("%A"),
#                 from_to=slot_time,
#                 appointment_date=date,
#                 month=date.strftime("%B"),
#                 date=date,
#                 doctor=doctor
#             )
#             appointment_time.save()
        
#         messages.success(request, 'Slots added successfully.')
#         return redirect('schedule_timings')  # Redirect back to the same page
    
#     return render(request, 'schedule_timings.html')

from django.db.models import Q
@never_cache
@login_required(login_url='signin')
def schedule_timings(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        if selected_date <= now().date():
            messages.error(request, "Please select a future date.")
            return redirect('schedule_timings')  # Redirect back to the same page
        
        max_date = now().date() + timedelta(days=7)  # Max date (today + 7 days)
        if selected_date > max_date:
            messages.error(request, "Please select a date within the next week.")
            return redirect('schedule_timings')  # Redirect back to the same page
        
        slots_selected = request.POST.getlist('slots')
        
        if len(slots_selected) < 1 or len(slots_selected) > 10:
            messages.error(request, "Please select slots.")
            return redirect('schedule_timings')  # Redirect back to the same page
        
        # Check if slots already exist for the selected date and doctor
        existing_slots = AppointmentTime.objects.filter(
            doctor=doctor,
            appointment_date=selected_date,
            from_to__in=slots_selected
        )
        
        if existing_slots.exists():
            messages.error(request, "Slots already exist for the selected date.")
            return redirect('schedule_timings')  # Redirect back to the same page
        
        # Create new slots
        for slot_time in slots_selected:
            appointment_time = AppointmentTime.objects.create(
                day=selected_date.strftime("%A"),
                from_to=slot_time,
                appointment_date=selected_date,
                month=selected_date.strftime("%B"),
                date=selected_date,
                doctor=doctor
            )
            appointment_time.save()
        
        messages.success(request, 'Slots added successfully.')
        return redirect('schedule_timings')  # Redirect back to the same page
    doctor_slots = AppointmentTime.objects.filter(doctor=doctor, is_booked=False).order_by('appointment_date', 'from_to')

    # Group slots by appointment date
    grouped_slots = {}
    for slot in doctor_slots:
        appointment_date = slot.appointment_date.strftime("%d %b %Y")
        if appointment_date not in grouped_slots:
            grouped_slots[appointment_date] = []
        grouped_slots[appointment_date].append(slot)

    context = {'grouped_slots': grouped_slots}
    return render(request, 'schedule_timings.html', context)


@never_cache
@login_required(login_url='signin')
def delete_slot(request, slot_id):
    slot = get_object_or_404(AppointmentTime, id=slot_id)
    slot.delete()
    messages.success(request, 'Slot deleted successfully.')
    return redirect('view_slot')



def view_slot(request):
    doctor = request.user.doctor

    # Retrieve all slots for the respective doctor
    doctor_slots = AppointmentTime.objects.filter(doctor=doctor, is_booked=False).order_by('appointment_date', 'from_to')

    # Group slots by appointment date
    grouped_slots = {}
    for slot in doctor_slots:
        appointment_date = slot.appointment_date.strftime("%d %b %Y")
        if appointment_date not in grouped_slots:
            grouped_slots[appointment_date] = []
        grouped_slots[appointment_date].append(slot)

    context = {'grouped_slots': grouped_slots}
    return render(request, 'view_slot.html', context)



def edit_slot(request, slot_id):
    slot = get_object_or_404(AppointmentTime, id=slot_id)
    
    if request.method == 'POST':
        new_from_to = request.POST.get('new_from_to')
        slot.from_to = new_from_to
        slot.save()
        return redirect('view_slot')
    
    return render(request, 'edit_slot.html', {'slot': slot})

def delete_slot(request, slot_id):
    slot = get_object_or_404(AppointmentTime, id=slot_id)
    
    if request.method == 'POST':
        slot.delete()
        return redirect('view_slot')
    
    return render(request, 'delete_slot.html', {'slot': slot})

@never_cache
@login_required(login_url='signin') 
def booking(request, doctor_id):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)
    doctor = Doctor.objects.get(id=doctor_id)

    appoint_time_doctor = AppointmentTime.objects.filter(doctor=doctor, is_booked=False)
    
    unique_appoint_day = set(time_slot.day for time_slot in appoint_time_doctor)
    appoint_day = sorted(list(unique_appoint_day))  
    context = {
        'doctor': doctor,
        'appoint_time_doctor': appoint_time_doctor,
        'appoint_day': appoint_day,
    }
    return render(request, 'booking.html', context)







# def appointments(request):
#     current_user = request.user
#     current_doctor = Doctor.objects.get(user=current_user)

#     appointment = MedicalHistory.objects.filter(doctor=current_doctor)
#     specialization = DoctorSpecialization.objects.filter(doctor=current_doctor)
#     context = {
#         'current_doctor':current_doctor,
#         'appointment':appointment,
#         'specialization':specialization,
#     }
#     return render(request, 'appointments.html', context)


# @never_cache
# @login_required(login_url='signin')
# def booking_summary(request):
#     current_user = request.user
#     appointments = get_list_or_404(Appointment, patient__user=current_user)
#     if appointments:
#         appointment = appointments[0]
#     else:
#         appointment = None

#     context = {
#         'appointment': appointment,
#     }

#     if request.method=='POST':
#         amount=10000
#         order_currency='INR'
#         client=razorpay.Client(
#             auth=('rzp_test_GfzsM6qWehBGju','4ZZkYgLAtHFGy89EjiHpDCyE')
#         )
#         payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})


#     return render(request, 'booking_summary.html', context)

@never_cache
@login_required(login_url='signin')
def success(request):
    current_user = request.user
    appointments = get_list_or_404(Billing, patient__user=current_user)
    if appointments:
        appointment = appointments[0]
    else:
        appointment = None

    context = {
        'appointment': appointment,
    }
    return render(request,"success.html",context)


# def history(request):
#     #doctor = Doctor.objects.get(id=doctor_id)
#     #doctor_id = Doctor.objects.get(id=doctor_id)
#     current_user = request.user
#     current_patient = get_object_or_404(Patient, user=current_user)
#     patient = MedicalHistory.objects.filter(patient=current_patient)

#     first_name = current_patient.user.first_name
#     last_name = current_patient.user.last_name
#     gender = current_patient.gender
#     #doctor = Doctor.objects.get(id=doctor_id)
#     # medical_historyForm = MedicalHistory.objects.all()

#     if request.method == 'POST':
#         medical_history_entries = MedicalHistory.objects.filter(patient=current_patient, is_processing=False)

#         if medical_history_entries.exists():
#             # If there is exactly one matching entry, use it
#             if medical_history_entries.count() == 1:
#                 medical_history = medical_history_entries.first()
#             else:
#                 # Handle the case where there are multiple entries
#                 # You might want to log a warning or take some other action
#                 print("Warning: Multiple MedicalHistory entries found for the same patient.")
#                 medical_history = medical_history_entries.first()
#         else:
#             # If there are no matching entries, create a new one
#             medical_history = MedicalHistory(patient=current_patient, is_processing=False)

#     # Rest of the code...
       
#         form = MedicalHistoryForm(request.POST)
#         if form.is_valid():

#             medical_history.first_name = first_name
#             medical_history.last_name = last_name
#             medical_history.gender = gender
#             medical_history.reason = form.cleaned_data['reason']
#             # height = form.cleaned_data['height']
#             medical_history.blood_group = request.POST['blood_group']
#             medical_history.weight = form.cleaned_data['weight']
#             medical_history.age = form.cleaned_data['age']
#             medical_history.previous_operation = form.cleaned_data['previous_operation']
#             medical_history.current_medication = form.cleaned_data['current_medication']
#             medical_history.other_illness = form.cleaned_data['other_illness']
#             medical_history.other_information = form.cleaned_data['other_information']
#             medical_history.is_processing = True
#             medical_history.save()
#             return redirect('patient_dashboard')
#     else:
#         form = MedicalHistoryForm()

#     context = {
#         'form':form,
#     }
#     return render(request, 'medical_history.html', context)



@never_cache
@login_required(login_url='signin')
def profile(request, doctor_id):
    current_user = request.user
    # current_patient = get_object_or_404(Patient, user=current_user)
    
    doctor = Doctor.objects.get(id=doctor_id)
    specialization = DoctorSpecialization.objects.get(doctor=doctor)
    qualification = Qualification.objects.get(doctor=doctor)
    experience = Experience.objects.get(user=doctor)
    appointment = AppointmentTime.objects.filter(doctor=doctor)
    context = {
        'doc_profile':doctor,
        'specialization':specialization,
        'qualification':qualification,
        'experience':experience,
        'appointment':appointment,
    }
    return render(request, 'profile.html', context)







@never_cache
@login_required(login_url='signin')
def doctor_search(request):
    gender_type = request.GET.get('gender_type')
    select_specialist = request.GET.getlist('select_specialist')

    doctors = Doctor.objects.all()

    if gender_type:
        doctors = doctors.filter(gender=gender_type)
    
    if select_specialist:
        doctors = doctors.filter(doctorspecialization__specialized_category__in=select_specialist)

    return render(request, 'doctor_search.html', {'doctors': doctors})


def bill(request):
    return render(request, 'bill.html')

@never_cache
@login_required(login_url='signin')
def update_consulting_fee(request, user_id):
    doctor = get_object_or_404(Doctor, user_id=user_id)
    if request.method == 'POST':
        consulting_fee = request.POST.get('consulting_fee')
        doctor.consulting_fee = consulting_fee
        doctor.save()
        messages.success(request, 'Consulting fee updated successfully.')

    return redirect('doctor_list')






@never_cache
@login_required(login_url='signin')
def add_doctor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        name = request.POST.get('name')
        registration_number=request.POST.get('registration_number')
        # Generate a random password
        password = generate_random_password()

        # Create a new user
        user = tbl_user.objects.create(
            email=email, 
            phone_number=phone_number, 
            first_name=name, 
            user_type='doctor',
            is_email_verified=True
        )
        user.set_password(password)  # Set password manually
        user.save()

        # Create a doctor profile
        doctor = Doctor.objects.create(
            user=user, 
            registration_number=registration_number
        )

        # Send welcome email
        send_welcome_email(email, password)
        messages.success(request, 'New Doctor added successfully.')

        return redirect('add_doctor')  

    return render(request, 'add_doctor.html')


def generate_random_password(length=12):
    # Define characters to use for generating password
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate random password
    random_password = ''.join(secrets.choice(characters) for i in range(length))
    return random_password



def send_welcome_email(email, password):
    subject = 'Welcome to MediMingle'
    message = f'''Dear Doctor,

    We are thrilled to inform you that you are now part of our extended family at MediMingle!
    We warmly welcome you and look forward to working together to provide exceptional healthcare services to our community. 
    Your expertise and dedication will undoubtedly contribute to our shared mission of improving lives.
    If you have any questions or need assistance, please don't hesitate to reach out to us.



    Your login details:
    Email: {email}
    Password: {password}

    
    Best regards,
    Team Medimingle
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)







@never_cache
@login_required(login_url='signin')
def confirm_booking(request, doctor_id):
    if request.method == 'POST':
        selected_slot = request.POST.get('from_to')

        print("Selected slot:", selected_slot)  # Add this line for debugging


        print("Selected slot:", selected_slot)  # Add this line for debugging
        date_and_time_range = selected_slot.split('-')
        print("Split result:", date_and_time_range)  # Add this line for debugging
        if len(date_and_time_range) >= 4:  # Ensure there are at least four parts
            slot_date = '-'.join(date_and_time_range[:3]).strip()  # Extracting the date part
            slot_time = '-'.join(date_and_time_range[3:]).strip()  # Extracting the time range part
            patient_id = request.user.patient.id
            print("Slot date:", slot_date)  # Add this line for debugging
            print("Slot time:", slot_time)  # Add this line for debugging





        doctor = Doctor.objects.get(id=doctor_id)
        doctor_name = doctor.user.get_full_name()
        fee=doctor.consulting_fee
        appointment_time_slot = AppointmentTime.objects.get(doctor=doctor, from_to=slot_time,appointment_date=slot_date)


        # Create Appointment instance
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient_id=patient_id,
            appointment_time_slot=appointment_time_slot,
            appointment_datetime=slot_date,
            appointment_time=slot_time,
            is_confirmed=False  # Set as unconfirmed initially
        )

        # Construct email message
        subject = 'New Appointment Booking'
        email_message = (
            f"Dear {doctor_name},\n\n"
            f"A new appointment has been booked:\n\n"
            f"Date: {slot_date}\n"
            f"Time: {slot_time}\n"
            f"Patient: {request.user.get_full_name()}\n\n"
            "Thank you.\n"
        )

        # Send email to the doctor
        from_email = 'medimingle@gmail.com'  # Replace with your email address
        to_email = doctor.user.email
        send_mail(subject, email_message, from_email, [to_email])
        messages.success(request, "An email has been sent to the corresponding doctor. Please wait for their response.")


        appointment_time_slot.is_booked = True
        appointment_time_slot.save()
        Notification.objects.create(
            doctor=doctor,
            message=f"A new appointment has been booked for {slot_date} at {slot_time} by {request.user.get_full_name()}"
        )


        context = {
            'slot_time': slot_time,
            'slot_date': slot_date,
            'doctor_name': doctor_name,
            'appointment': appointment,
            'email_message': email_message,
            'fee':fee
        }
        return render(request, 'confirm_booking.html', context)
    else:
        # Handle GET request
        pass


@never_cache
@login_required(login_url='signin')
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if appointment.doctor != request.user.doctor:
        return redirect('doctor_dashboard')  # Redirect if not authorized

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            appointment.is_confirmed = True
            appointment.save()

            subject = 'Appointment Confirmation'
            message = f'Your appointment with Dr. {appointment.doctor} on {appointment.appointment_datetime} has been confirmed.'
            from_email = 'medimingle@gmail.com'  # Your email address
            to_email = appointment.patient.user.email
            send_mail(subject, message, from_email, [to_email])
            messages.success(request, "Your appointment has been confirmed.")
            Notification.objects.create(
                patient=appointment.patient,
                message=message
            )

            Billing.objects.create(
                doctor=appointment.doctor,
                patient=appointment.patient,
                appointment=appointment,
                amount=appointment.doctor.consulting_fee, 
            )

        elif action == 'reject':
            appointment.delete()
            subject = 'Cancellation'
            message = f'Your appointment request with Dr. {appointment.doctor} on {appointment.appointment_datetime} has been rejected by the doctor due to some reasons.'
            from_email = 'medimingle@gmail.com'  # Your email address
            to_email = appointment.patient.user.email
            send_mail(subject, message, from_email, [to_email])
            Notification.objects.create(
                patient=appointment.patient,
                message = f'Your appointment request with Dr. {appointment.doctor} on {appointment.appointment_datetime} has been rejected by the doctor due to some reasons.'
            )
         
        
        return redirect('doctor_dashboard')  # Redirect to doctor dashboard after action
    else:
        return redirect('doctor_dashboard')


@never_cache
@login_required(login_url='signin')
def view_due_details(request):
    patient = request.user.patient
    unpaid_bills = Billing.objects.filter(patient=patient, is_bill_paid=False)

    if unpaid_bills.exists():
        billing_id = unpaid_bills.first().id
        appointments_with_fee = []
        for bill in unpaid_bills:
            appointment = bill.appointment
            appointment_details = {
                'date': appointment.appointment_time_slot.appointment_date,
                'consulting_fee': appointment.doctor.consulting_fee,
                # Add other appointment details as needed
            }
            appointments_with_fee.append(appointment_details)
        return redirect('make_payment', billing_id=billing_id )
    else:
        return redirect(request, 'patient_dashboard')

@never_cache
@login_required(login_url='signin')
def make_payment(request, billing_id):
    billing = get_object_or_404(Billing, id=billing_id)
    unpaid_bills = Billing.objects.filter(is_bill_paid=False)

    if request.method == 'POST':
        billing.is_bill_paid = True
        billing.save()

        return redirect('success')

    else:
        appointments_with_fee = []
        for bill in unpaid_bills:
            appointment = bill.appointment
            appointment_details = {
                'date': appointment.appointment_datetime,
                'consulting_fee': appointment.doctor.consulting_fee,
                # Add other appointment details as needed
            }
            appointments_with_fee.append(appointment_details)
        # Initialize Razorpay client with your API key and secret
        client = razorpay.Client(auth=('rzp_test_GfzsM6qWehBGju','4ZZkYgLAtHFGy89EjiHpDCyE'))

        # Create a Razorpay order
        order_data = {
            'amount': int(billing.amount * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': 'order_rcptid_11',  # Replace with your receipt id
            'payment_capture': 1  # Auto-capture payments
        }
        razorpay_order = client.order.create(data=order_data)

        # Pass the order ID to the payment page
        return render(request, 'payment.html', {'order_id': razorpay_order['id']})


def generate_receipt(request, bill_id):
    bill = Billing.objects.get(id=bill_id)

    return render(request, 'receipt_template.html', {'bill': bill})



def generate_receipt_pdf(request, bill_id):
    # Retrieve the bill object from the database
    bill = Billing.objects.get(id=bill_id)
    
    # Render the template with the bill data
    template = get_template('receipt_template.html')
    context = {'bill': bill}
    html = template.render(context)
    
    # Generate PDF using the rendered HTML
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{bill_id}.pdf"'
    
    pisaStatus = pisa.CreatePDF(
       html, dest=response)
    
    # Return the PDF as response
    return response




from datetime import datetime, timedelta
@never_cache
@login_required(login_url='signin')
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctor = appointment.doctor
    
    if request.method == 'POST':
        new_date_str = request.POST.get('new_date')
        new_time = request.POST.get('new_time')
        
        # Convert new_date_str to a datetime object
        new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
        
        # Check if the new date is within 7 days from today
        today = datetime.now().date()
        max_date = today + timedelta(days=7)
        if new_date > max_date:
            messages.error(request, 'You can only select a date within 7 days from today.')
            return redirect('reschedule_appointment', appointment_id=appointment_id)
        
    
        # Check if the selected date and time combination already exists
        existing_slot = Appointment.objects.filter(
            Q(doctor=appointment.doctor) &
            Q(appointment_datetime=new_date_str) &
            Q(appointment_time=new_time)
        ).exclude(id=appointment_id).exists()  # Exclude the current appointment
        
        if existing_slot:
            messages.error(request, 'This slot is already booked.')
            return redirect('reschedule_appointment', appointment_id=appointment_id)
        
        appointment.appointment_datetime = new_date_str
        appointment.appointment_time = new_time
        appointment.save()
        
        # Send email notification to the patient
        send_reschedule_email(appointment.patient.user.email, appointment)
        messages.success(request, 'Appointment rescheduled successfully.')
        # Redirect back to doctor dashboard or any other desired page
        return redirect('doctor_dashboard')  # Replace 'doctor_dashboard' with your actual URL name
    
    return render(request, 'reschedule_appointment.html', {'appointment': appointment})


def send_reschedule_email(patient_email, appointment):
    subject = 'Appointment Rescheduled'
    message = f"Your appointment with {appointment.doctor.user.get_full_name()} has been rescheduled to {appointment.appointment_datetime} at {appointment.appointment_time}."
    sender_email = 'your_email@example.com'  # Replace with your email
    send_mail(subject, message, sender_email, [patient_email])

#...............Seminar...................#

def doc_suggest(request):
    if request.method == 'POST':
        age_range = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        age_lower, age_upper = map(int, age_range.split('-'))
        

        if age_lower  < 15:
            # Retrieve the list of doctors specialized as pediatricians
            pediatricians = Doctor.objects.filter(doctorspecialization__specialized_category='Pediatrician')

            # Save the questionnaire responses and doctor details in the database
            response = QuestionnaireResponse.objects.create(age=age_range, height=height, weight=weight)
            response.save()

            # Pass the list of pediatrician doctors and the message to the template
            return render(request, 'doc_suggest.html', {'pediatricians': pediatricians, 'message': "You should consult a pediatrician."})

        else:
            # Redirect to another page or return some other response
           return redirect('doc_suggest')

    # else:
    #     return HttpResponse("Error: Form submission method not allowed!")
    return render(request,'doc_suggest.html')


def doc_suggest2(request):
    return render(request,'doc_suggest2.html')



def my_doctors(request):
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient)
    doctors = [appointment.doctor for appointment in appointments]
    context = {'doctors': doctors, 'appointments': appointments}
    return render(request, 'my_doctors.html', context)



def medical_data(request):
    return render(request, 'medical_data.html')