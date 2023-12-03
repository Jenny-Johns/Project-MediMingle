import datetime
from tkinter import Canvas
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate
from django.contrib.auth import authenticate, login
from .models import Doctor, Patient, tbl_user, AppointmentTime,DoctorSpecialization,MedicalHistory,Qualification,Experience,PatientAppointment
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User  
from django.contrib.auth.decorators import login_required
from .forms import UserProfileUpdateForm,ProfileUpdateForm
from .forms import  DoctorSpecializationForm, QualificationForm, ExperienceForm,DoctorForm,MedicalHistoryForm
from django.views.decorators.http import require_POST
from .choices import category, fromTimeChoice,toTimeChoice

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
        patient_data = Patient(user=user)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user)
        patient_form = UserProfileUpdateForm(request.POST, request.FILES, instance=patient_data)

        if user_form.is_valid() and patient_form.is_valid():
            # Update the Patient model fields
            user_form.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            messages.success(request, "Profile Updated")
            return redirect('profile_settings')  # Redirect back to the profile update page or another page
    else:
        user_form = ProfileUpdateForm(instance=user)
        patient_form = UserProfileUpdateForm(instance=patient_data)

    return render(request, 'profile_settings.html', {'user_form': user_form, 'patient_form': patient_form})
# def profile_settings(request):
#     user = request.user  # Get the logged-in user
#     try:
#         patient_data = Patient.objects.get(user=user)
#     except Patient.DoesNotExist:
#         patient_data = None

#     if request.method == 'POST':
#         user_form = ProfileUpdateForm(request.POST, instance=user)
#         patient_form = UserProfileUpdateForm(request.POST, request.FILES, instance=patient_data)

#         if user_form.is_valid() and patient_form.is_valid():
#             # Update the Patient model fields
#             user_form.save()
#             patient_form.save()
#             messages.success(request,"Profile Updated")
#             return redirect('patient_dashboard')  # Redirect back to the profile update page or another page
#     else:
#         user_form = ProfileUpdateForm(instance=user)
#         patient_form = UserProfileUpdateForm(instance=patient_data)
#     return render(request, 'profile_settings.html', {'user_form': user_form,'patient_form':patient_form})




@never_cache   
@login_required(login_url='signin')
def doctor_profile_settings(request):
    user = request.user  # Get the logged-in user
    doctor, created = Doctor.objects.get_or_create(user=user)
    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        
        if doctor:
            specialization_form = DoctorSpecializationForm(request.POST, instance=doctor.doctorspecialization_set.first())
            qualification_form = QualificationForm(request.POST, instance=doctor.qualification_set.first())
            experience_form = ExperienceForm(request.POST, instance=doctor.experience_set.first())
        else:
            specialization_form = DoctorSpecializationForm(request.POST)
            qualification_form = QualificationForm(request.POST)
            experience_form = ExperienceForm(request.POST)

        if user_form.is_valid() and doctor_form.is_valid() and specialization_form.is_valid() and qualification_form.is_valid() and experience_form.is_valid():
            user_form.save()
            
            # Ensure that the doctor instance has a user before saving
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            if doctor:
                doctorspecialization = specialization_form.save(commit=False)
                doctorspecialization.doctor = doctor
                specialization_form.save()
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

        if doctor:
            specialization_form = DoctorSpecializationForm(instance=doctor.doctorspecialization_set.first())
            qualification_form = QualificationForm(instance=doctor.qualification_set.first())
            experience_form = ExperienceForm(instance=doctor.experience_set.first())
        else:
            specialization_form = DoctorSpecializationForm()
            qualification_form = QualificationForm()
            experience_form = ExperienceForm()

    return render(request, 'doctor_profile_settings.html', {'user_form': user_form, 'doctor_form': doctor_form, 'specialization_form': specialization_form, 'qualification_form': qualification_form, 'experience_form': experience_form})
# def doctor_profile_settings(request):
#     user = request.user  # Get the logged-in user
#     try:
#         doctor = Doctor.objects.get(user=user)
#     except Doctor.DoesNotExist:
#         doctor = None
    
#     if request.method == 'POST':
#         user_form = ProfileUpdateForm(request.POST, instance=user)
#         doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
#         specialization_form = DoctorSpecializationForm(request.POST, instance=doctor.doctorspecialization_set.first())
#         qualification_form = QualificationForm(request.POST, instance=doctor.qualification_set.first())
#         experience_form = ExperienceForm(request.POST, instance=doctor.experience_set.first())

#         if user_form.is_valid() and doctor_form.is_valid() and specialization_form.is_valid() and qualification_form.is_valid() and experience_form.is_valid():
#             user_form.save()
#             doctor_form.save()
#             doctorspecialization = specialization_form.save(commit=False)
#             doctorspecialization.doctor = doctor
#             specialization_form.save()
#             qualification = qualification_form.save(commit=False)
#             qualification.doctor = doctor
#             qualification.save()
#             experience = experience_form.save(commit=False)
#             experience.doctor = doctor
#             experience.save()
#             messages.success(request,"Profile Updated")           
#             return redirect('doctor_dashboard')

