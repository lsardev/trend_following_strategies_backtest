import matplotlib.pyplot as plt
from calculate_indicators import get_rsi

def get_rsi_graphic(stock, start_date, end_date):
    date = get_rsi(stock, start_date, end_date)
    fig, ax = plt.subplots()

    ax.plot(date['Date'],date['RSI14'], label = 'RSI14')
    ax.set_ylabel('RSI')
    ax.set_title('Relative Strenght Index (RSI)')

    plt.show()

get_rsi_graphic("MRFG3.SA", "2020-01-01", "2020-12-10")

