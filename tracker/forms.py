from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import ModelForm, widgets
from django.forms.fields import IntegerField
from django.forms.widgets import *
from .models import *
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
    cell_no.widget.attrs = {'class': 'form-control', 'placeholder': 'Mobile Number'}

    mcontact = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False 
    )
    mcontact.widget.attrs = {'class': 'form-control', 'id': 'mcontact', 'placeholder': 'Contact Number'}

    fcontact = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False 
    )
    fcontact.widget.attrs = {'class': 'form-control', 'id': 'fcontact', 'placeholder': 'Contact Number'}

    c1contact = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False
    )
    c1contact.widget.attrs = {'class': 'form-control', 'id': 'c1contact', 'placeholder': 'Contact Number'}

    c2contact = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget, required=False
    )
    c2contact.widget.attrs = {'class': 'form-control', 'id': 'c2contact', 'placeholder': 'Contact Number'}

    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'suffix': TextInput(attrs={'class': 'form-control', 'placeholder': 'Suffix'}),
            'nick_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),
            'age': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'sex': Select(attrs={'class': 'form-control', 'placeholder': 'Sex'}),
            'birthdate': NumberInput(attrs={'type': 'date','class': 'form-control', 'placeholder': 'Date of Birth'}),
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