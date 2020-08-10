#work with the dataframes in merged_dataframes
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sn; sn.set()
from sklearn.linear_model import LinearRegression
from numpy import array, isnan, power
import statsmodels.api as sm 
from statsmodels.formula.api import ols
from statistics import mean

#i'll delete this later
# pd.set_option('display.max_rows', None)
# pd.options.display.max_rows
class regression_analyzer:
	def __init__(self, year, coin, time=1, no_zeros=False, dependent_variable=None):
		self.year=year
		self.coin=coin
		#refers to how many minutes ahead we want to try to predict the return
		self.time=time
		#removes all the zeroes from the dataframe
		if no_zeros:
			self.df = pd.read_csv(f'../dataframes/merged_dataframes/{year}_{coin}_merged_df.csv')
			self.df = self.df[self.df['sentiment_polarity'] != 0]
			self.df['Date'] = pd.to_datetime(self.df['Date'])
		#keeps the zeroes in the dataframe
		else:
			self.df = pd.read_csv(f'../dataframes/merged_dataframes/{year}_{coin}_merged_df.csv')
			self.df['Date'] = pd.to_datetime(self.df['Date'])

		self.df['high_sentiment'] = self.df['sentiment_polarity'].apply(lambda sentiment : 1 if sentiment > .8 else 0)

		self.dependent_variable = dependent_variable
	def main(self):
		print(self.df.columns)
		

	def plot_sentiment_by_return(self):
		# plt.plot(self.df[f'{dependent_variable}'][::-1])
		# plt.scatter(range(len(self.df['sentiment_polarity'])), self.df['sentiment_polarity'][::-1])
		df = self.df.dropna()
		plt.scatter(df['sentiment_polarity'], df[f'{self.dependent_variable}'][::-1])
		plt.show()


	def run_regression(self, formula, save=False):
		#use aggregate if you want a rolling average for a period of time.
		#use shifted if you want direct implication of each article
		df = self.aggregate_df()
		try: 
			#generate model
			model = ols(formula=formula, data=df)
		except:

			print('error: ')
			print('formula: ', formula)
			print(df)
			raise('error with ols')


		results = model.fit()
		
		print(results.summary())
		print("parameters", results.params)
		print("r^2", results.rsquared)

		print(results.params.index)

		#creates a model name based 
		# model_name = '+'.join([variable for variable in list(results.params.index[1:])])
		if save:
			model_name = f'regression_models/{self.dependent_variable}_predictions/{self.coin}/{formula} {self.year}_{self.time}_minute.pickle'
			results.save(model_name)
			print(f'saved "{model_name}.pickle" saved to disk')

		return results


	def shift_df(self):
		df = self.df.drop_duplicates('Date')

		log_returns_shifted = df[["Date", f"{self.dependent_variable}"]][self.time:].reset_index()
		print('hit')

		sentiment_polarity_shifted = df[['Date', 'sentiment_polarity']][:-1*self.time]


		df_dropped_nans = self.df.dropna()

		new_df = log_returns_shifted.merge(sentiment_polarity_shifted, left_index=True, right_index=True).dropna()

	def aggregate_df(self, df=[0], authors=None):

		if len(df) > 1:
			#if a df is given to the function, then we reassign df as a df with the authors
			print(authors)
			df = df[['Date', f'{self.dependent_variable}','sentiment_polarity', 'high_sentiment', 'publisher'] + authors].drop_duplicates('Date')

		else:
			#otherwise, we want the df to simply have these three columns
			df = self.df[['Date', f'{self.dependent_variable}','sentiment_polarity', 'high_sentiment', 'publisher']].drop_duplicates('Date')
		


		#gets the articles released on the same and averages them
		#computes a rolling average based on the time attribute, which signifies how 
		#many minutes in the future we want to find a prediction
		#the shift method will sihft the aggregate polarity to a location self.time units away
		#this will make it on the same row as the Closing Return that we want to run the regression against
		df['aggregate_polarity'] = df['sentiment_polarity'].rolling(self.time, min_periods=1).mean().shift(-1*self.time+1)
		
		#if we've given the dataframe the extra author columns
		print(len(df.columns))
		print(df.columns)
		if len(df.columns) > 6:
			df[authors] = df[authors].rolling(self.time, min_periods=1).sum().shift(-1*self.time+1)

		#gives you every element we want to know about
		df = df.iloc[::self.time,:]
		
		#removes nas to reduce computational time
		df = df[df['aggregate_polarity'].notna()]

		return df


	def get_author_dummy_variables(self):
		print(self.df.columns)

		#gets me a list of all authors in the data set
		authors = list(self.df['publisher'].drop_duplicates().dropna())

		#creates a data frame of dummy variables in the dataframe
		author_dummies =pd.get_dummies(self.df['publisher'])


		combined = self.df.merge(author_dummies, left_index=True, right_index=True)

		print(len(author_dummies))
		print(len(self.df))
		print(len(combined))

		print(combined[authors].sum().sum())
		crash=crash
		
		return combined, author_dummies.columns


if __name__ == '__main__':
	#currently dropping all articles that were released at the same minute.
	#time is in minutes: 1 = 1 minute shift; 60 minutes = 1 hour; 1440 minutes = 1 day
	# analyzer = regression_analyzer(2018, 'bitcoin', no_zeros=False, time=1)
		
	coins = ['bitcoin', 'ethereum', 'Zcash', 'litecoin']
	times = [1,5,30,60,1440]
	years = [2018, 2019]
	#should either be Volume, or log_returns
	dependent_variable = 'Volume'
	
	formulas = [f'{dependent_variable} ~ aggregate_polarity',f'{dependent_variable} ~ aggregate_polarity + power(aggregate_polarity, 2)', f'{dependent_variable} ~ aggregate_polarity + power(aggregate_polarity,3)',f'{dependent_variable} ~ aggregate_polarity + high_sentiment']

	for formula in formulas:
		for coin in coins:
			for time in times:
				analyzer = regression_analyzer(2019, coin, no_zeros=False, time=time, dependent_variable=dependent_variable)
				analyzer.run_regression(formula=formula, save=True)
