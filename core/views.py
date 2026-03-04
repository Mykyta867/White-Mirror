from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Sum
from datetime import date, timedelta
from .models import Patient, Doctor, Appointment, Service, Discount
from .forms import PatientForm, AppointmentForm, DoctorForm, DiscountForm


# ─────────────────────────── DASHBOARD ───────────────────────────
def dashboard(request):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    context = {
        'active_page': 'dashboard',
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.filter(is_active=True).count(),
        'today_appointments': Appointment.objects.filter(date=today).count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'recent_appointments': Appointment.objects.select_related(
            'patient', 'doctor', 'service'
        ).order_by('-date', '-time')[:8],
        'week_appointments': Appointment.objects.filter(
            date__gte=week_start,
            date__lte=week_start + timedelta(days=6)
        ).count(),
    }
    return render(request, 'dashboard.html', context)


# ─────────────────────────── PATIENTS ───────────────────────────
def patient_list(request):
    q = request.GET.get('q', '').strip()
    patients = Patient.objects.all()
    if q:
        patients = patients.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(patronymic__icontains=q) |
            Q(phone__icontains=q) |
            Q(email__icontains=q)
        )

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()

    return render(request, 'patients/list.html', {
        'patients': patients,
        'form': form,
        'q': q,
        'active_page': 'patients',
    })


def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.select_related(
        'doctor', 'service', 'discount'
    ).order_by('-date', '-time')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = patient
            appt.save()
            return redirect('patient_detail', pk=pk)
    else:
        form = AppointmentForm(initial={'patient': patient})

    return render(request, 'patients/detail.html', {
        'patient': patient,
        'appointments': appointments,
        'form': form,
        'active_page': 'patients',
        'doctors': Doctor.objects.filter(is_active=True),
        'services': Service.objects.filter(is_active=True),
        'discounts': Discount.objects.filter(is_active=True),
    })


def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', pk=pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/edit.html', {
        'form': form,
        'patient': patient,
        'active_page': 'patients',
    })


def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return redirect('patient_detail', pk=pk)


# ─────────────────────────── APPOINTMENTS ───────────────────────────
def appointment_list(request):
    appointments = Appointment.objects.select_related(
        'patient', 'doctor', 'service', 'discount'
    ).order_by('-date', '-time')

    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)

    date_filter = request.GET.get('date', '')
    if date_filter:
        appointments = appointments.filter(date=date_filter)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/list.html', {
        'appointments': appointments,
        'form': form,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'active_page': 'appointments',
        'status_choices': Appointment.STATUS_CHOICES,
    })


def appointment_update_status(request, pk):
    if request.method == 'POST':
        appt = get_object_or_404(Appointment, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appt.status = new_status
            appt.save()
    return redirect(request.POST.get('next', 'appointment_list'))


def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appt.delete()
    return redirect('appointment_list')


# ─────────────────────────── DOCTORS ───────────────────────────
def doctor_list(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()

    return render(request, 'doctors/list.html', {
        'doctors': doctors,
        'form': form,
        'active_page': 'doctors',
    })


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = doctor.appointments.select_related(
        'patient', 'service'
    ).order_by('-date', '-time')[:20]
    return render(request, 'doctors/detail.html', {
        'doctor': doctor,
        'appointments': appointments,
        'active_page': 'doctors',
    })


def doctor_toggle_active(request, pk):
    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor.is_active = not doctor.is_active
        doctor.save()
    return redirect('doctor_list')


# ─────────────────────────── SCHEDULE ───────────────────────────
def schedule(request):
    today = date.today()
    # Get week offset from query param
    offset = int(request.GET.get('week', 0))
    week_start = today - timedelta(days=today.weekday()) + timedelta(weeks=offset)
    week_end = week_start + timedelta(days=6)

    appointments = Appointment.objects.filter(
        date__gte=week_start,
        date__lte=week_end
    ).select_related('patient', 'doctor', 'service').order_by('date', 'time')

    days = [week_start + timedelta(days=i) for i in range(7)]
    schedule_data = {d: list(appointments.filter(date=d)) for d in days}

    day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    days_with_names = list(zip(days, day_names))

    return render(request, 'schedule/index.html', {
        'schedule_data': schedule_data,
        'days': days,
        'days_with_names': days_with_names,
        'week_start': week_start,
        'week_end': week_end,
        'today': today,
        'offset': offset,
        'prev_offset': offset - 1,
        'next_offset': offset + 1,
        'active_page': 'schedule',
    })


# ─────────────────────────── DISCOUNTS ───────────────────────────
def discount_list(request):
    discounts = Discount.objects.all()

    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discount_list')
    else:
        form = DiscountForm()

    return render(request, 'discounts/list.html', {
        'discounts': discounts,
        'form': form,
        'active_page': 'discounts',
    })


def discount_toggle(request, pk):
    if request.method == 'POST':
        discount = get_object_or_404(Discount, pk=pk)
        discount.is_active = not discount.is_active
        discount.save()
    return redirect('discount_list')


def discount_delete(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    if request.method == 'POST':
        discount.delete()
    return redirect('discount_list')
