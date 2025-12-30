from django.db import models
from django.contrib.auth.models import AbstractUser
from src.adminpanel.models.UserChoise import Language, Sex
# Create your models here.

class User(AbstractUser):
    real_adress = models.TextField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    language = models.CharField(max_length=2, choices=Language.choices)
    sex = models.CharField(max_length=5, choices=Sex.choices)


