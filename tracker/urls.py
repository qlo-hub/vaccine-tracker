from collections import namedtuple
from django.urls import path
from . import views

urlpatterns = [

    
    path('home/', views.homePage, name = 'home'),
    path('', views.loginPage, name = 'login'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('logout/', views.logoutUser, name = 'logout'),

    path('notifs/', views.notifsPage, name = 'notifs'),

    path('createRecord/', views.createRecord, name = 'createRecord'),
    path('patient/<str:pk>', views.patient, name = 'patient'),
    path('editPatient/<str:pk>', views.editPatient, name ='editPatient'),
    path('appointment/<str:pk>', views.appointment, name = 'appointment'),
    path('editAppointment/<str:pk>', views.editAppointment, name="editAppointment"),
    path('portal/<str:pk>', views.portal, name = 'portal'), 
    path('portalEdit/<str:pk>', views.portalEdit, name = 'portalEdit'),
    path('portalEditPass/<str:pk>', views.portalEditPass, name = 'portalEditPass'),
    path('certificate/<str:pk>', views.certificate, name='certificate'),
    path('generatepdf/<str:pk>', views.PdfDetail.as_view(), name="generatepdf"),
    path('generatepdfpatient/<str:pk>', views.PdfDetailPatient.as_view(), name="generatepdfpatient"),
    path('vaccine/<str:pk>', views.vaccine, name="vaccine"),
    path('editVaccine/<str:pk>', views.editVaccine, name="editVaccine"),

    path('report/', views.report, name='report'),
    path('reminder/', views.reminder, name='reminder'),
    path('staffUpdate/', views.staffUpdate, name='staffUpdate'),
    path('staffUpdateEdit/<str:pk>', views.staffUpdateEdit, name='staffUpdateEdit'),
    path('staffUpdateEditPass/<str:pk>', views.staffUpdateEditPass, name='staffUpdateEditPass'),
    path('staffCreate/', views.staffCreate, name='staffCreate'),

    path('homePatient/', views.homePagePatient, name = 'homePatient'),
]