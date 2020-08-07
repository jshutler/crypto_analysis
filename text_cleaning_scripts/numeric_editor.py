import pandas as pd 
from os import listdir
from math import log

def main(coin, year):
	'''we'll use this file to clean and add numeric changes to our dataframes where needed'''
	coin_short = {
	'bitcoin': "BTC",
	"ethereum": "ETH",
	"litecoin": "LTC",
	"zcash": "ZEC",
	}

 	
	crypto_path = f"../data/crypto_minute_data/{year}/gemini_{coin_short[coin]}USD_{year}_1min.csv"
	news_path = f"../data/news_data/{year}/{year}_{coin}_dataframe.csv"


	try:
		print('hit')
		crypto_df = pd.read_csv(crypto_path)
		news_df = pd.read_csv(news_path)
	except:
		return

	print(year, coin)
	print(crypto_df.columns)
	crypto_df['logged_returns'] = crypto_df['Close'].apply(log)

	
	crypto_df.to_csv(crypto_path)


		


if __name__ == '__main__':
	years = [2017, 2018, 2019]
	coins = ['bitcoin', 'litecoin', 'ethereum', 'zcash']
	
	for year in years:
		for coin in coins:

			main(coin, year)