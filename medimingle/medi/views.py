import datetime
from tkinter import Canvas
from django.http import FileResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import Doctor, Patient, tbl_user, AppointmentTime,DoctorSpecialization,MedicalHistory,Qualification,Experience,Appointment,Notification
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

import secrets
import string
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

            # Send activation email
            subject = 'Activate Your Medimingle Account'
            message = f'Hi {user.first_name},\n\nClick the link below to activate your account:\n\n{activation_link}\n\nBest regards,\nThe Medimingle Team'
            send_mail(subject, message, 'medimingle@gmail.com', [user.email])
            messages.success(request, "You have registered successfully. Verify your email and login.")
            return redirect('signin')
        else:
            return render(request,'register.html')
        
 
"""
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
                messages.error(request, "Admin has blocked your account")
                return redirect('signin')
            elif user is not None and not user.is_email_verified:
                messages.info(request, "Email not verified.")
            else:
                messages.info(request,"Invalid Credentials")
                return redirect('signin')
        response = render(request,"signin.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response"""


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
    patient_appointments = Appointment.objects.filter(patient=request.user.patient)
    doc = tbl_user.objects.filter(user_type='doctor').exclude(is_superuser=True)
    notifications = Notification.objects.filter(patient=current_patient)
    n_count=notifications.count()

    context={
        'patient': current_patient,
        'appointments':patient_appointments,
        'n_count':n_count
    }
    

    return render(request,'patient_dashboard.html',context)

@never_cache   
@login_required(login_url='signin')
def doctor_dashboard(request):
    current_user = request.user
    current_doctor = get_object_or_404(Doctor, user=current_user)
    specialization = DoctorSpecialization.objects.filter(doctor=current_doctor)
    doctor_appointments = Appointment.objects.filter(doctor=request.user.doctor)
    notifications = Notification.objects.filter(doctor=current_doctor)
    n_count=notifications.count()
    if request.method == 'POST':
        patient_id = request.POST['status']
        accepted_patient = MedicalHistory.objects.get(id=patient_id)
        accepted_patient.is_active = True
        accepted_patient.save()
        return redirect('doctor_dashboard')

    pat=tbl_user.objects.filter(user_type='patient').exclude(is_superuser=True)
    pat_count=pat.count()
    context={
        "pat":pat,
        "pat_count":pat_count,
        "doctor": current_doctor,
        'specialization':specialization,
        'appointments': doctor_appointments,
        'notifications': notifications,
        "n_count":n_count

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


def doc_suggest(request):
    return render(request,'doc_suggest.html')


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

def schedule_timings(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    starting_times = {
        '08:00': '8:00 AM',
        '08:30': '8:30 AM',
        '09:00': '9:00 AM',
        '10:30': '10:30 AM',
        '11:00': '11:00 AM',
        '02:00': '2:00 PM',
        '02:30': '2:30 PM',
        '03:00': '3:00 PM',
        '03:30': '3:30 PM',
        '04:00': '4:00 PM'    
    }

    if request.method == "POST":
        appointment_date = request.POST.get('appointment_date')
        time_from = request.POST.get('time_from')
        appointment_date_obj = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        time_from_obj = datetime.strptime(time_from, '%H:%M').time()
        ending_time_obj = (datetime.combine(datetime.today(), time_from_obj) + timedelta(minutes=30)).time()
        t = f"{time_from}-{ending_time_obj}"
        if appointment_date_obj < timezone.now().date():
            messages.error(request, 'Cannot schedule slots for past dates.')
            return redirect(request.path_info)
        existing_slots = AppointmentTime.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date_obj,
            time_from=time_from_obj
        )
        if existing_slots.exists():
            messages.error(request, 'This time slot is already scheduled for the selected date.')
            return redirect(request.path_info)
        num_existing_slots = AppointmentTime.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date_obj
        ).count()
        if num_existing_slots >= 10:
            messages.error(request, 'Doctor cannot schedule more than 10 timings for a day.')
            return redirect(request.path_info)

        AppointmentTime.objects.create(
            day=appointment_date_obj.strftime("%A"),
            time_from=time_from_obj,
            time_to=ending_time_obj,
            from_to=t,
            appointment_date=appointment_date_obj,
            date=appointment_date_obj.strftime("%d"),
            month=appointment_date_obj.strftime("%B"),
            doctor=doctor
        )

        messages.success(request, 'Slot added successfully.')
        return redirect(request.path_info)

    context = {
        'doctor': doctor,
        'starting_times': starting_times,
    }

    return render(request, 'schedule_timings.html', context)




@never_cache
@login_required(login_url='signin')
def delete_slot(request, slot_id):
    slot = get_object_or_404(AppointmentTime, id=slot_id)
    slot.delete()
    messages.success(request, 'Slot deleted successfully.')
    return redirect('view_slot')


@never_cache
@login_required(login_url='signin')

def view_slot(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    scheduled_slots = AppointmentTime.objects.filter(doctor=doctor).order_by('appointment_date', 'time_from')

    unique_days = scheduled_slots.values_list('day', flat=True).distinct()

    context = {
        'doctor': doctor,
        'unique_days': unique_days,
        'scheduled_slots': scheduled_slots,
    }
    return render(request, "view_slot.html", context)


@never_cache
@login_required(login_url='signin') 
def booking(request, doctor_id):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)
    doctor = Doctor.objects.get(id=doctor_id)

    appoint_time_doctor = AppointmentTime.objects.filter(doctor=doctor)
    
    unique_appoint_day = set(time_slot.day for time_slot in appoint_time_doctor)
    appoint_day = sorted(list(unique_appoint_day))  
    context = {
        'doctor': doctor,
        'appoint_time_doctor': appoint_time_doctor,
        'appoint_day': appoint_day,
    }
    return render(request, 'booking.html', context)






