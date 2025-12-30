from django.db import models

class DropBox(models.TextChoices):
    five = '5', '5sec'
    ten = '10', '10sec'
    fifteen = '15', '15sec'
    thirty = '30', '30sec'


class TypeBanner(models.TextChoices):
    main = 'main', 'main'
    stock = 'stock', 'stock'