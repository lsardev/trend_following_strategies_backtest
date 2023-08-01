import yfinance as yf

#pegando base de dados
def get_stock_data(stock, start_date, end_date):
    data = yf.download(stock, start_date, end_date).reset_index()
    
    return data

#get_stock_data("VALE3.SA", "2020-01-01", "2020-12-10")

