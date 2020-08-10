import pandas as pd 
from math import log
from datetime import datetime
from os import listdir



def main(year, coin, minute_data_infile, news_data_infile, outfile):
	#this file will merge the minute data and the news_data into one file

	
	
	#making sure we only merge data for data we have
	minute_data_file_name = f'gemini_{coin_ticker}_{year}_1min.csv'
	clean_csv_df_file_name = f'{year}_{coin}_dataframe.csv'

	
	minute_data = pd.read_csv(minute_data_infile)
	
	
	news_df = pd.read_csv(news_data_infile, index_col=1)
	


	print(minute_data.columns)
	print(news_df.columns)

	#gives us the log returns for each value
	minute_data['log_returns'] = minute_data['Close'].apply(log)
	

	#converts all strings, to datetime objects. Then makes all the seconds 0 in order
	#to match the minutes for the minute date data frame.
	news_df['date_published'] = pd.to_datetime(news_df['date_published'], utc=True).apply(lambda dt: dt.replace(second=0))
	minute_data['Date'] = pd.to_datetime(minute_data['Date'], utc=True)

	#takes value of 1 or 0. Tells whether or not an article was released in that minute
	merged_df = minute_data.merge(news_df, how='left',left_on='Date', right_on='date_published')


	merged_df.to_csv(outfile)
	print(f'{outfile} saved to disk')



def get_ticker(coin):
	ticker_dict = {
	'bitcoin':'BTCUSD',
	'ethereum': 'ETHUSD',
	'Zcash': 'ZECUSD',
	'litecoin': 'LTCUSD'
	}

	return ticker[coin]




if __name__ == '__main__':
	years = range(2018, 2020)
	coins = ['bitcoin', 'ethereum', 'Zcash', 'litecoin']
	for coin in coins:
		for year in years:
			#gives us the coin ticker given the coin name
			coin_ticker = get_ticker(coin)
			print(coin_ticker)

			minute_data_infile = f'../data/crypto_minute_data/{year}/gemini_{coin_ticker}_{year}_1min.csv'
			news_data_infile = f'../data/news_data_collected_01_2020/processed_data/{year}/{year}_{coin}_dataframe.csv'
			
			outfile = f'../data/news_crypto_merge/{year}/{year}_{coin}_merged_df.csv'
			
			main(year, coin, minute_data_infile, news_data_infile, outfile)