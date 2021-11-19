from tracker.models import Patient
from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Patient)
admin.site.register(Physician)
admin.site.register(Appointment)
admin.site.register(PatientUser)
admin.site.register(Vaccine)
admin.site.register(PatientVaccine)