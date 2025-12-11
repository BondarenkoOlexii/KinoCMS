from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from src.common.models import SeoBlock, Image
# Create your models here.

class NewsStock(models.Model):
    class Type(models.TextChoices):
        news = 'news', 'News'
        stock = 'stock', 'Stock'

    discription = models.TextField()
    image = GenericRelation(Image)
    trailer = models.URLField()
    create_time = models.DateTimeField()
    type = models.CharField(max_length=10, choices=Type.choices)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)