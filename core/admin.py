from django.contrib import admin
from .models import Patient, Doctor, Service, Appointment, Discount


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'phone', 'email', 'created_at']
    search_fields = ['last_name', 'first_name', 'phone', 'email']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'specialization', 'phone', 'experience_years', 'is_active']
    list_filter = ['specialization', 'is_active']
    search_fields = ['last_name', 'first_name']
    list_editable = ['is_active']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration_minutes', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    list_editable = ['is_active', 'price']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'service', 'date', 'time', 'status']
    list_filter = ['status', 'date', 'doctor']
    search_fields = ['patient__last_name', 'doctor__last_name']
    date_hierarchy = 'date'
    list_editable = ['status']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_type', 'value', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['discount_type', 'is_active']
    list_editable = ['is_active']
