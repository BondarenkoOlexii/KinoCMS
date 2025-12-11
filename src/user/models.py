from django.db import models
# Create your models here.

class User(models.Model):
    class Language(models.TextChoices):
        news = 'ru', 'ru'
        stock = 'uk', 'uk'

    class Sex(models.TextChoices):
        news = 'm', 'men'
        stock = 'w', 'women'

    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    user_name = models.CharField(max_length=20, null=True)
    email = models.EmailField()
    real_adress = models.TextField(null=True)
    password = models.CharField(max_length=24)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    language = models.CharField(max_length=2, choices=Language.choices)
    sex = models.CharField(max_length=5, choices=Sex.choices)



