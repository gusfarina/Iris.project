from django.urls import path
from . import views

urlpatterns = [
    path('', views.resumes, name='resumes'),
    path('register-resume', views.register_resume, name='register_resume'),
    path('get_resume', views.get_resume, name='get_resume'),
]
