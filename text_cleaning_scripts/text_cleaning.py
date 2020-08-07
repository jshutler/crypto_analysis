import re
import pandas as pd 

def main(coin, year):
	csv_path = f'raw_csv_dataframes/{year}_{coin}_dataframe.csv'
	df = pd.read_csv(csv_path, index_col=0)
	df['title'] = df['title'].replace(to_replace=r'\<[^>]*\>',value='', regex =True)
	
	df = df.drop_duplicates('title')

	df.to_csv(f'clean_csv_dataframes/{year}_{coin}_dataframe.csv')
	print(f'csv saved to clean_{csv_path}')


	






if __name__ == '__main__':
	years = [2017, 2018, 2019]
	for year in years:
		main('bitcoin', year)
	# main(2019, 'bitcoin')

