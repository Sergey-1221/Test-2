from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

import json
import time
import numpy as np
import pandas as pd
import talib

import requests
from bs4 import BeautifulSoup
from .models import Currency,Coin

def reduction_num(num):
	if  num > 1000000000000000:
		return "{:e}".format(num)
	elif num > 1000000000000:
		return str(float('{:.2f}'.format(num/1000000000)))+" T"
	elif num > 1000000000:
		return str(float('{:.2f}'.format(num/1000000000)))+" B"
	elif num > 1000000:
		return str(float('{:.2f}'.format(num/1000000)))+" M"
	else:
		return round(num)

def format_num(num,symbol=""):
	if 0 > num:
		symbol = "-"+symbol
		num = abs(num)

	if num > 1000000:
		num = reduction_num(num)
	elif num >= 10000:
		num = '{0:,}'.format(round(num, 2))
	elif num > 10:
		num = round(num, 4)
	else:
		num = round(num, 7)

	return symbol+str(num)

def Cryptocompare(path):
		CRYPTOCOMPARE_API = ""
		url = "https://min-api.cryptocompare.com/" + path + "&api_key=" + CRYPTOCOMPARE_API
		response = requests.get(url)
		if response.status_code == 200:
			response = response.json()
			if "Response" in response:
				if response["Response"] == "Error":
					return False
			return response
		return False

