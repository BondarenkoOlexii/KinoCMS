from django.db import models

class Type(models.TextChoices):
    news = 'news', 'News'
    stock = 'stock', 'Stock'