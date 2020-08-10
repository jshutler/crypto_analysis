import pandas as pd 
import matplotlib.pyplot as plt 
from statsmodels.regression.linear_model import OLSResults
from os import listdir
import seaborn as sn; sn.set()
from pprint import pprint
class plot_regression_results:

	def __init__(self, dependent_variable='return', save=False, show=False):
		self.dependent_variable = dependent_variable
		self.save=save
		self.show=show


	def main(self, pickle_names, path=None):
		#will give me the first results, bit coin in this case
		#run plots for all coins
		for pickle_name in pickle_names:
			df = pd.read_pickle(path+pickle_name).reset_index()
			df[['coefficients', 'standerd_errors']] = df[['coefficients', 'standerd_errors']].round(2)
			df = df[df['residuals'] > 100]
			coin = pickle_name.split('_')[0]
			print(coin)

			# self.plot_r_squareds(df, coin)
			self.plot_coefficients(df, coin)

	def plot_r_squareds(self, df, coin):
		##########################################################################
		#this janky ass code converts the times coefficient to an integer, sorts the 
		#whole df by 'times' then converts times back into a string
		df['times'] = df['times'].apply(int)
		df = df.sort_values(by='times')
		df['times'] = df['times'].apply(str)
		################################################################
		x = df['times']
		y=df['r_squareds']

		plt.errorbar(x=x, y=y, fmt= 'o', marker ='.')
		plt.axhline(y=0, color='r', linestyle= '-')
		plt.xlabel('Times')
		plt.ylabel('R^2')
		plt.title(f'{coin}: {self.dependent_variable}')

		if self.save:
			plt.savefig(f'plots/{self.dependent_variable}_analysis/regression_plots/r_squareds/{coin}_rsquared_plot')
			print('saved figure')
		
		if self.show:
			plt.show()
		else:
			plt.close()
		
	def plot_coefficients(self, df,coin):
		print(df.columns)
		index = df.index

		#gives a uniques list of all formulas
		formulas = list(df['formulas'].drop_duplicates())

		#generate a data frame with only the best r^2 for each data frame
		best_df = self.get_best_df(df, formulas)	
		#this will let me access the coeffients within the tuple in the dataframe
		

		# print(df)
		# print(df[['coefficients', 'standerd_errors']])
		aggregate_polarity_dict = {'times': [], 'coefficients': [], 'standerd_errors': []}
		polarity_squared_dict = {'times': [], 'coefficients': [], 'standerd_errors': []}
		polarity_cubed_dict = {'times': [], 'coefficients': [], 'standerd_errors': []}
		high_sentiment_dict = {'times': [], 'coefficients': [], 'standerd_errors': []}
		print(df['coefficients'][1])

		#this loop will give me all of my data in dictionaries aggregated appropriately
		for index, row in df.iterrows():
			coefs = list(row['coefficients'].index)

			#the following set of if statements creates dictionaries with wanted attributes
			#in the regression models that contain that specific coefficient 
			if 'aggregate_polarity' in coefs:
				aggregate_polarity_dict['times'].append(row['times'])
				aggregate_polarity_dict['coefficients'].append(row['coefficients']['aggregate_polarity'])
				aggregate_polarity_dict['standerd_errors'].append(row['standerd_errors']['aggregate_polarity'])

			if 'power(aggregate_polarity, 2)' in coefs:
				polarity_squared_dict['times'].append(row['times'])
				polarity_squared_dict['coefficients'].append(row['coefficients']['aggregate_polarity'])
				polarity_squared_dict['standerd_errors'].append(row['standerd_errors']['aggregate_polarity'])

			if 'power(aggregate_polarity, 3)' in coefs:
				polarity_cubed_dict['times'].append(row['times'])
				polarity_cubed_dict['coefficients'].append(row['coefficients']['aggregate_polarity'])
				polarity_cubed_dict['standerd_errors'].append(row['standerd_errors']['aggregate_polarity'])


			if 'high_sentiment' in coefs:
				high_sentiment_dict['times'].append(row['times'])
				high_sentiment_dict['coefficients'].append(row['coefficients']['aggregate_polarity'])
				high_sentiment_dict['standerd_errors'].append(row['standerd_errors']['aggregate_polarity'])


		
		dictionaries = [aggregate_polarity_dict, polarity_squared_dict, polarity_cubed_dict, high_sentiment_dict]
		coefficient_name = ['aggregate_polarity', 'polarity_squared', 'polarity_cubed', 'high_sentiment']
		print(type(aggregate_polarity_dict['times'][0]))

		coef_dfs = [pd.DataFrame(coef) for coef in dictionaries]



		#finally, it is time to make some plots
		for coefficient, coefficient_name in zip(coef_dfs, coefficient_name):
			##########################################################################
			#this janky ass code converts the times coefficient to an integer, sorts the 
			#whole df by 'times' then converts times back into a string
			coefficient['times'] = coefficient['times'].apply(int)
			coefficient = coefficient.sort_values(by='times')
			coefficient['times'] = coefficient['times'].apply(str)
			################################################################

			x = coefficient['times']
			y = coefficient['coefficients']
			standerd_errors = coefficient['standerd_errors']
			# plt.scatter(x=x, y=y)
			plt.errorbar(x=x, y=y, yerr=standerd_errors, fmt='o', ecolor='r', elinewidth=2, marker='.')

			plt.ylim(bottom=-2, top=1)
			
			plt.axhline(y=0, color='c', linestyle= '-')

			plt.title(coefficient_name)

			plt.xlabel('times')
			plt.ylabel('Beta')
			if self.save:
				plt.savefig(f'plots/{self.dependent_variable}_analysis/regression_plots/coefficients/{coin}_{coefficient_name}_plot')		
				print('saved figure')
			
			if self.show:
				plt.show()
			else:
				plt.close()



	def get_best_df(self, df,formulas):
		'''gives the dataframe with only the highest r^2 values'''
		best_df = []
		for formula in formulas:
			spliced_df = df[df['formulas'] == formula].reset_index()

			best_df.append(spliced_df.iloc[spliced_df['r_squareds'].idxmax()])
			return best_df

if __name__ == '__main__':
	coins = ['bitcoin', 'ethereum', 'Zcash', 'litecoin']
	# results = listdir(f'results/return_predictions/{coin}')
	dependent_variable = 'volume'
	path =f'results/{dependent_variable}_predictions/'
	pickle_names = listdir(path)
	plotter = plot_regression_results(dependent_variable = dependent_variable, save=True, show=False)
	plotter.main(pickle_names, path)