import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import mpld3
from pandas.plotting import register_matplotlib_converters
from datetime import date, timedelta


def open_stock_plot(stock_id):

    plt.clf()
    register_matplotlib_converters()
    matplotlib.use('WebAgg')
    df = yf.download(stock_id,
                     start=date.today()-timedelta(days=365),
                     end=str(date.today()),
                     progress=False)
    matplotlib.use('WebAgg')
    plt.plot(df["Close"])
    plt.title(stock_id)
    mpld3.show()