from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:pk>/status/', views.appointment_update_status, name='appointment_update_status'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),

    # Doctors
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:pk>/toggle/', views.doctor_toggle_active, name='doctor_toggle_active'),

    # Schedule
    path('schedule/', views.schedule, name='schedule'),

    # Discounts
    path('discounts/', views.discount_list, name='discount_list'),
    path('discounts/<int:pk>/toggle/', views.discount_toggle, name='discount_toggle'),
    path('discounts/<int:pk>/delete/', views.discount_delete, name='discount_delete'),
]
