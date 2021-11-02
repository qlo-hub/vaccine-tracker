from collections import namedtuple
from django.urls import path
from . import views

urlpatterns = [

    
    path('home/', views.homePage, name = 'home'),
    path('', views.loginPage, name = 'login'),
    path('register/', views.registerPage, name = 'register'),
    path('logout/', views.logoutUser, name = 'logout'),

    path('notifs/', views.notifsPage, name = 'notifs'),

    path('createRecord/', views.createRecord, name = 'createRecord'),
    path('patient/<str:pk>', views.patient, name = 'patient'),
    path('editPatient/<str:pk>', views.editPatient, name ='editPatient'),
    path('appointment/<str:pk>', views.appointment, name = 'appointment'),
    path('portal/<str:pk>', views.portal, name = 'portal'), 
    path('certificate/<str:pk>', views.certificate, name='certificate'),
    path('generatepdf/<str:pk>', views.PdfDetail.as_view(), name="generatepdf"),

]