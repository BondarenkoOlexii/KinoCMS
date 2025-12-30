from django.db import models

class Language(models.TextChoices):
    news = 'ru', 'ru'
    stock = 'uk', 'uk'


class Sex(models.TextChoices):
    news = 'm', 'men'
    stock = 'w', 'women'