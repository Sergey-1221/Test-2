"""tradecoin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main.views import *
from api.views import Api

urlpatterns = [
    path('', index),
    path('price/<currency>/', price),
    path('chart/<coin>/<currency>/', сharts),
    path('coin/<coin>/<currency>/', coin),
    path('coin/<coin>/<currency>/information', coin),
    path('coin/<coin>/<currency>/analytics', coin_analytics),
    path('coin/<coin>/<currency>/news', coin_news),
    path('charts/<currency>/', charts_none),
    path('treemap/<currency>/', treemap),
    path('greed-and-fear-index/<currency>/', greed_and_fear_index),

    path('admin/', admin.site.urls),
    path('api/treemap/<currency>/', Api.treemap),
    path('api/fear_and_greed_index/<limit>', Api.fear_and_greed_index),
    path('api/fear_and_greed_index/', Api.fear_and_greed_index),
    path('api/history/candlestick/<coin>/<currency>/', Api.history_data)
]
