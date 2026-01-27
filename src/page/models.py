from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from src.common.models import SeoBlock, ThourghtImage, Image
from src.adminpanel.models.BannerChoise import TypeBanner, DropBox
from src.adminpanel.models.TypeRoomPage import TypeRoom
from django.core.validators import RegexValidator
# Create your models here.

#-----------------------------------------------------------------------------------------

phone_validator = RegexValidator(r'\+380\d{9}$')


class PageThourghtImage(ThourghtImage):
    images_info = models.ForeignKey('Page', on_delete=models.CASCADE)
class ContactThourghtImage(ThourghtImage):
    images_info = models.ForeignKey('Contacts', on_delete=models.CASCADE)
class BannerThourghtImage(ThourghtImage):
    images_info = models.ForeignKey('Banner', on_delete=models.CASCADE)
    url = models.URLField()
    text = models.TextField(null=True)
class BackBannerThourghtImage(ThourghtImage):
    images_info = models.ForeignKey('BackgroundBanner', on_delete=models.CASCADE)


#-----------------------------------------------------------------------------------------

class Page(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    data_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image = models.ManyToManyField(Image, through=PageThourghtImage)
    type = models.CharField(max_length=20, choices=TypeRoom.choices)
    is_active = models.BooleanField(null=True)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)

class MainPage(models.Model):
    name = models.CharField(default='Главная страница', null=True, blank=True)
    data_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    number_phone = models.CharField(max_length=20, null=True, blank=True, validators=[phone_validator], unique=True)
    seo_text = models.TextField(blank=True, null=True)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)


class Contacts(models.Model):
    name = models.CharField(225)
    adress = models.TextField()
    coordinate = models.TextField()
    image = models.ManyToManyField(Image, through=ContactThourghtImage)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)

#Banner --------------------------------------------------------------------------------------
class Banner(models.Model):
    type = models.CharField(max_length=10, choices=TypeBanner.choices, default=TypeBanner.choices[0][0])
    speed_button = models.CharField(max_length=10, choices=DropBox.choices, default=DropBox.choices[0][0])
    image = models.ManyToManyField(Image, through=BannerThourghtImage)
    active = models.BooleanField(default=True)


class BackgroundBanner(models.Model):
    is_image = models.BooleanField()
    image = models.ManyToManyField(Image, through=BackBannerThourghtImage)
    background_color = models.CharField(max_length=10)
