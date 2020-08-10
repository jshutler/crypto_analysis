import pandas as pd 
from sklearn import linear_model
from math import log


class regression_maker():
	def __init__(self, coin, year):
		self.coin = coin
		self.news_df = pd.read_csv(f'clean_csv_dataframes/{year}_{coin}_dataframe.csv')
		self.minute_data = pd.read_csv(f'Crypto_Data/gemini_BTCUSD_{year}_1min.csv', header=1)


	def main(self):
		x = self.news_df['sentiment_polarity']
		y = self.minute_data['Close']
		y = y.apply(log)

		print(y)
		model = linear_model.LinearRegression().fit(x,y)




if __name__ == '__main__':
	maker = regression_maker('bitcoin', 2017)
	maker.main()

