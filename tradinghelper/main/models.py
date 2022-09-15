from django.db import models

# Create your models here.


class Coin(models.Model):
	name = models.CharField(max_length=50)
	code = models.CharField(max_length=4)

class Main_coin(models.Model):
	name = models.CharField(max_length=50)
	icon = models.CharField(max_length=1,null=True)
	code = models.CharField(max_length=3)