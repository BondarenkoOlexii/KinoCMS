from django.db import models
from src.common.models import SeoBlock, Image
from src.adminpanel.models.NewsStocksType import Type
from src.common.models import ThourghtImage
# Create your models here.

class NewsThourghtImage(ThourghtImage):
    images_info = models.ForeignKey('NewsStockModel', on_delete=models.CASCADE)



class NewsStockModel(models.Model):
    class Meta:
        db_table = 'news_newsstock'

    name = models.CharField(max_length=225)
    description = models.TextField()
    image = models.ManyToManyField(Image, through=NewsThourghtImage)
    trailer = models.URLField()
    create_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=Type.choices)
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(null=True)