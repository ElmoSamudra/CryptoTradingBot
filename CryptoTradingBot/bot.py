import websocket
import json
import pprint
import talib
import numpy
from binance.client import Client
from binance.enums import *
import config

SOCKET = "wss://stream.binance.com:9443/ws/<symbol>@kline_<interval>"

SOCKET_ETHUSDT = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

client = Client(confid.API_KEY, config.API_SECRET)

def order(symbol, quantity, side, order_type):
    try:
        order= client.create_ordcer(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
        
    except Exception as e:
        return False

    return True

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"
TRADE_QUANTITY = 0.05

closes = []
in_position = false

def on_open(ws):
    print("opened connection")


def on_close(ws, close_status_code, close_msg):
    print("closed connection")


def on_message(ws, message):
    global closes
    print("received message")
    json_message = json.loads(message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print(closes)

    if len(closes) > RSI_PERIOD:
        np_closes = numpy.array(closes)
        rsi = talib.RSI(np_closes, RSI_PERIOD)
        
        last_rsi = rsi[-1]
        print("the current rsi is {}".format(last_rsi))
        
        if last_rsi > RSI_OVERBOUGHT:
            if in_position:
                print("OVERBOUGHT time to SELL!")

                order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = false
            else:
                print("It is overbought, but we don't own any. Nothing I can do.")
        if last_rsi < RSI_OVERSOLD:
            if in_position:
                print("It is ovversold, but I already own it. Nothing I can do.")
            else:
                print("OVERSOLD time to BUY!")
                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = True


ws = websocket.WebSocketApp(
    SOCKET_ETHUSDT, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()
