from django.db import models

class Language(models.TextChoices):
    news = 'ru', 'ru'
    stock = 'uk', 'uk'


class Sex(models.TextChoices):
    news = 'm', 'men'
    stock = 'w', 'women'

class City(models.TextChoices):
    winterfell = 'W', 'Винтерфелл'
    eyrie = 'E', 'Орлиное Гнездо'
    riverrun = 'R', 'Риверран'
    pyke = 'P', 'Пайк'
    casterly_rock = 'C', 'Кастерли Рок'
    sunspear = 'S', 'Солнечное Копьё'
    storms_end = 'S_E', 'Штормовой Предел'
    red_keep = 'R_K', 'Красный Замок'
    highgarden = 'H', 'Хайгарден'
