import pandas as pd 
from math import log
from datetime import datetime
from os import listdir



def main(year, coin):
	coin_ticker = get_ticker(coin)
	print(coin_ticker)
	#making sure we only merge data for data we have
	minute_data_file_name = f'gemini_{coin_ticker}_{year}_1min.csv'
	clean_csv_df_file_name = f'{year}_{coin}_dataframe.csv'
	minute_data_directory = listdir(f'Crypto_Data')
	news_df_directory = listdir(f'clean_csv_dataframes')

	if minute_data_file_name not in minute_data_directory:
		print(f'{minute_data_file_name} is not in the Crypto Data directory.')
		return None
	elif clean_csv_df_file_name not in news_df_directory:
		print(f'{clean_csv_df_file_name} is not in the clean_csv_dataframes directory.')
		return None
	else:
		print('All data imported, now reading in dataframes.')
		minute_data = pd.read_csv(f'Crypto_Data/gemini_{coin_ticker}_{year}_1min.csv', header=1)
		news_df = pd.read_csv(f'clean_csv_dataframes/{year}_{coin}_dataframe.csv', index_col=1)
	


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
	

	file_to_be_saved = f'{year}_{coin}_merged_df.csv'
	merged_df_directory = listdir('merged_dataframes')
	print(merged_df_directory)

	if file_to_be_saved not in merged_df_directory:
		merged_df.to_csv(f'merged_dataframes/{file_to_be_saved}')
		print('saved merged df to disk')
	else:
		print('file already in directory')


def get_ticker(coin):
	if coin == 'bitcoin':
		return 'BTCUSD'

	elif coin == 'ethereum':
		return 'ETHUSD'

	elif coin == 'Zcash':
		return 'ZECUSD'

	elif coin == 'litecoin':
		return 'LTCUSD'

	else:
		print('coin not registered')
		exit()




if __name__ == '__main__':
	years = [2017,2018,2019]
	coins = ['bitcoin', 'ethereum', 'Zcash', 'litecoin']
	for coin in coins:
		for year in years:
			main(year, coin)