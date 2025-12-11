from django.db import models
from src.film.models import Film
from src.hall.models import Hall
# Create your models here.

class Session(models.Model):
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)
    day = models.DateField()
    start_time = models.TimeField()
    price = models.DecimalField('грн')
