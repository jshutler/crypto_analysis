import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re
from gensim.utils import simple_preprocess
from string import punctuation
import nltk

def main(year, coin, infile, outfile):
	'''This function will do the text preprocessing to our dataset. It will '''



	
	df = pd.read_csv(infile)

	df['processed_titles'] = df.title.apply(lambda x: x.lower())


	

	#this maps all punctuation to None, 
	table = str.maketrans('', '', punctuation)

	#with the table mapping punctuation to None, this will replace all punctuation with blanks
	df.processed_titles = df.processed_titles.apply(lambda x: x.translate(table).split())

	#initializes the word lemmatizer
	lemmatizer = WordNetLemmatizer()

	#goes through and removes all stopwords from title, and also lemmatizes each word in the title
	df.processed_titles = df.processed_titles.apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x if word not in set(stopwords.words('english'))]))


	#removes the <b> in the data set
	df.processed_titles = df.processed_titles.replace(to_replace=r'\<[^>]*\>',value='', regex =True)
 
	df.to_csv(outfile)





if __name__ == '__main__':
	
	years = range(2017, 2020)
	coins = ['bitcoin', 'ethereum', 'Zcash', 'litecoin']
	
	for year in years:
		for coin in coins:
			print(year, coin)
			infile = f'../data/news_data_collected_01_2020/preprocessed_data/{year}/{year}_{coin}_dataframe.csv'
			outfile = f'../data/news_data_collected_01_2020/processed_data/{year}/{year}_{coin}_dataframe.csv'

			# print(stopwords.words('english'))
			main(year, coin, infile, outfile)

