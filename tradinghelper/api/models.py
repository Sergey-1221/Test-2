from django.db import models

# Create your models here.
class Currency(models.Model):
	name = models.CharField(max_length=100)
	icon = models.CharField(max_length=1, null=True)
	code = models.CharField(max_length=3)

class Coin(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=5)
	img_src = models.CharField(max_length=255)
