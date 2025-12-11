from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from src.common.models import SeoBlock, Image

# Create your models here.
class Page(models.Model):
    class TypeRoom(models.TextChoices):
        vip = 'vip', 'VIP'
        child_room = 'child', 'ChildRoom'
        cafe = 'cafe', 'Cafe'
        description = 'description', 'Description'


    name = models.CharField(max_length=20)
    description = models.TextField()
    image = GenericRelation(Image)
    type = models.CharField(max_length=20, choices=TypeRoom.choices)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)

class MainPage(models.Model):
    number_phone = models.CharField(max_length=20)
    seo_text = models.TextField
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)


class Contacts(models.Model):
    name = models.CharField(225)
    adress = models.TextField()
    coordinate = models.TextField()
    image = GenericRelation(Image)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)