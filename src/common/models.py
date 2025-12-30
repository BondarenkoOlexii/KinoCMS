from django.db import models
from src.adminpanel.models.CommonChoise import CommonType

# Create your models here.
class SeoBlock(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=20)
    keyword = models.CharField(max_length=20)
    description = models.TextField()


class Image(models.Model): # Галерея картінок де ми прописуємо кому саме належить вибрана фоточка, наприклад
    photo = models.ImageField(upload_to='media')  # Посилання на фоточку


class ThourghtImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    image_type = models.CharField(max_length=125, choices=CommonType)

    class Meta:
        abstract = True