from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from src.common.models import Image

# Create your models here.

class Banner(models.Model):
    class DropBox(models.TextChoices):
        five = '5', '5sec'
        ten = '10', '10sec'
        fifteen = '15', '15sec'
        thirty = '30', '30sec'

    class TypeBanner(models.TextChoices):
        main = 'main', 'main'
        stock = 'stock', 'stock'

    type = models.CharField(max_length=10, choices=TypeBanner.choices)
    url = models.URLField()
    text = models.TextField(null=True)
    speed_button = models.CharField(max_length=10, choices=DropBox.choices)
    image = GenericRelation(Image)
    active = models.BooleanField()


class BackgroundBanner(models.Model):
    is_image = models.BooleanField()
    image = GenericRelation(Image)
    background_color = models.CharField(max_length=10)
