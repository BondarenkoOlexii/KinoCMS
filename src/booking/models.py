from django.db import models
from src.user.models import User
from src.session.models import Session
from src.hall.models import Seat, Hall
# Create your models here.

class Booking(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.BooleanField()
    create_time = models.DateTimeField()