from datetime import datetime
import pandas as pd 
from pytz import timezone

class datetime_editor:
	'''This script will format the datetime objects we want for our analysis of the news article data set. 
	It will provide the datetime in pst, and give the day of week, hour, minute, and whether or not it was a weekend'''
	def __init__(self, coin, year, infile, outfile):
		self.infile = infile
		self.outfile = outfile
		self.df = pd.read_csv(infile, index_col =0)


	def run(self):
		self.df['date_published'] = self.get_datetime_object()
		self.df['date_published_pst'] = self.get_pst()
		self.df['month_pst'] = self.get_month_pst()
		self.df['day_of_week_pst'] = self.get_day_of_week_pst()
		self.df['hour_pst'] = self.get_hour_pst()
		self.df['minute_pst'] = self.get_minute_pst()
		self.df['second_pst'] = self.get_second_pst()
		self.df['weekend'] = self.get_weekend()
		

		self.df.to_csv(self.outfile) #SAVING DATA TO OUTFILE

		print(f'{self.outfile} saved to disk')



	def get_datetime_object(self):
		return pd.to_datetime(self.df['date_published'], utc=True)

	def get_pst(self):
		#sets the timezone to pst
		return self.df['date_published'].dt.tz_convert(timezone('US/Pacific'))

	def get_month_pst(self):
		#changes the vecotr into a Datetime index, which has the attributes Year, Month, Day, Hour, Etc
		return pd.DatetimeIndex(self.df['date_published_pst']).month

	def get_day_of_week_pst(self):
		return pd.DatetimeIndex(self.df['date_published_pst']).dayofweek

	def get_hour_pst(self):
		return pd.DatetimeIndex(self.df['date_published_pst']).hour

	def get_minute_pst(self):
		return pd.DatetimeIndex(self.df['date_published_pst']).minute

	def get_second_pst(self):
		return pd.DatetimeIndex(self.df['date_published_pst']).second

	def get_weekend(self):
		# print(self.df['day_of_week_pst'])
		return self.df['day_of_week_pst'].apply(lambda row : 0 if (row >= 0 and row <=4) else 1)

		




		


if __name__ == '__main__':
	
	coins = ['bitcoin', 'ethereum', 'Zcash', 'litecoin']
	years = range(2018, 2020)
	for year in years:
		for coin in coins:
			#establishign where we are reading and writing our data to
			infile = f'../data/news_data_collected_01_2020/preprocessed_data/{year}/{year}_{coin}_dataframe.csv'
			outfile = f'../data/news_data_collected_01_2020/processed_data/{year}/{year}_{coin}_dataframe.csv'
		

		editor = datetime_editor(coin, year, infile, outfile)
		editor.run()
	# editor = datetime_editor(2017, 'bitcoin')
	# editor.get_weekend()
	