def medical_history(request):
    current_user = request.user
    try:
        current_doctor = get_object_or_404(Doctor, user=current_user)
    except:
        raise ValueError('no doctor found')
    buf = io.BytesIO()
    c = Canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    history = MedicalHistory.objects.filter(doctor=current_doctor)

    lines = []

    for hist in history:
        lines.append("********* MediHelp *************")
        lines.append(" ")
        lines.append("========== Patient Medical History ===============")
        lines.append("First Name: "+hist.first_name)
        lines.append("Last Name: "+hist.last_name)
        lines.append("Reason For Visit: "+hist.reason)
        lines.append("Height: "+hist.weight)
        lines.append("Age: "+hist.age)
        lines.append("Gender: "+str(hist.gender))
        lines.append("Blood Group: "+hist.blood_group)
        lines.append("Previous Operation: "+hist.previous_operation)
        lines.append("Current Medicaion: "+hist.current_medication)
        lines.append("Other Illness: "+hist.other_illness)
        lines.append("Other Information: "+hist.other_information)
        lines.append("==========================================")
        

    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='medical_history.pdf')

def appointments(request):
    current_user = request.user
    current_doctor = Doctor.objects.get(user=current_user)

    appointment = MedicalHistory.objects.filter(doctor=current_doctor)
    specialization = DoctorSpecialization.objects.filter(doctor=current_doctor)
    context = {
        'current_doctor':current_doctor,
        'appointment':appointment,
        'specialization':specialization,
    }
    return render(request, 'appointments.html', context)


@never_cache
@login_required(login_url='signin')
def booking_summary(request):
    current_user = request.user
    appointments = get_list_or_404(Appointment, patient__user=current_user)
    if appointments:
        appointment = appointments[0]
    else:
        appointment = None

    context = {
        'appointment': appointment,
    }

    if request.method=='POST':
        amount=10000
        order_currency='INR'
        client=razorpay.Client(
            auth=('rzp_test_GfzsM6qWehBGju','4ZZkYgLAtHFGy89EjiHpDCyE')
        )
        payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})


    return render(request, 'booking_summary.html', context)
@never_cache
@login_required(login_url='signin')
def success(request):
    current_user = request.user
    appointments = get_list_or_404(Appointment, patient__user=current_user)
    if appointments:
        appointment = appointments[0]
    else:
        appointment = None

    context = {
        'appointment': appointment,
    }
    return render(request,"success.html",context)


def history(request):
    #doctor = Doctor.objects.get(id=doctor_id)
    #doctor_id = Doctor.objects.get(id=doctor_id)
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)
    patient = MedicalHistory.objects.filter(patient=current_patient)

    first_name = current_patient.user.first_name
    last_name = current_patient.user.last_name
    gender = current_patient.gender
    #doctor = Doctor.objects.get(id=doctor_id)
    # medical_historyForm = MedicalHistory.objects.all()

    if request.method == 'POST':
        medical_history_entries = MedicalHistory.objects.filter(patient=current_patient, is_processing=False)

        if medical_history_entries.exists():
            # If there is exactly one matching entry, use it
            if medical_history_entries.count() == 1:
                medical_history = medical_history_entries.first()
            else:
                # Handle the case where there are multiple entries
                # You might want to log a warning or take some other action
                print("Warning: Multiple MedicalHistory entries found for the same patient.")
                medical_history = medical_history_entries.first()
        else:
            # If there are no matching entries, create a new one
            medical_history = MedicalHistory(patient=current_patient, is_processing=False)

    # Rest of the code...
       
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():

            medical_history.first_name = first_name
            medical_history.last_name = last_name
            medical_history.gender = gender
            medical_history.reason = form.cleaned_data['reason']
            # height = form.cleaned_data['height']
            medical_history.blood_group = request.POST['blood_group']
            medical_history.weight = form.cleaned_data['weight']
            medical_history.age = form.cleaned_data['age']
            medical_history.previous_operation = form.cleaned_data['previous_operation']
            medical_history.current_medication = form.cleaned_data['current_medication']
            medical_history.other_illness = form.cleaned_data['other_illness']
            medical_history.other_information = form.cleaned_data['other_information']
            medical_history.is_processing = True
            medical_history.save()
            return redirect('patient_dashboard')
    else:
        form = MedicalHistoryForm()

    context = {
        'form':form,
    }
    return render(request, 'medical_history.html', context)

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
# def doctor_search(request):
#     doctors = Doctor.objects.order_by('-date_joined') #A hyphen "-" in front of "check_in" indicates descending order. 

#     if 'gender_type' in request.GET:
#         gender_type = request.GET['gender_type']
#         if gender_type:
#             doctors = doctors.filter(gender__iexact=gender_type)
            
#     context = {
#         'doctors':doctors,
#     }
#     return render(request, 'doctor_search.html', context)




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
        selected_slot = request.POST.get('from_to').split('-')
        slot_date = selected_slot[0]
        slot_time = selected_slot[1]
        patient_id = request.user.patient.id


        doctor = Doctor.objects.get(id=doctor_id)
        doctor_name = doctor.user.get_full_name()

        # Create Appointment instance
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient_id=patient_id,
            appointment_datetime=slot_date,
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







