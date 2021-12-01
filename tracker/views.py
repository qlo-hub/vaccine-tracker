from django.db.models import query
from django.db.models.query import QuerySet
from django.db.models.query_utils import PathInfo
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import message, send_mail
from vaccine_tracker.settings import DATABASES, EMAIL_HOST_USER
from .decorators import unauthenticated_user, allowed_users, admin_only
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
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm



# Create your views here.
# @login_required(login_url='login')
# @user_passes_test(lambda u: u.is_superuser)
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

            messages.success(request, 'Account has been created for {} {}.'.format(pfname, plname))
        else:
            messages.error(request, patient_form.errors)
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
            messages.success(request, 'Patient details have been saved.')
        else:
            messages.error(request, patient_form.errors)
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

    appointments = Appointment.objects.filter(patient=patient)

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
            messages.error(request, appointment_form.errors)
        return redirect('/appointment/' + pk)

    data = {
        'patient': patient,
        'appointment_form': appointment_form,
        'appointment_form_patient': appointment_form_patient,
        'appointments': appointments,
        'age': age,
    }

    return render(request, 'tracker/appointment.html', data)

@login_required(login_url='login')
def editAppointment(request, pk):
    patient = Patient.objects.get(id=pk)
    appointments = Appointment.objects.filter(patient=patient)

    appointment_formset = forms.modelformset_factory(Appointment, AppointmentForm, extra=0)
    formset = appointment_formset(queryset=appointments)
    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    if(request.method == "POST"):
        formset = appointment_formset(request.POST, queryset=appointments)
        if formset.is_valid():
            for form in formset:
                form.save()
            messages.success(request, 'Appointment saved!')
        else:
            messages.error(request, formset.errors)
        return redirect('/appointment/' + pk)

    data = {
        'patient': patient,
        'formset': formset,
        'appointments': appointments,
        'age': age,
    }

    return render(request, 'tracker/editAppointment.html', data)

def hasPatientUser(request, pk):
    patient = Patient.objects.get(id=pk)
    if PatientUser.objects.get(patient=patient) is None:
        return False
    
    return True


@login_required(login_url='login')
def portal(request, pk):
    patient = Patient.objects.get(id=pk)
    try:
        patient_user = PatientUser.objects.get(patient=patient)
    except PatientUser.DoesNotExist:
        patient_user = None
    patient_user_grp = Group.objects.get(name='Patient User')

    portal_form = PortalForm()
    patient_form = PatientUserForm()
    portal_form_edit = PortalFormEdit()
    
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
        'patient_user': patient_user, 
        'age': age,
        'portal_form': portal_form,
        'patient_form': patient_form,
        'portal_form_edit': portal_form_edit,
    }
    return render(request, 'tracker/portal.html', data)

@login_required(login_url='login')
def portalEdit(request, pk):
    patient = Patient.objects.get(id=pk)

    try:
        patient_user = PatientUser.objects.get(patient=patient)
    except PatientUser.DoesNotExist:
        patient_user = None

    patient_form = PatientUserForm(instance=patient_user)
    portal_form_edit = PortalFormEdit(instance=patient_user.user)

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    if(request.method == "POST"):
        patient_form = PatientUserForm(request.POST, instance=patient_user)
        portal_form_edit = PortalFormEdit(request.POST, instance=patient_user.user)

        if patient_form.is_valid() and portal_form_edit.is_valid():
            patient_form.save()
            portal_form_edit.save()
            messages.success(request, 'Patient Account details have been saved.')
        else:
            messages.error(request, patient_form.errors)

        return redirect('/portal/' + pk)
    
    data = {
        'patient': patient,
        'patient_user': patient_user,
        'patient_form': patient_form,
        'portal_form_edit': portal_form_edit,
        'age': age,
    }

    return render(request, 'tracker/portalEdit.html', data)

@login_required(login_url='login')
def portalEditPass(request, pk):
    patient = Patient.objects.get(id=pk)

    try:
        patient_user = PatientUser.objects.get(patient=patient)
    except PatientUser.DoesNotExist:
        patient_user = None

    password_form = PasswordChangeForm(patient_user.user)

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    if(request.method == "POST"):
        password_form = PasswordChangeForm(patient_user.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Changed!')
        else:
            messages.error(request, password_form.errors)
        
        return redirect('/portal/' + pk)

    data = {
        'patient': patient,
        'patient_user': patient_user,
        'password_form': password_form,
        'age': age,
    }

    return render(request, 'tracker/portalEditPass.html', data)

@login_required(login_url='login')
def certificate(request, pk):
    patient = Patient.objects.get(id=pk)
    cert_date_form = CertDateForm(instance=patient)

    # -- Age (x Years y Months) -- 
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)

    patient.cert_date = curr_date
    patient.age = age

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

    def get_context_data(self, *args, **kwargs):
        patient = self.model 
        patient_birthdate = patient.birthdate
        context = super(PdfDetail, self).get_context_data(*args, **kwargs)

        # curr_date = datetime.date.today()
        # months = curr_date.month - patient_birthdate
        # years = curr_date.year - patient_birthdate

        context['curr_date'] = datetime.date.today()
        # context['age'] = "{} year {} month".format(years, months)

        return context

