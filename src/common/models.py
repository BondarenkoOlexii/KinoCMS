from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import ContentType


# Create your models here.
class SeoBlock(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=20)
    keyword = models.CharField(max_length=20)
    description = models.TextField()


class Gallery(models.Model): # Галерея картінок де ми прописуємо кому саме належить вибрана фоточка, наприклад
    photo = models.ImageField(upload_to='')  # Посилання на фоточку


class Image(models.Model):
    IMAGE_TYPES = (                    # Тип картінки
        ('banner', 'Головний банер'),
        ('poster', 'Вертикальний постер'),
        ('gallery', 'Фото галереї'),
        ('promo', 'Промо матеріали'),
    )

    media_file = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey('content_type', 'object_id')

