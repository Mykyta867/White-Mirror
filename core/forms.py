from django import forms
from .models import Patient, Appointment, Doctor, Service, Discount


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'patronymic', 'phone',
                  'email', 'date_of_birth', 'address', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ім\'я'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Прізвище'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'По батькові'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+380XXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Адреса проживання'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Додаткові примітки...'}),
        }
        labels = {
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
            'patronymic': 'По батькові',
            'phone': 'Телефон',
            'email': 'Email',
            'date_of_birth': 'Дата народження',
            'address': 'Адреса',
            'notes': 'Примітки',
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'service', 'discount',
                  'date', 'time', 'status', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-input'}),
            'doctor': forms.Select(attrs={'class': 'form-input'}),
            'service': forms.Select(attrs={'class': 'form-input'}),
            'discount': forms.Select(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Примітки до запису...'}),
        }
        labels = {
            'patient': 'Пацієнт',
            'doctor': 'Лікар',
            'service': 'Послуга',
            'discount': 'Знижка',
            'date': 'Дата',
            'time': 'Час',
            'status': 'Статус',
            'notes': 'Примітки',
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'patronymic', 'specialization',
                  'phone', 'email', 'experience_years', 'photo', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-input'}),
            'specialization': forms.Select(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
        }


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'discount_type', 'value', 'description',
                  'is_active', 'valid_from', 'valid_to']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'discount_type': forms.Select(attrs={'class': 'form-input'}),
            'value': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'valid_from': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'valid_to': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
