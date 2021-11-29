from typing import Text
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.conf import settings
from django.db.models import fields
from django.db.models.fields import files
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import OneToOneRel
from django.forms import ModelForm, widgets
from django.forms.fields import DateField, IntegerField
from django.forms.widgets import *
from .models import *
from django.core.validators import *
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget



class RegisterForm(UserCreationForm):
    last_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'placeholder': 'Last Name..'}))
    first_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'placeholder': 'First Name..'}))
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.',widget=forms.TextInput(attrs={'placeholder': 'Email..'}) )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class PhysicianForm(ModelForm):
    cell_no = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False
    )
    class Meta:
        model = Physician
        fields = "__all__"

class CreateRecordFormPatient(ModelForm):
    cell_no = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False,
    )
    cell_no.widget.attrs = {'class': 'form-control', 'placeholder': '+63'}

    mcontact = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False 
    )
    mcontact.widget.attrs = {'class': 'form-control', 'id': 'mcontact', 'placeholder': '+63'}

    fcontact = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False 
    )
    fcontact.widget.attrs = {'class': 'form-control', 'id': 'fcontact', 'placeholder': '+63'}

    c1contact = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False
    )
    c1contact.widget.attrs = {'class': 'form-control', 'id': 'c1contact', 'placeholder': '+63'}

    c2contact = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False
    )
    c2contact.widget.attrs = {'class': 'form-control', 'id': 'c2contact', 'placeholder': '+63'}

    birthdate = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control', 'id': 'dob', 'placeholder': 'mm-dd-yyyy'},
            format='%m-%d-%Y',
        ),
        input_formats=['%m-%d-%Y']
    )
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'suffix': TextInput(attrs={'class': 'form-control', 'placeholder': 'Suffix'}),
            'nick_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),
            'sex': Select(attrs={'class': 'form-control', 'placeholder': 'Sex'}),
            'age': HiddenInput(attrs={'type': 'hidden'}),

            'username': HiddenInput(attrs={'type': 'hidden'}),
            'relationship': TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'}),

            'cert_date': HiddenInput(attrs={'type': 'hidden'}),
            
            'attending_doctor': Select(attrs={'class': 'form-control', 'placeholder': 'Attending Doctor'}),
            'landline': TextInput(attrs={'class': 'form-control', 'placeholder': 'Home/Landline'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            
            'house_no': TextInput(attrs={'class': 'form-control', 'placeholder': 'House/Unit no/LtBlk/Street'}),
            'barangay': TextInput(attrs={'class': 'form-control', 'placeholder': 'Barangay'}),
            'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'region': TextInput(attrs={'class': 'form-control', 'placeholder': 'Region'}),
            'zip': TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),

            'mfname': TextInput(attrs={'class': 'form-control', 'id': 'mfname', 'placeholder': 'First Name'}),
            'mlname': TextInput(attrs={'class': 'form-control', 'id': 'mlname', 'placeholder': 'Last Name'}),
            'memail': TextInput(attrs={'class': 'form-control', 'id': 'memail', 'placeholder': 'Email'}),

            'ffname': TextInput(attrs={'class': 'form-control', 'id': 'ffname', 'placeholder': 'First Name'}),
            'flname': TextInput(attrs={'class': 'form-control', 'id': 'flname', 'placeholder': 'Last Name'}),
            'femail': TextInput(attrs={'class': 'form-control', 'id': 'femail', 'placeholder': 'Email'}),

            'c1full_name': TextInput(attrs={'class': 'form-control', 'id': 'c1full_name', 'placeholder': 'Full Name'}),
            'relation1': TextInput(attrs={'class': 'form-control', 'id': 'relation1', 'placeholder': 'Relation'}),
            'c2full_name': TextInput(attrs={'class': 'form-control', 'id': 'c2full_name', 'placeholder': 'Full Name'}),
            'relation2': TextInput(attrs={'class': 'form-control', 'id': 'relation2', 'placeholder': 'Relation'}),   
        }

class CertDateForm(ModelForm):
    cert_date = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control', 'id': 'date', 'placeholder': 'mm-dd-yyyy'},
            format='%m-%d-%Y',
        ),
        input_formats=['%m-%d-%Y']
    )
    class Meta:
        model = Patient
        fields = ('cert_date',)

class AppointmentForm(ModelForm):
    date = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control', 'id': 'date', 'placeholder': 'mm/dd/yyyy'},
            format='%m/%d/%Y',
        ),
        input_formats=['%m/%d/%Y']
    )
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'patient': HiddenInput(attrs={'type': 'hidden'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'time': forms.NumberInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Time', 'format': '%I:%M %p'}),
            'doctor': Select(attrs={'class': 'form-control', 'placeholder': 'Doctor'}),
            'visit': TextInput(attrs={'class': 'form-control', 'placeholder': 'Visit'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }

class AppointmentFormPatient(ModelForm):
    date = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control', 'id': 'date', 'placeholder': 'mm/dd/yyyy'},
            format='%m/%d/%Y',
        ),
        input_formats=['%m/%d/%Y']
    )
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'patient': HiddenInput(attrs={'type': 'hidden'}),
            'status': HiddenInput(attrs={'type': 'hidden'}),
            'time': forms.NumberInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Time', 'format': '%I:%M %p'}),
            'doctor': HiddenInput(attrs={'type': 'hidden'}),
            'visit': TextInput(attrs={'class': 'form-control', 'placeholder': 'Visit'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }

class EditAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('status',)
        # widgets = {
        #     'patient': HiddenInput(attrs={'type': 'hidden'}),
        # }

class PortalForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'required': True,}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'required': True,}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required': True}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': True,}),
        }

class PatientUserForm(ModelForm):
    class Meta:
        model = PatientUser
        fields = ('relationship',)
        widgets = {
            'relationship': TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'}),
        }

class PatientVaccineForm(ModelForm):
    LOCATION = (
    ('R thigh', 'R thigh'), ('L thigh', 'L thigh'), ('R arm ', 'R arm'),
    ('L arm', 'L arm'), ('R buttocks', 'R buttocks'), ('L buttocks', 'L buttocks'),
    )
    location = forms.ChoiceField(choices=LOCATION)
    class Meta:
        model = Vaccine
        fields = ('brand', 'date', 'location', 'remarks')
        widgets = {
        #     'brand': TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand'}),
             'date': TextInput(attrs={'placeholder': 'MM/DD/YYYY'})
        #     'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        #     'remarks': TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks'}),
        }

class StaffCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'required': True,}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'required': True,}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required': True}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': True,}),
        }

class DoctorForm(ModelForm):
    CAN_REG = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    date_start = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control', 'id': 'date-start', 'placeholder': 'Date Start (MM/DD/YYYY)'},
            format='%m/%d/%Y',
        ),
        input_formats=['%m/%d/%Y']
    )
    date_end = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control', 'id': 'date-end', 'placeholder': 'Date End (MM/DD/YYYY)'},
            format='%m/%d/%Y',
        ),
        input_formats=['%m/%d/%Y']
    )
    cell_no = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False
    )
    cell_no.widget.attrs = {'class': 'form-control', 'id': 'cell_no', 'placeholder': 'Contact (+63)'}
    can_reg = ChoiceField(choices=CAN_REG, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Can Register?'}))
    class Meta:
        model = Physician
        exclude = ('user', )
        widgets = {
            'prefix': TextInput(attrs={'class': 'form-control', 'placeholder': 'Prefix',}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'doc_type': TextInput(attrs={'class': 'form-control', 'placeholder': 'Type'}), 
        }