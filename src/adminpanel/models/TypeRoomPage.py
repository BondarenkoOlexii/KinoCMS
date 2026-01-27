from django.db import models

class TypeRoom(models.TextChoices):
    vip = 'vip', 'VIP'
    child_room = 'child', 'ChildRoom'
    cafe = 'cafe', 'Cafe'
    description = 'description', 'Description',
    stock = 'stock', 'Stock'

