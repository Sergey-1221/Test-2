from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import Coin, Main_coin

import requests
import json
import time

from api.views import Data, CandlestickAnalysis

CRYPTOCOMPARE_API = ""


class Page(Data):
    context = {}

    def set_currency(self):
        currency_data, currency_fulldata = self.currency_info()
        self.context["currency"] = currency_data
        self.context["currency_full"] = currency_fulldata
        return self


def price(request, currency):
    page = Page(currency).set_currency()
    page.context["coins"] = page.list_coins_full()
    return render(request, 'main/price.html', page.context)


def index(request):
    return HttpResponseRedirect('/price/USD')


def сharts(request, coin, currency):
    page = Page(currency).set_currency()
    page.context["symbol"] = coin + currency
    return render(request, 'main/сharts.html', page.context)

def coin(request, coin, currency):
    page = Page(currency).set_currency()
    data = page.coin_info(coin)
    page.context["symbol"] = coin + currency
    page.context["coin"] = data["coin"]
    page.context["coin_info"] = data["coin_info"]
    page.context["coin_price"] = data["coin_price"]
    return render(request, 'main/coin-information.html', page.context)

def coin_analytics(request, coin, currency):
    url = request.GET
    page = Page(currency).set_currency()
    data = page.coin_info(coin)
    page.context["symbol"] = coin + currency
    page.context["coin"] = data["coin"]
    page.context["coin_info"] = data["coin_info"]
    page.context["coin_price"] = data["coin_price"]

    time_frame = url.get("time_frame")
    if not time_frame:
        time_frame = "1_hour"

    page.context["time_frame"] = time_frame


    data = page.history_data(coin, time_frame)
    analysis = CandlestickAnalysis(data)
    for x in [10, 20, 50, 100, 200]:
        analysis.SMA(x)
        analysis.EMA(x)
    analysis.WMA(30)

    analysis.CCI(20)
    analysis.RSI(14)
    analysis.STOCH()
    analysis.MACD()
    analysis.WILLR(14)

    oscillators_list = ["CCI", "RSI", "STOCH", "MACD", "WILLR"]
    MA_list = ["SMA", "EMA", "WMA"]

    page.context["data_analysis_MA"] = analysis.format_analysis_value(MA_list)
    page.context["total_analysis_MA"] = analysis.total_analysis_value(MA_list)
    page.context["data_analysis_oscillators"] = analysis.format_analysis_value(oscillators_list)
    page.context["total_analysis_oscillators"] = analysis.total_analysis_value(oscillators_list)
    page.context["total_analysis"] = analysis.total_analysis_value()

    return render(request, 'main/coin-analytics.html', page.context)

def coin_news(request, coin, currency):
    page = Page(currency).set_currency()
    data = page.coin_info(coin)
    page.context["news"] = page.news(coin) + page.news(coin, 2)
    page.context["symbol"] = coin + currency
    page.context["coin"] = data["coin"]
    page.context["coin_info"] = data["coin_info"]
    page.context["coin_price"] = data["coin_price"]
    page.context["news"] = page.context["news"][:-2]

    return render(request, 'main/coin-news.html', page.context)


def charts_none(request, currency):
    page = Page(currency).set_currency()
    page.context["coins"] = page.list_coins_full()
    return render(request, 'main/сharts-none.html', page.context)

def treemap(request, currency):
    page = Page(currency).set_currency()
    return render(request, 'main/treemap.html', page.context)

def greed_and_fear_index(request, currency):
    page = Page(currency).set_currency()
    return render(request, 'main/greed_and_fear_index.html', page.context)
