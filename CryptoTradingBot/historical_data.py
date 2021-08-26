from binance.client import Client
import config
import csv

client = Client(config.API_KEY, config.API_SECRET)

csvfile = open('ETHUSDT_012021_022021_5MIN.csv', "w", newline="")

candlestick_writer = csv.writer(csvfile, delimiter=",")

candlesticks = client.get_historical_klines(
    "ETHUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Jan, 2021", "1 Feb, 2021")

for candlestick in candlesticks:
    candlestick[0] = candlestick[0] / 1000
    candlestick_writer.writerow(candlestick)


csvfile.close()