class PdfDetailPatient(PDFTemplateResponseMixin, DetailView):
    model = Patient
    template_name = 'tracker/pdf_cert_patient.html'
    download_filename = 'Vaccine Certificate of {}-{}'.format(model.last_name, model.first_name)
    context_object_name = 'patient'

    def get_context_data(self, *args, **kwargs):
        patient = self.model 
        patient_birthdate = patient.birthdate
        context = super(PdfDetailPatient, self).get_context_data(*args, **kwargs)

        # curr_date = datetime.date.today()
        # months = curr_date.month - patient_birthdate
        # years = curr_date.year - patient_birthdate

        context['curr_date'] = datetime.date.today()
        # context['age'] = "{} year {} month".format(years, months)

        return context

@login_required(login_url='login')
def vaccine(request, pk):
    patient = Patient.objects.get(id=pk)
    vaccines = PatientVaccine.objects.filter(patient=patient)

    vaccine_form = PatientVaccineForm(request.POST or None, initial={'patient': patient})
    if vaccine_form.is_valid():
        vaccine_form.save()
        messages.success(request, 'Vaccine has been added to {}'.format(patient))
        return redirect('/vaccine/' + pk)
    else:
        messages.error(request, vaccine_form.errors)

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)
    
    data = {
        'patient': patient, 
        'vaccines': vaccines,
        'vaccine_form': vaccine_form,
        'age': age,
    }
    return render(request, 'tracker/vaccine.html', data)

@login_required(login_url='login')
def editVaccine(request, pk):
    patient = Patient.objects.get(id=pk)
    patient_vaccine = PatientVaccine.objects.filter(patient=patient)

    vaccines = []
    for vaccine in patient_vaccine:
        vaccines.append(Vaccine.objects.filter(id=vaccine.vaccine.id))

    vaccine_formset = forms.modelformset_factory(Vaccine, VaccineForm, extra=0)
    formsets = []
    for vaccine in vaccines:
        formsets.append(vaccine_formset(request.POST or None, queryset=vaccine))

    # -- Age (X Years Y Months) --
    curr_date = datetime.date.today()
    months = curr_date.month - patient.birthdate.month
    years = curr_date.year - patient.birthdate.year
    age = "{} year {} month".format(years, months)
    
    data = {
        'patient': patient, 
        'formsets': formsets,
        'vaccines': vaccines,
        'age': age,
    }
    return render(request, 'tracker/editVaccine.html', data)

@login_required(login_url='login')
def report(request):
    vaccines = Vaccine.objects.all()
    physician = Physician.objects.all()

    data = {
        'physician': physician,
    }
    return render(request, 'tracker/report.html', data)

@login_required(login_url='login')
def reminder(request):
    physician = Physician.objects.all()

    data = {
        'physician': physician,
    }
    
    return render(request, 'tracker/reminder.html', data)

@login_required(login_url='login')
def staffUpdate(request):
    physicians = Physician.objects.all()
    doc_grp = Group.objects.get(name='Doctor')
    physicianFilter = PhysicianFilter(request.GET, queryset=physicians)
    physicians = physicianFilter.qs

    data = {
        'physicians': physicians, 'physicianFilter': physicianFilter,
    }

    return render(request, 'tracker/staffUpdate.html', data)

@login_required(login_url='login')
def staffUpdateEdit(request, pk):
    physician = Physician.objects.get(id=pk)
    staff_create_form = StaffUpdateForm(instance=physician.user)
    doc_user_form = DoctorForm(instance=physician)

    if(request.method == "POST"):
        staff_create_form = StaffUpdateForm(request.POST, instance=physician.user)
        doc_user_form = DoctorForm(request.POST, instance=physician)

        if staff_create_form.is_valid() and doc_user_form.is_valid():
            staff_create_form.save()
            doc_user_form.save()
            messages.success(request, 'Staff details have been saved.')
        else:
            messages.error(request, staff_create_form.errors)

        return redirect('/staffUpdate/')
    
    data = {
        'physician': physician,
        'staff_create_form': staff_create_form,
        'doc_user_form': doc_user_form,
    }

    return render(request, 'tracker/staffUpdateEdit.html', data)

@login_required(login_url='login')
def staffUpdateEditPass(request, pk):
    physician = Physician.objects.get(id=pk)
    password_form = PasswordChangeForm(physician.user)

    if(request.method == "POST"):
        password_form = PasswordChangeForm(physician.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Changed!')
        else:
            messages.error(request, password_form.errors)
        
        return redirect('/staffUpdate/')

    data = {
        'physician': physician,
        'password_form': password_form,
    }

    return render(request, 'tracker/staffUpdateEditPass.html', data)


@login_required(login_url='login')
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