class Data:
	global Coin,Currency
	def __init__(self, currency):
		self.currency = currency
		self.currency_data = False

	def currency_info(self):
		currency_data = Currency.objects.filter(code=self.currency).values()[0]
		currency_fulldata = Currency.objects.all().values()
		currency_fulldata_1 = []
		for x in currency_fulldata:
			if x["code"] != currency_data["code"]:
				currency_fulldata_1.append(x)

		currency_data = Currency.objects.filter(code=self.currency).values()[0]
		self.currency_data = currency_data

		return currency_data, currency_fulldata_1

	def cryptocompare_format_price(self,data):
		if type(self.currency_data) == bool:
			self.currency_info()
		else:
			symbol = self.currency_data['icon']
			new_data = {
				"change_24h": format_num(data["CHANGE24HOUR"],symbol),
				"change_procent_24h": float('{:.2f}'.format(data["CHANGEPCT24HOUR"])),
				"price": format_num(data["PRICE"], symbol),
				"capitalization": format_num(data["MKTCAP"], symbol),
				"volume_24h":  format_num(data["TOTALVOLUME24HTO"], symbol),
				"open_24h": format_num(data["OPEN24HOUR"], symbol),
				"high_24h": format_num(data["HIGH24HOUR"], symbol),
				"low_24h": format_num(data["LOW24HOUR"], symbol)
			}
			new_data["change_24h_type"] = "long" if new_data["change_procent_24h"] > 0 else "short"
			return new_data

	def coin(self, coin):
		coin_obj = Coin.objects.filter(code=coin).values()

		if len(coin_obj) == 0:
			data = Cryptocompare("data/top/exchanges/full?fsym=" + coin + "&tsym=USD")
			if data:
				coin_obj = Coin()
				coin_obj.name = data["Data"]["CoinInfo"]["FullName"]
				coin_obj.code = coin
				coin_obj.img_src = "https://cryptocompare.com/" + data["Data"]["CoinInfo"]["ImageUrl"]
				coin_obj.save()
				return self.coin(coin)


		coin_obj = list(coin_obj)[0]
		coin_obj["pair"] = coin.upper() + "/" + self.currency.upper()
		return coin_obj

	def coin_info(self, coin):
		coin_min_data = self.coin(coin)

		coin_price = Cryptocompare("data/pricemultifull?fsyms=" + coin + "&tsyms=" + self.currency)
		coin_price = self.cryptocompare_format_price(coin_price["RAW"][coin][self.currency])

		coin_info = Cryptocompare("data/top/exchanges/full?fsym=" + coin + "&tsym=" + self.currency)
		coin_info = coin_info["Data"]["CoinInfo"]
		coin_info["NetHashesPerSecond"] = reduction_num(coin_info["NetHashesPerSecond"])
		coin_info["MaxSupply"] = reduction_num(coin_info["MaxSupply"])
		coin_info["TotalCoinsMined"] = reduction_num(coin_info["TotalCoinsMined"])

		return {"coin": coin_min_data,
				"coin_info": coin_info,
				"coin_price": coin_price}

	def news(self, coin, page=1):
		start = 10 * (page - 1)
		query = coin
		url = f'https://www.google.com/search?q={query}&start={start}&tbm=nws&lr=lang_ru'

		r = requests.get(url)

		soup = BeautifulSoup(r.text, 'lxml')

		blocks = soup.find(id="main").find_all("a")
		blocks = blocks[15:-6] if start == 0 else blocks[15:-7]

		news_data = []
		for block in blocks:
			title = block.find("h3").text
			url = block["href"].split("?q=")[1].split("&")[0]
			url_name = block.find(class_="UPmit").text
			discription = block.find_all(class_="BNeawe")[3]
			date = discription.span.text
			discription.span.decompose()
			discription = discription.text

			news_data.append({
				"title": title,
				"url": url,
				"url_name": url_name,
				"date": date,
				"description": discription
			})
		return news_data

	def list_coins_full(self):
		response = Cryptocompare("data/top/totalvolfull?tsym=" + self.currency + "&page=0&limit_toplist=100&limit=100")["Data"]
		coins = []

		for coin in response:
			try:

				array = self.cryptocompare_format_price(coin['RAW'][self.currency])
				array["chart_img"] = 'https://images.cryptocompare.com/sparkchart/' + coin['CoinInfo']['Name'] + '/USD/latest.png?ts=' + str(time.time())
				array["name"] = coin['CoinInfo']['Name']
				array["FullName"] = coin['CoinInfo']['FullName']
				array["icon"] = coin['CoinInfo']['ImageUrl']

				coins.append(array)
			except:
				pass

		return coins

	def history_data(self, coin, time_frame="1_hour", candle=200, time_interval=""):
		aggregate, time_value = time_frame.split("_")
		data = Cryptocompare(f"data/v2/histo{time_value}?tsym={self.currency}&fsym={coin}&aggregate={aggregate}&limit={candle}")["Data"]["Data"]
		return data

	def treemap_json(self, url_get):
		currency = self.currency
		data = Cryptocompare("data/top/totalvolfull?tsym=" + self.currency + "&page=0&limit_toplist=100&limit=100")["Data"]
		get_format_bool = url_get.get("format") in ["rating", "technology", "proof_type"]
		if get_format_bool:
			data_1 = {}
		else:
			data_1 = []

		for x in range(0, len(data)):
			arr = {}
			#
			arr["name"] = data[x]["CoinInfo"]["Name"]
			arr["link"] = "/coin/" + data[x]["CoinInfo"]["Name"] + "/" + currency
			# data[x]["icon"] = "https://cryptocompare.com"+data[x]["CoinInfo"]["ImageUrl"]
			arr["id"] = "coin_" + str(x)

			try:
				arr["coin_info"] = {
					"price": data[x]['DISPLAY'][currency]["PRICE"],
					"name": data[x]['CoinInfo']["FullName"],
					"icon": "https://www.cryptocompare.com" + data[x]['CoinInfo']["ImageUrl"],
					"capitalization": data[x]['DISPLAY'][currency]["MKTCAP"],
					"chart_img": 'https://images.cryptocompare.com/sparkchart/' + arr[
						"name"] + '/' + currency + '/latest.png?ts=' + str(time.time()),
				}

				value = data[x]['RAW'][currency]["TOTALVOLUME24HTO"] if url_get.get("size") == "value_traded" else \
					data[x]['RAW'][currency]["MKTCAP"]
				arr["value_name"] = "Объем торгов" if url_get.get("size") == "value_traded" else "Капитализация"
				arr["value"] = [
					value,
					data[x]['RAW'][currency]["VOLUME24HOUR"],
					data[x]['RAW'][currency]["CHANGEPCT24HOUR"]
				]
				if get_format_bool:
					if url_get.get("format") == "rating":
						rating_format = data[x]["CoinInfo"]["Rating"]["Weiss"]["Rating"]
						if rating_format == "":
							rating_format = "N/A"
					elif url_get.get("format") == "technology":
						rating_format = data[x]["CoinInfo"]["Algorithm"]

					elif url_get.get("format") == "proof_type":
						rating_format = data[x]["CoinInfo"]["ProofType"]

					if rating_format in data_1:
						data_1[rating_format]["children"].append(arr)
						data_1[rating_format]["value"][0] += value
					else:
						data_1[rating_format] = {}
						data_1[rating_format]["name"] = rating_format
						data_1[rating_format]["children"] = []
						data_1[rating_format]["value"] = [value, None, None]
						data_1[rating_format]["children"].append(arr)
				else:
					data_1.append(arr)
				# data[x]["value"] = [data[x]['RAW'][currency]["MKTCAP"],data[x]['RAW'][currency]["VOLUME24HOUR"],data[x]['RAW'][currency]["CHANGEPCT24HOUR"],None]
				pass
			except:
				pass
		# data[x]["value"] = [0,None,None]

		if get_format_bool:
			data_1 = list(data_1.values())

		return json.dumps(data_1)


