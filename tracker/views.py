from django.db.models.query_utils import PathInfo
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from vaccine_tracker.settings import DATABASES, EMAIL_HOST_USER
from .decorators import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .filters import *
import datetime
from xhtml2pdf import pisa
from easy_pdf.views import PDFTemplateResponseMixin, PDFTemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.decorators import method_decorator




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
                recipient = str(form.cleaned_data.get('email'))
            
                send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently = False)

                messages.success(request, 'Account was created for ' + username)
                return redirect('home')
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
                
        context = {'form':form}
        return render(request, 'tracker/register.html', context)

def password_reset(request):
    password_reset_form = PasswordResetForm()

    if(request.method == 'POST'):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            users = User.objects.filter(Q(email=email))
            if users.exists():
                for user in users:
                    subject = 'Password Reset Requested'
                    email_template_name = 'tracker/password/password_reset_email.txt'
                    context = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    mail = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject, mail, EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found!')
                    return redirect('password_reset/done')
    data = {
        'password_reset_form': password_reset_form
    }
    return render(request, 'tracker/password/password_reset.html', data)

@login_required(login_url='login')
def notifsPage(request):
    return render(request,'tracker/notifs.html')

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
                    if user.groups.filter(name='Patient User').exists():
                        login(request, user)
                        return redirect('homePatient')
                    else:
                        login(request, user)
                        return redirect('home')
                else:
                    messages.info(request, 'Username or password is incorrect. Please try again.')
        context = {}
        return render(request, 'tracker/login.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Doctor'])
def homePage(request):
    patients = Patient.objects.all()
    patientFilter = PatientFilter(request.GET, queryset=patients)
    patients = patientFilter.qs

    physicians = Physician.objects.all()
    data = {
        'patients': patients, 'physicians': physicians , 'patientFilter': patientFilter,
    }

    return render(request, "tracker/home.html", data)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Patient User'])
def homePagePatient(request):
    patientUser = request.user.patientuser

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patientUser.patient.birthdate.month
    years = curr_date.year - patientUser.patient.birthdate.year
    age = "{} year {} month".format(years, months)
    
    data = {
        'patientUser': patientUser, 'age': age,
    }
    return render(request, 'tracker/homePatient.html', data)

#--CREATE RECORD VIEW--
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Doctor'])
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

            messages.success(request, 'Account was created for {} {}.'.format(pfname, plname))
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
        return redirect('/home')

    context = {'patient_form':patient_form,
                'latest_id': latest_id,
    }
    return render(request, "tracker/createRecord.html", context)
    
@login_required(login_url='login')
def patient(request, pk):
    patient = Patient.objects.get(id=pk)

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)
    
    data = {
        'patient': patient, 'age': age,
    }
    return render(request, 'tracker/patient.html', data)


@login_required(login_url='login')
def editPatient(request, pk):
    patient = Patient.objects.get(id=pk)
    patient_form = CreateRecordFormPatient(instance=patient)

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    if(request.method == "POST"):
        patient_form = CreateRecordFormPatient(request.POST, instance=patient)
        if patient_form.is_valid():
            pfname = patient_form.cleaned_data.get('first_name')
            plname = patient_form.cleaned_data.get('last_name')
            patient_form.save()

            return redirect('/patient/' + pk)

    data = {
        'patient': patient, 'patient_form': patient_form,
        'age': age,
    }

    return render(request, 'tracker/editPatient.html', data)

@login_required(login_url='login')
def appointment(request, pk):
    patient = Patient.objects.get(id=pk)
    appointment_form = AppointmentForm(initial={'patient': patient})
    appointment_form_patient = AppointmentFormPatient(initial={'patient': patient, 'status': 'Requested', 'doctor': patient.attending_doctor})

    appointments = Appointment.objects.all()

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    if(request.method == "POST"):
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment_form.save()
            messages.success(request, 'Appointment scheduled!')
        else:
            messages.error(request, 'Failed to schedule appointment.')
        return redirect('/appointment/' + pk)

    data = {
        'patient': patient,
        'appointment_form': appointment_form,
        'appointment_form_patient': appointment_form_patient,
        'appointments': appointments,
        'age': age,
    }

    return render(request, 'tracker/appointment.html', data)

# @method_decorator(login_required, name='dispatch')
# class editAppointment(UpdateView, DetailView):
#     model = Patient
#     template_name = 'tracker/editAppointment.html'
#     fields = ['status',]

#     def get_context_data(self, request, pk, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['patient'] = Patient.objects.get(id=pk)

#         # -- Age (X Years Y Months) --
#         curr_date = datetime.date.today()
#         months = curr_date.month - patient.birthdate.month
#         years = curr_date.year - patient.birthdate.year
#         age = "{} year {} month".format(years, months)

