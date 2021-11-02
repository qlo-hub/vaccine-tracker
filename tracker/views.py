from django.db.models.query_utils import PathInfo
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from vaccine_tracker.settings import EMAIL_HOST_USER
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .filters import *
import datetime


# Create your views here.
# @login_required(login_url='login')
# @user_passes_test(lambda u: u.is_superuser)
def registerPage(request):
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                last_name = form.cleaned_data.get('last_name')
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                subject = 'Account Registration'
                message = 'Hi Mr./Ms.' + last_name + '! Here are your account credentials for our application.' + ' Username: ' + username + ' Password: ' + raw_password
                recepient = str(form.cleaned_data.get('email'))
            
                send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

                messages.success(request, 'Account was created for ' + username)
                return redirect('home')
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
                
        context = {'form':form}
        return render(request, 'patientmonitoring/register.html', context)

@login_required(login_url='login')
def notifsPage(request):
    return render(request,'patientmonitoring/notifs.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'Username or password is incorrect. Please try again.')
        context = {}
        return render(request, 'patientmonitoring/login.html', context)



@login_required(login_url='login')
def homePage(request):
    patients = Patient.objects.all()
    patientFilter = PatientFilter(request.GET, queryset=patients)
    patients = patientFilter.qs

    physicians = Physician.objects.all()
    data = {
        'patients': patients, 'physicians': physicians , 'patientFilter': patientFilter,
    }

    return render(request, "patientmonitoring/home.html", data)

#--CREATE RECORD VIEW--
@login_required(login_url='login')
def createRecord(request):
    patient_form = CreateRecordFormPatient()
    latest = Patient.objects.latest('id')
    latest_id = getattr(latest, 'id')

    
    
    if(request.method == "POST"):
        patient_form = CreateRecordFormPatient(request.POST)
        if patient_form.is_valid():
            pfname = patient_form.cleaned_data.get('first_name')
            plname = patient_form.cleaned_data.get('last_name')

            patient_form.save()

            messages.success(request, 'Account was created for ' + pfname + plname)
        return redirect('/home')
        # else:
            # messages.error(request, "Unsuccessful registration. Invalid information.")


    context = {'patient_form':patient_form,
                'latest_id': latest_id,
    }
    return render(request, "patientmonitoring/createRecord.html", context)

@login_required(login_url='login')
def patient(request, pk):
    patient = Patient.objects.get(id=pk)
    bday = getattr(patient, 'birthdate')
    curr_date = datetime.date.today()
    months = curr_date.month - bday.month 
    
    data = {
        'patient': patient, 'months': months,
    }
    return render(request, 'patientmonitoring/patient.html', data)

@login_required(login_url='login')
def editPatient(request, pk):
    patient = Patient.objects.get(id=pk)
    patient_form = CreateRecordFormPatient(instance=patient)

    if(request.method == "POST"):
        patient_form = CreateRecordFormPatient(request.POST, instance=patient)
        if patient_form.is_valid():
            pfname = patient_form.cleaned_data.get('first_name')
            plname = patient_form.cleaned_data.get('last_name')

            patient_form.save()

            # messages.success(request, 'Account was created for ' + pfname + plname)
            return redirect('/patient/' + pk)

    data = {
        'patient': patient, 'patient_form': patient_form
    }

    return render(request, 'patientmonitoring/editPatient.html', data)

@login_required(login_url='login')
def appointment(request, pk):
    patient = Patient.objects.get(id=pk)
    appointment_form = AppointmentForm(initial={'patient': patient})

    appointments = Appointment.objects.all()

    if(request.method == "POST"):
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment_form.save()
            messages.success(request, 'Appointment scheduled!')
        else:
            messages.error(request, 'Appointment scheduling failed!')
        return redirect('/appointment/' + pk)

    data = {
        'patient': patient,
        'appointment_form': appointment_form,
        'appointments': appointments,
    }

    return render(request, 'patientmonitoring/appointment.html', data)