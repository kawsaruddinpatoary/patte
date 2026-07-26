from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('team-details/', views.teamDetails, name='team-details'),
    path('working-process/', views.workingProcess, name='working-process'),
    path('history', views.history, name='history'),
]