#         return context


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Doctor'])
def editAppointment(request, pk):
    patient = Patient.objects.get(id=pk)
    appointments = Appointment.objects.all()
    edit_appointment_form = EditAppointmentForm(instance=patient)

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    if(request.method == "POST"):
        edit_appointment_form = EditAppointmentForm(request.POST, instance=patient)
        if edit_appointment_form.is_valid():
            edit_appointment_form.save()
       
        return redirect('/appointment/' + pk)

    data = {
        'patient': patient,
        'edit_appointment_form': edit_appointment_form,
        'appointments': appointments,
        'age': age,
    }

    return render(request, 'tracker/editAppointment.html', data)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Doctor'])
def portal(request, pk):
    patient = Patient.objects.get(id=pk)
    patient_user_grp = Group.objects.get(name='Patient User')
    portal_form = PortalForm()
    patient_form = PatientUserForm()
    
    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    if request.method == 'POST':
        portal_form = PortalForm(request.POST)
        patient_form = PatientUserForm(request.POST)
        if User.objects.filter(username = request.POST['username']).exists():
            messages.error(request, 'Username exists.')
        else:
            if portal_form.is_valid() and patient_form.is_valid():
                user = portal_form.save()
                profile = patient_form.save(commit=False)
                profile.user = user
                profile.patient = patient
                profile.save()
                patient_user_grp.user_set.add(user)
                messages.success(request, 'Account Created!')
        return redirect('/portal/' + pk)
    
    data = {
        'patient': patient, 
        'age': age,
        'portal_form': portal_form,
        'patient_form': patient_form,
    }
    return render(request, 'tracker/portal.html', data)

@login_required(login_url='login')
def certificate(request, pk):
    patient = Patient.objects.get(id=pk)
    cert_date_form = CertDateForm(instance=patient)
    #cert_date = None

    # -- Age (x Years y Months) -- 
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    if(request.method == "POST"):
         cert_date_form = EditAppointmentForm(request.POST, instance=patient)
         if cert_date_form.is_valid():
             cert_date_form.save()
       
         return redirect('/certificate/' + pk)

    data = {
        'patient': patient, 
        'age': age,
        'curr_date': curr_date,
        'cert_date_form': cert_date_form,
    }
    return render(request, 'tracker/certificate.html', data)

class PdfDetail(PDFTemplateResponseMixin, DetailView):
    model = Patient
    template_name = 'tracker/pdf_cert.html'
    download_filename = 'Vaccine Certificate of {}-{}'.format(model.last_name, model.first_name)
    context_object_name = 'patient'

    # curr_date = datetime.date.today()
    # months = curr_date.month - model.birthdate.month
    # years = curr_date.year - model.birthdate.year
    # age = "{} year {} month".format(years, months)

@login_required(login_url='login')
def vaccine(request, pk):
    patient = Patient.objects.get(id=pk)
    vaccines = Vaccine.objects.all()

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)
    
    data = {
        'patient': patient, 
        'vaccines': vaccines,
        'age': age,
    }
    return render(request, 'tracker/vaccine.html', data)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Doctor'])
def editVaccine(request, pk):
    patient = Patient.objects.get(id=pk)
    vaccines = Vaccine.objects.all()
    vaccine_form = PatientVaccineForm(instance=patient)

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    if(request.method == "POST"):
        vaccine_form = PatientVaccineForm(request.POST, instance=patient)
        if vaccine_form.is_valid():
            vaccine_form.save()
       
        return redirect('/vaccine/' + pk)
    
    data = {
        'patient': patient, 
        'vaccine_form': vaccine_form,
        'vaccines': vaccines,
        'age': age,
    }
    return render(request, 'tracker/editVaccine.html', data)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Doctor'])
def report(request):

    return render(request, 'tracker/report.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Doctor'])
def reminder(request):

    return render(request, 'tracker/reminder.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Doctor'])
def staffUpdate(request):
    doc_grp = Group.objects.get(name='Doctor')

    return render(request, 'tracker/staffUpdate.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Doctor'])
def staffCreate(request):
    doc_grp = Group.objects.get(name='Doctor')
    staff_create_form = StaffCreateForm()
    doc_user_form = DoctorForm()
    

    if request.method == 'POST':
        staff_create_form = StaffCreateForm(request.POST)
        doc_user_form = DoctorForm(request.POST)
        if User.objects.filter(username = request.POST['username']).exists():
            messages.error(request, 'Username exists.')
        else:
            if staff_create_form.is_valid() and doc_user_form.is_valid():
                #staff_create_form.save()
                user = staff_create_form.save()
                profile = doc_user_form.save(commit=False)
                profile.user = user
                profile.save()
                doc_grp.user_set.add(user)
                messages.success(request, 'Account Created!')
        return redirect('/staffCreate/')
    
    data = {
        'staff_create_form': staff_create_form,
        'doc_user_form': doc_user_form,
    }

    return render(request, 'tracker/staffCreate.html', data)