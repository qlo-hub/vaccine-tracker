from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.conf import settings
from django.db.models import fields
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


class AppointmentForm(ModelForm):
    date = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control', 'id': 'date', 'placeholder': 'mm-dd-yyyy'},
            format='%m-%d-%Y',
        ),
        input_formats=['%m-%d-%Y']
    )
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'patient': HiddenInput(attrs={'type': 'hidden'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'time': forms.NumberInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Time'}),
            'doctor': Select(attrs={'class': 'form-control', 'placeholder': 'Doctor'}),
            'visit': TextInput(attrs={'class': 'form-control', 'placeholder': 'Visit'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }

class PortalForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': True,}),
            'password1': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'required': True,}),
            'password2': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'required': True,}),
        }