#     else:
#         user_form = ProfileUpdateForm(instance=user)
#         doctor_form = DoctorForm(instance=doctor)
#         specialization_form = DoctorSpecializationForm(instance=doctor.doctorspecialization_set.first())
#         qualification_form = QualificationForm(instance=doctor.qualification_set.first())
#         experience_form = ExperienceForm(instance=doctor.experience_set.first())

#     return render(request, 'doctor_profile_settings.html', {'user_form': user_form, 'doctor_form': doctor_form,'specialization_form':specialization_form, 'qualification_form': qualification_form, 'experience_form': experience_form})

# def doctor_specialization(request):
#     try:
#         current_doctor = Doctor.objects.get(user=request.user)
#     except Doctor.DoesNotExist:
#         pass
#     if request.method == 'POST':
#         category = request.POST.getlist('category')
#         for i in range(len(category)):
#             specialized_category = DoctorSpecialization( doctor=current_doctor,specialized_category=category[i])
#             specialized_category.save()
#         return redirect('doctor_profile_settings')
    


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


def login_view(request):
    return render(request,'login_view.html')


@never_cache
@login_required(login_url='signin')
@require_POST
def deactivate_user(request, user_id):
    user = get_object_or_404(tbl_user, id=user_id)
    user.is_active = False
    user.save()
    return redirect('adminpage')


@never_cache
@login_required(login_url='signin')
@require_POST
def activate_user(request, user_id):
    user = get_object_or_404(tbl_user, id=user_id)
    user.is_active = True
    user.save()
    return redirect('adminpage')


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
    if request.method == "POST":
        time_from = request.POST['time_from']
        time_to = request.POST['time_to']
        appointment_date = request.POST['appointment_date']
        from_to = time_from+"-"+time_to
        appointment_date_obj = datetime.datetime.strptime(appointment_date, '%Y-%m-%d')
        day = appointment_date_obj.date().strftime("%A")
        date = appointment_date_obj.date().strftime("%d")
        month = appointment_date_obj.date().strftime("%B")
        appoint_time = AppointmentTime.objects.create(day=day, time_from=time_from, time_to=time_to ,from_to=from_to, date=date, month=month, appointment_date=appointment_date, doctor=doctor)
        appoint_time.save()
        messages.success(request, 'Schedule added successfully.')
        return redirect(request.path_info)
    context = {
        'doctor':doctor,
        'fromTimeChoice': fromTimeChoice,
        'toTimeChoice' : toTimeChoice,
    }
    return render(request, 'schedule_timings.html',context)


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
    scheduled_slots = AppointmentTime.objects.filter(doctor=doctor)
    context={
        'doctor':doctor,
        'scheduled_slots':scheduled_slots,
    }
    return render(request,"view_slot.html",context)


@never_cache
@login_required(login_url='signin') 
def booking(request, doctor_id):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)
    doctor = Doctor.objects.get(id=doctor_id)
    # for checking purpose
    try:
        booked_doctor = MedicalHistory.objects.get(doctor=doctor, patient=current_patient)
    except:
        booked_doctor = MedicalHistory(doctor=doctor, patient=current_patient)
        booked_doctor.save()

    appoint_time_doctor = AppointmentTime.objects.filter(doctor=doctor)
    

    appoint_day = appoint_time_doctor.values_list('day',flat=True).distinct()
    appoint_date = appoint_time_doctor.values_list('appointment_date', flat=True)
    time_from = appoint_time_doctor.values_list('time_from',flat=True)
    time_to = appoint_time_doctor.values_list('time_to',flat=True)
    print("from: ", time_from)
    context = {
        'doctor':doctor,
        # 'form':form,
        'appoint_time_doctor' : appoint_time_doctor,
        # 'day_doc_appoint':day_doc_appoint,
        'appoint_day':appoint_day,
        'time_from': time_from,
        'time_to' : time_to,
        'appoint_date':appoint_date,

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

def patient_appointment(request, doctor_id):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)
    
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == "POST":
        
        from_to = str(request.POST['from_to'])
        print("from_to day:", from_to)
        
        splitted_from_to = from_to.split(',')
        print("Split: ", splitted_from_to[1])

        doc_appoint = PatientAppointment(appoint_day=splitted_from_to[1], appoint_time=splitted_from_to[0], doctor=doctor, patient=current_patient)
        doc_appoint.save()
        return redirect('history') 


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
def doctor_search(request):
    doctors = Doctor.objects.order_by('-date_joined') #A hyphen "-" in front of "check_in" indicates descending order. 

    if 'gender_type' in request.GET:
        gender_type = request.GET['gender_type']
        if gender_type:
            doctors = doctors.filter(gender__iexact=gender_type)
            # print("filtered: ",doctors)

    context = {
        'doctors':doctors,
    }
    return render(request, 'doctor_search.html', context)

def bill(request):
    return render(request, 'bill.html')

