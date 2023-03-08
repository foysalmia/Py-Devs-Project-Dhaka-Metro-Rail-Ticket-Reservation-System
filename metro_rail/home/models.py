from django.db import models

# Create your models here.

class Routes(models.Model):
    name = models.CharField(max_length=20)
    station_no = models.IntegerField(primary_key=True)

class Trips(models.Model):
    passenger = models.CharField(max_length=20)
    from_station = models.CharField(max_length=30)
    to_station = models.CharField(max_length=30)
    date = models.DateField()
    seat_type = models.CharField(max_length=10)
    seat_quantity = models.IntegerField()
    cost = models.IntegerField()

class Train(models.Model):
    pass