from django.contrib import admin

# Register your models here.

from .models import Coin,Main_coin

admin.site.register(Coin) 
admin.site.register(Main_coin)