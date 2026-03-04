"""
Management command to populate the database with sample data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time, timedelta
import random

from core.models import Doctor, Patient, Service, Discount, Appointment


class Command(BaseCommand):
    help = 'Seed the database with sample dental clinic data'

    def handle(self, *args, **options):
        self.stdout.write('🦷 Seeding Dental CRM database...\n')

        # Doctors
        doctors_data = [
            ('Іваненко', 'Олексій', 'Петрович', 'therapist', '+380501234567', 12),
            ('Коваленко', 'Марія', 'Іванівна', 'orthodontist', '+380671234568', 8),
            ('Петренко', 'Василь', 'Михайлович', 'surgeon', '+380931234569', 15),
            ('Сидоренко', 'Олена', 'Василівна', 'periodontist', '+380661234570', 6),
            ('Бондаренко', 'Андрій', 'Сергійович', 'pediatric', '+380991234571', 10),
        ]
        doctors = []
        for last, first, pat, spec, phone, exp in doctors_data:
            doc, _ = Doctor.objects.get_or_create(
                last_name=last, first_name=first,
                defaults={'patronymic': pat, 'specialization': spec, 'phone': phone, 'experience_years': exp}
            )
            doctors.append(doc)
        self.stdout.write(f'  ✅ Created {len(doctors)} doctors')

        # Services
        services_data = [
            ('Консультація', 'diagnostics', 300, 30),
            ('Лікування карієсу', 'therapy', 800, 60),
            ('Видалення зуба', 'surgery', 600, 45),
            ('Відбілювання зубів', 'hygiene', 2000, 90),
            ('Брекет-система', 'orthodontics', 15000, 60),
            ('Коронка металокерамічна', 'prosthetics', 3500, 60),
            ('Чищення зубного каменю', 'hygiene', 500, 45),
            ('Рентген зуба', 'diagnostics', 150, 10),
            ('Пломба', 'therapy', 650, 50),
            ('Імплант', 'surgery', 12000, 90),
        ]
        services = []
        for name, cat, price, dur in services_data:
            svc, _ = Service.objects.get_or_create(
                name=name, defaults={'category': cat, 'price': price, 'duration_minutes': dur}
            )
            services.append(svc)
        self.stdout.write(f'  ✅ Created {len(services)} services')

        # Discounts
        discounts_data = [
            ('Пенсіонер', 'percentage', 15, 'Знижка для пенсіонерів'),
            ('Студент', 'percentage', 10, 'Знижка для студентів'),
            ('Постійний клієнт', 'percentage', 20, 'Для пацієнтів від 10 візитів'),
            ('Перший візит', 'fixed', 100, 'Знижка на перший прийом'),
            ('Сімейна', 'percentage', 12, 'Для членів родини'),
        ]
        discounts = []
        for name, dtype, val, desc in discounts_data:
            disc, _ = Discount.objects.get_or_create(
                name=name, defaults={'discount_type': dtype, 'value': val, 'description': desc}
            )
            discounts.append(disc)
        self.stdout.write(f'  ✅ Created {len(discounts)} discounts')

        # Patients
        patients_data = [
            ('Мельник', 'Тетяна', 'Олегівна', '+380501111111', 'tmelnik@gmail.com'),
            ('Гриценко', 'Микола', 'Андрійович', '+380672222222', ''),
            ('Шевченко', 'Оксана', 'Василівна', '+380933333333', 'oksana@ukr.net'),
            ('Кравченко', 'Дмитро', 'Іванович', '+380664444444', ''),
            ('Лисенко', 'Наталія', 'Петрівна', '+380995555555', 'nat.lysenko@gmail.com'),
            ('Романенко', 'Артем', 'Сергійович', '+380506666666', ''),
            ('Дорошенко', 'Ірина', 'Михайлівна', '+380677777777', 'irina.d@mail.ua'),
            ('Ткаченко', 'Сергій', 'Вікторович', '+380938888888', ''),
        ]
        patients = []
        for last, first, pat, phone, email in patients_data:
            p, _ = Patient.objects.get_or_create(
                last_name=last, first_name=first,
                defaults={'patronymic': pat, 'phone': phone, 'email': email}
            )
            patients.append(p)
        self.stdout.write(f'  ✅ Created {len(patients)} patients')

        # Appointments
        today = date.today()
        statuses = ['pending', 'pending', 'completed', 'completed', 'completed', 'in_progress', 'cancelled']
        appt_count = 0

        for i in range(30):
            day_offset = random.randint(-14, 7)
            appt_date = today + timedelta(days=day_offset)
            appt_time = time(random.randint(9, 17), random.choice([0, 15, 30, 45]))
            status = 'completed' if day_offset < 0 else ('pending' if day_offset > 0 else random.choice(['pending', 'in_progress']))

            Appointment.objects.create(
                patient=random.choice(patients),
                doctor=random.choice(doctors),
                service=random.choice(services),
                discount=random.choice([None, None, None] + discounts),
                date=appt_date,
                time=appt_time,
                status=status,
            )
            appt_count += 1

        self.stdout.write(f'  ✅ Created {appt_count} appointments')
        self.stdout.write(self.style.SUCCESS('\n✅ Done! Database seeded successfully.'))
        self.stdout.write('  Run: python manage.py runserver')
