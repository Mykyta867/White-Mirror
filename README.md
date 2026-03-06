# 🦷 White-Mirror — Адмін-панель стоматологічної клініки

Django-based CRM система для управління стоматологічною клінікою.

## Стек
- **Backend:** Django 4.2
- **Database:** SQLite (можна замінити на PostgreSQL)
- **Frontend:** HTML + CSS (без фреймворків)
- **Шрифти:** Manrope + Inter (Google Fonts)

## Функціонал

| Сторінка | Можливості |
|----------|-----------|
| Головна | Статистика, останні записи |
| Пацієнти | Список, пошук, додавання, картка пацієнта |
| Картка пацієнта | Інфо, історія прийомів, запис на прийом |
| Записи | Таблиця всіх записів, фільтри по статусу, зміна статусу |
| Лікарі | Картки лікарів, профіль, активація/деактивація |
| Розклад | Тижневий вид прийомів, навігація по тижнях |
| Знижки | Управління знижками, активація/деактивація |

## Встановлення

```bash
# 1. Клонувати репозиторій
git clone <repo-url>
cd dental_crm

# 2. Створити та активувати venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Встановити залежності
pip install -r requirements.txt

# 4. Міграції
python manage.py migrate

# 5. Завантажити тестові дані (опційно)
python manage.py seed_data

# 6. Створити суперкористувача
python manage.py createsuperuser

# 7. Запустити сервер
python manage.py runserver
```

Відкрити в браузері: http://127.0.0.1:8000/

Django Admin: http://127.0.0.1:8000/admin/

## Структура проекту

```
White-Mirror/
├── White-Mirror/          # Налаштування Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                # Основний додаток
│   ├── models.py        # Моделі: Doctor, Patient, Service, Appointment, Discount
│   ├── views.py         # В'юшки для всіх сторінок
│   ├── urls.py          # URL маршрути
│   ├── forms.py         # Django форми
│   ├── admin.py         # Django Admin
│   └── management/
│       └── commands/
│           └── seed_data.py  # Команда для тестових даних
├── templates/           # HTML шаблони
│   ├── base.html        # Базовий шаблон з sidebar
│   ├── dashboard.html
│   ├── patients/
│   ├── appointments/
│   ├── doctors/
│   ├── schedule/
│   └── discounts/
├── static/
│   ├── css/style.css    # Всі стилі
│   └── js/main.js       # JS для модальних вікон
├── media/               # Завантажені файли (фото лікарів)
├── .gitignore
├── requirements.txt
└── README.md
```

## Моделі бази даних

- **Doctor** — лікарі клініки (ПІБ, спеціалізація, досвід, фото)
- **Patient** — пацієнти (ПІБ, телефон, email, дата народження)
- **Service** — послуги клініки (назва, ціна, тривалість)
- **Discount** — знижки (відсоткові та фіксовані)
- **Appointment** — записи на прийом (зв'язок між пацієнтом, лікарем, послугою)
