from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from src.common.models import SeoBlock, Image
from src.cinema.models import Cinema
# Create your models here.

class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    description = models.TextField()
    image = GenericRelation(Image)
    seat_count = models.IntegerField()
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)

class Seat(models.Model):
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    row = models.SmallIntegerField()
    seat_num = models.SmallIntegerField()
