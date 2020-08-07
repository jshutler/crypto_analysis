import pandas as pd 
import numpy as np 
from os import listdir
import pprint as pp

def main(coin, year):
	coin_short = {
	'bitcoin': "BTC",
	"ethereum": "ETH",
	"litecoin": "LTC",
	"zcash": "ZEC",
	}
	
	#get path for files
	crypto_path = f"../data/crypto_minute_data/{year}/gemini_{coin_short[coin]}USD_{year}_1min.csv"
	news_path = f"../data/news_data/{year}/{year}_{coin}_dataframe.csv"


	#load data into dataframes
	crypto_df = pd.read_csv(crypto_path)
	news_df = pd.read_csv(news_path)


	#TO ENSURE THAT BOTH ARE OF A DATETIME OBJECT that can be matched up.
	news_df['date_published'] = pd.to_datetime(news_df['date_published'], utc=True).apply(lambda dt: dt.replace(second=0))
	crypto_df['Date'] = pd.to_datetime(crypto_df['Date'], utc=True)


	print(news_df.shape)
	news_df['date_published'] = pd.to_datetime(news_df.groupby('date_published').mean().reset_index(), utc = True)
	print(news_df.shape)




	merged_df = pd.merge(crypto_df, news_df, left_on = "Date", right_on = 'date_published', how = 'left')

	print(merged_df.shape)

	#date_published for news



def log_returns(crypto_df):
	'''we'll use this file to clean and add numeric changes to our dataframes where needed'''
	crypto_df['logged_returns'] = crypto_df['Close'].apply(log)
	return crypto_df

if __name__ == '__main__':
	coin = 'bitcoin'
	year = 2017
	main(coin, year)