from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('ask-questions/', views.ask_questions, name='ask_questions'),
    path('physics/', views.physics, name='physics'),
    path('feedback/', views.feedback, name='feedback'),
]
