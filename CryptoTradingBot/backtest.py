import backtrader as bt


class MadHatterStrategy(bt.Strategy):
    def __init__(self):
        self.RSI = bt.talib.RSI(self.data, period=14)
        macd, macdsignal, macdhist = bt.talib.MACD(
            self.data)

    def next(self):

        if self.RSI < 30:
            self.buy(size=1)
            print()
        if self.RSI > 70:
            self.close(self.macd)


cerebro = bt.Cerebro()

data = bt.feeds.GenericCSVData(
    dataname="ETHUSDT_012021_022021_5MIN.csv", dtformat=2)

cerebro.adddata(data)

cerebro.addstrategy(MadHatterStrategy)

cerebro.run()

cerebro.plot()
