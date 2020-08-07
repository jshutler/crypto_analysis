from textblob import TextBlob 
import pandas as pd 

def main(coin,year):
	df = pd.read_csv(f'clean_csv_dataframes/{year}_{coin}_dataframe.csv', index_col=0)
	#applies the function to everysingle value in the column
	df['sentiment_polarity'] = df['title'].apply(sentiment_analysis_polarity)

	#applies the function to everysingle value in the column
	df['sentiment_subjectivity'] = df['title'].apply(sentiment_analysis_subjectivity)

	df.to_csv(f'clean_csv_dataframes/{year}_{coin}_dataframe.csv')



def sentiment_analysis_polarity(df):
	return TextBlob(df).sentiment.polarity

def sentiment_analysis_subjectivity(df):
	return TextBlob(df).sentiment.subjectivity




if __name__ == '__main__':
	years = [2017, 2018, 2019]
	for year in years:
		main('bitcoin', year)