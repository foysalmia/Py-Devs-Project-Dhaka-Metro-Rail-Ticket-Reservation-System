from django.db import models

# Create your models here.


class AboutUs(models.Model):
    image = models.ImageField(upload_to='media')
    name = models.CharField(max_length=100)
    descrption = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=12)
    link_user = models.URLField(max_length=200, blank=True)
