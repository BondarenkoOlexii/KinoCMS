<div align="center">

# 🎬 KinoCMS

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Broker%20%26%20Channels-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-Task%20Queue-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![AdminLTE](https://img.shields.io/badge/AdminLTE-3.x-blue?style=for-the-badge&logo=bootstrap&logoColor=white)](https://adminlte.io/)

<p align="center">
  <b>Веб-платформа для мережі кінотеатрів з кастомною панеллю керування AdminLTE, інтерактивним бронюванням місць та чергами фонових завдань.</b>
</p>

</div>

---

## 📌 Про проєкт

**KinoCMS** — це повнофункціональний веб-сервіс для кінотеатрів, що поєднує публічний портал для глядачів та повністю кастомну адміністративну панель (без використання стандартної `django-admin`).

Платформа дозволяє керувати розкладом, контентом сторінок, банерами та розсилками, а користувачам — переглядати афішу, фільтрувати сеанси та бронювати квитки через інтерактивну схему залу.

---

## ✨ Основний функціонал

### 🍿 Клієнтська частина
* **Афіша та «Скоро у кіно»:** Каталог фільмів у прокаті та очікуваних прем'єр з детальним описом і трейлерами.
* **Розклад сеансів:** Фільтрація фільмів за датами, кінотеатрами, типами залів (2D, 3D, IMAX) та часом.
* **Бронювання місць:** Інтерактивна сітка залу на основі JSON-конфігурації з підтримкою різних типів місць (Standard, Comfort, VIP) та WebSocket-синхронізацією.
* **Тестова оплата:** Симуляція процесу оплати та оформлення квитків на стороні сервера.
* **Кінотеатри та зали:** Інформаційні сторінки кінотеатрів з фотогалереями, описом обладнання та умовами відвідування.
* **Новини та акції:** Спеціальні пропозиції, знижки та події кінотеатру.

### ⚙️ Кастомна панель керування (AdminLTE)
* **Керування фільмами та розкладом:** Додавання сеансів, цін, форматів показу та постерів.
* **Кінотеатри та зали:** Налаштування схеми розташування місць через гнучку JSON-структуру.
* **Банери та брендинг:** Керування головним слайдером, фоновим банером сайту та акційними блоками.
* **Конструктор сторінок:** Редагування статичних і динамічних сторінок сайту («Про нас», «Контакти», «Кафе» тощо).
* **Маркетинг та розсилки:** Масова email-розсилка повідомлень користувачам у фоновому режимі через Celery.
* **Керування користувачами:** База зареєстрованих клієнтів з можливістю редагування профілів.

---

## 🛠 Технологічний стек

* **Бекенд:** Python 3.11+, Django (MVT architecture)
* **Асинхронність & Real-Time:** Django Channels (WebSockets), Celery
* **База даних & Брокер:** PostgreSQL, Redis
* **Фронтенд:** Django Template Language (DTL), HTML5, CSS3, JavaScript (ES6+), jQuery, Bootstrap, AdminLTE 3

---

## 📐 Приклад конфігурації залу (JSON Schema)

Схема розміщення місць і проходів генерується та зберігається у форматі JSON:

```json
{
  "rows": [
    {
      "rowNumber": 1,
      "seats": [
        {"id": "1-1", "type": "standard", "label": "1"},
        {"id": "1-2", "type": "standard", "label": "2"},
        {"isGap": true},
        {"id": "1-3", "type": "standard", "label": "3"},
        {"id": "1-4", "type": "standard", "label": "4"}
      ]
    },
    {
      "rowNumber": 2,
      "seats": [
        {"id": "2-1", "type": "comfort", "label": "1"},
        {"id": "2-2", "type": "comfort", "label": "2"},
        {"isGap": true},
        {"id": "2-3", "type": "vip", "label": "VIP 1"}
      ]
    }
  ]
}
```

---

## 🚀 Встановлення та запуск

### 1. Клонування репозиторію
```bash
git clone [https://github.com/BondarenkoOlexii/KinoCMS.git](https://github.com/BondarenkoOlexii/KinoCMS.git)
cd KinoCMS
```

### 2. Створення віртуального середовища
**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Встановлення залежностей
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Налаштування змінних середовища
Створіть файл `.env` у кореневій папці проєкту:

```env
DEBUG=True
SECRET_KEY=your_secret_django_key
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DB_NAME=kinocms_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Redis & Celery
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
CELERY_BROKER_URL=redis://127.0.0.1:6379/0

# Email settings (для розсилки)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
```

### 5. Застосування міграцій та початкова ініціалізація
Виконайте стандартні міграції та команду `setups` для створення адміністратора й генерації базових сторінок:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py setups
```

### 6. Запуск черги завдань Celery
В окремому терміналі запустіть Celery worker:

```bash
celery -A src worker -l info
```

> **Примітка для Windows:** для Celery може знадобитися прапорець пул-виконання:
> ```bash
> celery -A src worker -l info -P solo
> ```

### 7. Запуск сервера розробки
```bash
python manage.py runserver
```

* **Головна сторінка сайту:** http://127.0.0.1:8000/
* **Панель адміністратора (AdminLTE):** http://127.0.0.1:8000/adminpanel/

---

## 👨‍💻 Автор
**Bondarenko Olexii**

* GitHub: [@BondarenkoOlexii](https://github.com/BondarenkoOlexii)
