from django.db import models


class FilmChoises(models.TextChoices):
    TWO_D = '2D', '2D'
    THREE_D = '3D', '3D'
    IMAX = 'IMAX', 'IMAX'