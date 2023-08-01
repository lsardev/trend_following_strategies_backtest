import numpy as np
from select_stock import get_stock_data

#Calculando média móvel, 50 dias
def get_simple_moving_average(stock, start_date, end_date, window_size):
    data = get_stock_data(stock, start_date, end_date)

    data[f'SMA{window_size}'] = data['Adj Close'].rolling(window_size).mean()
    print(data.tail())
#get_moving_average("VALE3.SA", "2020-01-01", "2020-12-10", 50)

def get_exponecial_moving_average(stock, start_date, end_date, window_size):
    data = get_stock_data(stock, start_date, end_date)

    data[f'SMA{window_size}'] = data['Adj Close'].ewm(window_size).mean()
    print(data.tail())


#Calculando MACD: fest_em = 12, slow_em = 26
def get_macd_and_sinal(stock, start_date, end_date, fest_em, slow_em):
    data = get_stock_data(stock, start_date, end_date)

    #média dos 12 períodos
    mme12 = data['Close'].ewm(span=fest_em).mean()

    #média dos 26 períodos
    mme26 = data['Close'].ewm(span=slow_em).mean()

    #macd
    macd = mme12 - mme26

    #linha de sinal de compra e venda
    sinal=macd.ewm(9).mean()

    #colocando dados do MACD e sinal no dataframe
    data['MACD'] = macd
    data['Sinal'] = sinal

    return data
#print(get_macd_and_sinal("VALE3.SA", "2020-01-01", "2020-12-10", 12, 26))

#calculando RSI
def get_rsi(stock, start_date, end_date):
    data = get_stock_data(stock, start_date, end_date)

    #calculando variação
    data['change'] = data['Close'] - data['Close'].shift(1)

    #identificar periodos de ganhos e perdas
    data['gain'] = data.loc[data['change']>0, 'change'].apply(abs)
    data.loc[(data['gain'].isna()), 'gain'] = 0
    data.loc[0, 'gain'] = np.NaN

    data['loss'] = data.loc[data['change']<0, 'change'].apply(abs)
    data.loc[(data['loss'].isna()), 'loss'] = 0
    data.loc[0, 'loss'] = np.NaN

    #calcular média dos ganhos e das perdas
    window_size = 14

    data['avg_gain'] = data['gain'].rolling(window_size).mean()
    data['avg_loss'] = data['loss'].rolling(window_size).mean()

    first_valor = data['avg_gain'].first_valid_index()
    
    for index,row in data.iterrows():
        if index == first_valor:
            prev_avg_gain = row['avg_gain']
            prev_avg_loss = row['avg_loss']

        elif index > first_valor:
            data.loc[index, 'avg_gain'] = ((prev_avg_gain*(window_size-1)) + row['gain'])/window_size
            prev_avg_gain = data.loc[index, 'avg_gain']

            data.loc[index, 'avg_loss'] = ((prev_avg_loss*(window_size-1)) + row['loss'])/window_size
            prev_avg_gain = data.loc[index, 'avg_loss']

    #Calcular RS - diferença de ganhos e perdas
    data[f'RS{window_size}'] = data['avg_gain']/data['avg_loss']

    #Calcular RSI
    data[f'RSI{window_size}'] = 100 - (100/(1 + data[f'RS{window_size}']))

    #print(data)
    #print(data[['RS14', 'RSI14']].tail())

    return data
#get_rsi("VALE3.SA", "2020-01-01", "2020-12-10")






