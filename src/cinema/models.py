from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from src.common.models import SeoBlock, Image
from src.adminpanel.models.FilmChoise import FilmChoises
from src.user.models import User
from src.common.models import ThourghtImage
# Create your models here.

class CinemaThourghtImage(ThourghtImage):
    images_info = models.ForeignKey('Cinema', on_delete=models.CASCADE)

class HallThourghtImage(ThourghtImage):
    images_info = models.ForeignKey('Hall', on_delete=models.CASCADE)
class FilmThourghtImage(ThourghtImage):
    images_info = models.ForeignKey('Film', on_delete=models.CASCADE)


class Cinema(models.Model):
    name = models.CharField(20)
    discription = models.TextField()
    condition = models.TextField()
    image = models.ManyToManyField(Image, through=CinemaThourghtImage)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)


class Film(models.Model):

  name = models.CharField(max_length=225)
  description = models.TextField()
  trailer = models.URLField()
  start_time = models.DateTimeField()
  image = models.ManyToManyField(Image, through=FilmThourghtImage)
  seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)
  type = models.CharField(max_length=10,
                          choices=FilmChoises.choices,
                          default=FilmChoises.TWO_D,
                          verbose_name="Формат фільму")

class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    description = models.TextField()
    image = models.ManyToManyField(Image, through=HallThourghtImage)
    seat_count = models.IntegerField(null=True)
    create_data = models.DateTimeField(auto_now_add=True)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)

class Seat(models.Model):
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    row = models.SmallIntegerField()
    seat_num = models.SmallIntegerField()


class Session(models.Model):
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)
    day = models.DateField()
    start_time = models.TimeField()
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Booking(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.BooleanField()
    create_time = models.DateTimeField()