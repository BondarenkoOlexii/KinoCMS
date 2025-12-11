from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from src.common.models import SeoBlock, Image
# Create your models here.

class Cinema(models.Model):
    name = models.CharField(20)
    discription = models.TextField()
    condition = models.TextField()
    image = GenericRelation(Image)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)
