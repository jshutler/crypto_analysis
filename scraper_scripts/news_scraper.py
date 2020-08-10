import pandas as pd 
import pickle
import requests
from bs4 import BeautifulSoup
from json import loads

class contextual_news_scraper:
	'''This program will use the Contexutual News API to download news articles given a key word and return a data frame with relevant information about the articless'''
	def __init__(self, term, year, pages=1, start_month=1, end_month=13):

		self.pages = pages
		self.term = term
		self.year = year

		#lets you decide what month to start your search
		self.start_month = start_month
		self.end_month = end_month

	def get_news_df(self):
		#establishing all the data points that we want to get 
		titles = []
		keywords = []
		urls = []
		language = []
		publishers = []
		datetimes = []
		descriptions = []
		bodies = []

		#Main loop of the function. will loop through all the months in the given year to get data
		for month in range(self.start_month, self.end_month):

			#reads through all the pages on this given query
			for page in range(self.pages):	

				try:
					response_json = self.get_json(page, month) #function call to the Search API itself
				except:
					break  #breaks from the loop and saves the values that we have

				#if the page has no information, we will move to the next one
				if len(response_json['value']) == 0:
					break
				
				for value in response_json['value']:
					#putting titles in list
					
					titles.append(value['title'])
					keywords.append(value['keywords'])
					urls.append(value['url'])
					language.append(value['language'])
					publishers.append(value['provider']['name'])
					datetimes.append(value['datePublished'])
					descriptions.append(value['description'])
					bodies.append(value['body'])


		data_dict = {'title': titles, 'url': urls, 'language': language, 'keywords': keywords, 'publisher': publishers, 'date_published': datetimes,'article': bodies}
		
		news_df = pd.DataFrame(data_dict)


		return news_df
		




	def get_json(self, page, month):
		url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/NewsSearchAPI" #url to the contexual search api

		#QUERIES TO API
		if month == 12: #needs custom syntax for the month of december
			querystring = {"fromPublishedDate":f"{month}/01/{self.year}",f"toPublishedDate":f"{month}/31/{self.year}", "autoCorrect":"false","pageNumber":page,"pageSize":f"{self.pages}","q":self.term,"safeSearch":"false"}
		
		else: #query to all months that are not december
			querystring = {"fromPublishedDate":f"{month}/01/{self.year}",f"toPublishedDate":f"{month+1}/01/{self.year}", "autoCorrect":"false","pageNumber":page,"pageSize":f"{self.pages}","q":self.term,"safeSearch":"false"}
		
		headers = {
		    'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
		    'x-rapidapi-key': "94ed915629msh28a8aee42e9c89dp1cdc6ejsn5fed886c6b11"
		    }
		
		#Returns the response page from the API
		response = requests.request("GET", url, headers=headers, params=querystring)

	
		#converts response into json format
		response_json = loads(response.text)

		print(response.headers)

		return response_json	
		





if __name__ == '__main__':



	years = [2018, 2019]
	coins = ['bitcoin', 'ethereum', 'zcash', 'litecoin']
	start_month = 1
	end_month = 13
	
	for coin in coins:

		for year in years:

			scraper = contextual_news_scraper(coin, year, pages=50, start_month=start_month, end_month=end_month) #initializes scraper
			news_df = scraper.get_news_df() #scrapes data and return dataframe

			outfile_path = f'../data/news_data_updated/{year}_{coin}_dataframe.csv'	#sets path of outfile	

			news_df.to_csv(outfile_path) #saves dataframe to csv file

			print('News Data Frame sucessfully saved to disk!')