class CandlestickAnalysis:
	status = {
		-2: "Активно продавать",
		-1: "Продавать",
		0: "Нейтрально",
		1: "Покупать",
		2: "Активно покупать"
	}
	indicator_name = {
		"SMA": "Простое скользящее среднее",
		"EMA": "Экспоненциальное скользящее среднее",
		"WMA": "Взвешенное скользящее среднее",
		"CCI": "Индекс товарного канала",
		"RSI": "Индекс относительной силы",
		"STOCH": "Cтохастик",
		"STOCHRSI": "Стохастический индекс относительной силы",
		"MACD": "Уровень MACD",
		"WILLR": "Процентный диапазон Вильямса"

	}

	def __init__(self, data):
		self.data = pd.DataFrame(data)
		self.data.set_index(['time'], inplace=True)
		self.data_close = self.data["close"].values
		self.data_high = self.data["high"].values
		self.data_low = self.data["low"].values
		self.value = self.data["close"].values[-1]
		self.analysis = {}
		self.analysis_value = {}

	def SMA(self, timeperiod):
		self.analysis[f"SMA_{timeperiod}"] = talib.SMA(self.data_close, timeperiod=timeperiod)
		self.ma_analysis_value(f"SMA_{timeperiod}")

	def EMA(self, timeperiod):
		self.analysis[f"EMA_{timeperiod}"] = talib.SMA(self.data_close, timeperiod=timeperiod)
		self.ma_analysis_value(f"EMA_{timeperiod}")

	def WMA(self, timeperiod):
		self.analysis[f"WMA_{timeperiod}"] = talib.SMA(self.data_close, timeperiod=timeperiod)
		self.ma_analysis_value(f"WMA_{timeperiod}")

	def CCI(self, timeperiod):
		key = f"CCI_{timeperiod}"
		self.analysis[key] = talib.CCI(self.data_high, self.data_low, self.data_close, timeperiod=timeperiod)
		x = self.analysis[key][-1]
		if x > 100:
			code = 1
		elif x < -100:
			code = -1
		else:
			code = 0

		self.analysis_value[key] = [x, self.status[code], code]

	def RSI(self, timeperiod):
		key = f"RSI_{timeperiod}"
		self.analysis[key] = talib.RSI(self.data_close, timeperiod=timeperiod)
		x = self.analysis[key][-1]
		if x < 20:
			code = 1
		elif x > 80:
			code = -1
		else:
			code = 0

		self.analysis_value[key] = [x, self.status[code], code]

	def STOCH(self):
		key = f"STOCH"
		self.analysis[key] = {}
		self.analysis[key]["K"], self.analysis[key]["D"] = talib.STOCH(self.data_high, self.data_low, self.data_close,
																	   fastk_period=14)
		K = self.analysis[key]["K"][-1]
		D = self.analysis[key]["D"][-1]
		if K > D and D < 20 and K < 20:
			code = 1
		elif K < D and D > 80 and K > 80:
			code = -1
		else:
			code = 0

		self.analysis_value[key] = [K, self.status[code], code]

	def STOCHRSI(self): #works not stable
		key = f"STOCHRSI"
		self.analysis[key] = {}
		self.analysis[key]["K"], self.analysis[key]["D"] = talib.STOCHRSI(self.data_close, fastk_period=3)
		K = self.analysis[key]["K"][-1]
		D = self.analysis[key]["D"][-1]
		if K > D and D < 20 and K < 20:
			code = 1
		elif K < D and D > 80 and K > 80:
			code = -1
		else:
			code = 0

		self.analysis_value[key] = [K, self.status[code], code]

	def MACD(self):
		key = f"MACD"
		self.analysis[key] = {}
		self.analysis[key]["macd"], self.analysis[key]["signal"], self.analysis[key]["hist"] = talib.MACD(
			self.data_close, fastperiod=12, slowperiod=26, signalperiod=9)
		macd = self.analysis[key]["macd"][-1]
		signal = self.analysis[key]["signal"][-1]
		hist = self.analysis[key]["hist"][-1]
		if hist > 0:
			code = 1
		elif hist < 0:
			code = -1
		else:
			code = 0

		self.analysis_value[key] = [macd, self.status[code], code]

	def WILLR(self, timeperiod):
		key = f"WILLR_{timeperiod}"
		self.analysis[key] = talib.WILLR(self.data_high, self.data_low, self.data_close, timeperiod=timeperiod)
		x1 = self.analysis[key][-1]
		x2 = self.analysis[key][-2]
		if x1 < -80 and x1 > x2:
			code = 1
		elif x1 > -20 and x1 < x2:
			code = -1
		else:
			code = 0

		self.analysis_value[key] = [x1, self.status[code], code]

	def ma_analysis_value(self, key):
		x = self.analysis[key][-1]
		if x < self.value:
			code = 1
		elif x > self.value:
			code = -1
		else:
			code = 0

		self.analysis_value[key] = [x, self.status[code], code]

	def _format_indicator_name(self, indicator_abbreviated):
		indicator_abbreviated = indicator_abbreviated.split("_")
		if len(indicator_abbreviated) == 2:
			indicator_full = self.indicator_name[indicator_abbreviated[0]]+f" ({indicator_abbreviated[1]})"
		else:
			indicator_full = self.indicator_name[indicator_abbreviated[0]]

		return indicator_full

	def format_analysis_value(self, dictionary=[]):
		format_value = {}
		def add(key_value):
			name = self._format_indicator_name(key_value)
			value = round(self.analysis_value[key_value][0],2)
			signal = self.analysis_value[key_value][2]
			if signal == -1:
				signal = "sell"
			elif signal == 1:
				signal = "buy"
			else:
				signal = "neutral"
			format_value[key_value] = [name, value, self.analysis_value[key_value][1], signal]

		if len(dictionary) == 0:
			for key in self.analysis_value:
				add(key)
		else:
			for key in self.analysis_value:
				if key.split("_")[0] in dictionary:
					add(key)

		return format_value

	def total_analysis_value(self, dictionary=[]):
		x = 0
		count = 0
		buy_count = 0
		sell_count = 0
		neutral_count = 0


		for key in self.analysis_value:
			if len(dictionary) != 0 and key.split("_")[0] not in dictionary:
				continue

			status = self.analysis_value[key][2]
			if status == -1:
				sell_count += 1
			elif status == 1:
				buy_count += 1
			else:
				neutral_count += 1

			count += 1
			x += status

		if count // 2 < x:
			code = 2
		elif count // 4.5 < x:
			code = 1
		elif -count // 4.5 < x:
			code = 0
		elif -count // 2 < x:
			code = -1
		else:
			code = -2

		return {"info": [self.status[code], code, abs(x), count],
				"value": [sell_count, neutral_count,buy_count]}


class Api(Data):
	global json
	def fear_and_greed_index(request,limit=1):
		response = requests.get("https://api.alternative.me/fng/?limit=" + str(limit))
		data = json.loads(response.text)
		json_data = json.dumps(data['data'])
		return HttpResponse(json_data, content_type="application/json")


	def treemap(request, currency):
		data = Data(currency)
		json = data.treemap_json(request.GET)
		return HttpResponse(json, content_type="application/json")

	def history_data(request, coin, currency):
		url = request.GET
		data = Data(currency)
		#d = data.history_data(coin, limit_len)
		d = data.history_data(coin, url.get("time_frame"))
		d = json.dumps(d)
		return HttpResponse(d, content_type="application/json")


