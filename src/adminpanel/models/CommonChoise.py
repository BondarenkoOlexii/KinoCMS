from django.db import models

class CommonType(models.TextChoices):
    logo = 'logo', 'Логотип'
    stock = 'banner', 'Баннер'
    scheme = 'scheme', 'Схема'
    gallery = 'gallery' 'Галерея Зображень'
