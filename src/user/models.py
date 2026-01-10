from django.db import models
from django.contrib.auth.models import AbstractUser
from src.adminpanel.models.UserChoise import Language, Sex, City
from django.core.validators import RegexValidator

# Create your models here.

phone_validator = RegexValidator(r'\+380\d{9}$')

class User(AbstractUser):
    real_adress = models.TextField(null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[phone_validator], unique=True)
    city = models.CharField(max_length=20, null=True, choices=City, default=City.choices[0][0])
    date_of_birth = models.DateField(null=True)
    language = models.CharField(max_length=2, choices=Language.choices, default=Language.choices[0][0])
    sex = models.CharField(max_length=5, choices=Sex.choices, default=Sex.choices[0][0])
    credit_card = models.CharField(max_length=16, unique=True)
    


