from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Physician(models.Model):
    # user = models.OneToOneField(User, limit_choices_to={'groups__name':u'Physician'}, null=True, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    cell_no = PhoneNumberField(null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)

    def __str__(self):
        return self.last_name + ", " + self.first_name + ' - ' + self.specialization
    
    def get_absolute_url(self):
        return reverse('updatePhysician', args=[str(self.pk)])

class Patient(models.Model):
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    suffix = models.CharField(max_length=2, null=True, blank=True)
    nick_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=1, null=True, choices=SEX)
    birthdate = models.DateField(null=True)
    attending_doctor = models.ForeignKey(Physician, related_name="docpatient", on_delete=models.CASCADE)

    # Contact Deets
    cell_no = PhoneNumberField(null=True, blank=True)
    landline = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    
    # Address
    house_no = models.CharField(max_length=100, null=True, blank=True)
    barangay = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    zip = models.IntegerField(null=True, blank=True)
    
    
    # Mother
    mfname = models.CharField(max_length=100, null=True, blank=True)
    mlname = models.CharField(max_length=100, null=True, blank=True)
    mcontact = PhoneNumberField(null=True, blank=True)
    memail = models.EmailField(max_length=254, null=True, blank=True)
    # Father
    ffname = models.CharField(max_length=100, null=True, blank=True)
    flname = models.CharField(max_length=100, null=True, blank=True)
    fcontact = PhoneNumberField(null=True, blank=True)
    femail = models.EmailField(max_length=254, null=True, blank=True)

    c1full_name = models.CharField(max_length=100, null=True, blank=True)
    relation1 = models.CharField(max_length=100, null=True, blank=True)
    c1contact = PhoneNumberField(null=True, blank=True)

    c2full_name = models.CharField(max_length=100, null=True, blank=True)
    relation2 = models.CharField(max_length=100, null=True, blank=True)
    c2contact = PhoneNumberField(null=True, blank=True)
    def __str__(self):
        return self.last_name + ", " + self.first_name