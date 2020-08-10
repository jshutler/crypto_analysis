from textblob import TextBlob 
import pandas as pd 

def main(coin,year, infile, outfile):

	df = pd.read_csv(infile)

	#applies the function to everysingle value in the column
	df['sentiment_polarity'] = df['processed_titles'].apply(sentiment_analysis_polarity)

	#applies the function to everysingle value in the column
	df['sentiment_subjectivity'] = df['processed_titles'].apply(sentiment_analysis_subjectivity)

	df.to_csv(outfile)



def sentiment_analysis_polarity(df):
	return TextBlob(df).sentiment.polarity

def sentiment_analysis_subjectivity(df):
	return TextBlob(df).sentiment.subjectivity




if __name__ == '__main__':
	years = range(2018, 2020)
	coins = ['bitcoin', 'ethereum', 'Zcash', 'litecoin']
	
	for year in years:
		for coin in coins:
			print(year,coin)
			infile = f'../data/news_data_collected_01_2020/processed_data/{year}/{year}_{coin}_dataframe.csv'
			outfile = f'../data/news_data_collected_01_2020/processed_data/{year}/{year}_{coin}_dataframe.csv'
			
			main('coin', year, infile, outfile)