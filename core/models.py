from django.db import models


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('therapist', 'Терапевт'),
        ('surgeon', 'Хірург'),
        ('orthodontist', 'Ортодонт'),
        ('periodontist', 'Пародонтолог'),
        ('pediatric', 'Дитячий стоматолог'),
        ('orthopedist', 'Ортопед'),
    ]
    first_name = models.CharField('Ім\'я', max_length=100)
    last_name = models.CharField('Прізвище', max_length=100)
    patronymic = models.CharField('По батькові', max_length=100, blank=True)
    specialization = models.CharField('Спеціалізація', max_length=50, choices=SPECIALIZATION_CHOICES)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    photo = models.ImageField('Фото', upload_to='doctors/', blank=True, null=True)
    experience_years = models.IntegerField('Досвід (років)', default=0)
    is_active = models.BooleanField('Активний', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лікар'
        verbose_name_plural = 'Лікарі'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name, self.patronymic]
        return ' '.join(p for p in parts if p).strip()

    @property
    def initials_name(self):
        parts = [self.last_name]
        if self.first_name:
            parts.append(self.first_name[0] + '.')
        if self.patronymic:
            parts.append(self.patronymic[0] + '.')
        return ' '.join(parts)


class Patient(models.Model):
    first_name = models.CharField('Ім\'я', max_length=100)
    last_name = models.CharField('Прізвище', max_length=100)
    patronymic = models.CharField('По батькові', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True)
    date_of_birth = models.DateField('Дата народження', null=True, blank=True)
    address = models.TextField('Адреса', blank=True)
    notes = models.TextField('Примітки', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Пацієнт'
        verbose_name_plural = 'Пацієнти'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name, self.patronymic]
        return ' '.join(p for p in parts if p).strip()

    @property
    def visit_count(self):
        return self.appointments.filter(status='completed').count()

    @property
    def last_visit(self):
        last = self.appointments.filter(status='completed').order_by('-date').first()
        return last.date if last else None


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('therapy', 'Терапія'),
        ('surgery', 'Хірургія'),
        ('orthodontics', 'Ортодонтія'),
        ('prosthetics', 'Протезування'),
        ('hygiene', 'Гігієна'),
        ('diagnostics', 'Діагностика'),
    ]
    name = models.CharField('Назва послуги', max_length=200)
    category = models.CharField('Категорія', max_length=50, choices=CATEGORY_CHOICES, default='therapy')
    description = models.TextField('Опис', blank=True)
    price = models.DecimalField('Ціна (грн)', max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField('Тривалість (хв)', default=30)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} — {self.price} грн'


class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Відсоток (%)'),
        ('fixed', 'Фіксована сума (грн)'),
    ]
    name = models.CharField('Назва знижки', max_length=200)
    discount_type = models.CharField('Тип знижки', max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField('Розмір знижки', max_digits=10, decimal_places=2)
    description = models.TextField('Опис', blank=True)
    is_active = models.BooleanField('Активна', default=True)
    valid_from = models.DateField('Діє з', null=True, blank=True)
    valid_to = models.DateField('Діє до', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Знижка'
        verbose_name_plural = 'Знижки'
        ordering = ['-created_at']

    def __str__(self):
        if self.discount_type == 'percentage':
            return f'{self.name} ({self.value}%)'
        return f'{self.name} ({self.value} грн)'

    @property
    def display_value(self):
        if self.discount_type == 'percentage':
            return f'{self.value}%'
        return f'{self.value} грн'


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('in_progress', 'В процесі'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    ]
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE,
        related_name='appointments', verbose_name='Пацієнт'
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE,
        related_name='appointments', verbose_name='Лікар'
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name='Послуга'
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Знижка'
    )
    date = models.DateField('Дата')
    time = models.TimeField('Час')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField('Примітки', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Запис'
        verbose_name_plural = 'Записи'
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.patient} — {self.doctor} ({self.date})'

    @property
    def final_price(self):
        price = self.service.price
        if self.discount:
            if self.discount.discount_type == 'percentage':
                price = price * (1 - self.discount.value / 100)
            else:
                price = price - self.discount.value
        return max(price, 0)

    @property
    def status_color(self):
        colors = {
            'pending': 'warning',
            'in_progress': 'info',
            'completed': 'success',
            'cancelled': 'danger',
        }
        return colors.get(self.status, 'secondary')
