from datetime import datetime
import pandas as pd 
from pytz import timezone

class datetime_editor:
	def __init__(self, coin, year):
		self.df_name = f'raw_csv_dataframes/{year}_{coin}_dataframe.csv'
		self.df = pd.read_csv(self.df_name, index_col =0)


	def run(self):
		self.df['date_published'] = self.get_datetime_object()
		self.df['date_published_pst'] = self.get_pst()
		self.df['month_pst'] = self.get_month_pst()
		self.df['day_of_week_pst'] = self.get_day_of_week_pst()
		self.df['hour_pst'] = self.get_hour_pst()
		self.df['minute_pst'] = self.get_minute_pst()
		self.df['second_pst'] = self.get_second_pst()
		self.df['weekend'] = self.get_weekend()
		

		self.df.to_csv(self.df_name)
		print('saved to disk')



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
	years = [2017, 2018, 2019]
	for year in years:
		editor = datetime_editor('bitcoin', year)
		editor.run()
	# editor = datetime_editor(2017, 'bitcoin')
	# editor.get_weekend()
	

