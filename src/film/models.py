from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from src.common.models import SeoBlock, Image


# Create your models here.
class Film(models.Model):
  class Choises(models.TextChoices):
    TWO_D = '2D', '2D'
    THREE_D = '3D', '3D'
    IMAX = 'IMAX', 'IMAX'


  name = models.CharField(max_length=225)
  description = models.TextField()
  trailer = models.URLField()
  image = GenericRelation(Image)
  seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)
  type = models.CharField(max_length=10,
                          choices=Choises.choices,
                          default=Choises.TWO_D,
                          verbose_name="Формат фільму")
