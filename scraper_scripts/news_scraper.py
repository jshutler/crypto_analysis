import pandas as pd 
import pickle
import requests
from bs4 import BeautifulSoup
from json import loads

class contextual_news_scraper:
	def __init__(self, term, year, pages=1):

		self.pages = pages
		self.term = term
		self.year = year


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

		#going through the requests and actually collecting all the above data points
		for month in range(1, 13):
			for page in range(self.pages):
				try:
					response_json = self.get_json(page, month)
				except:
					break
				#breaks from the loop and saves the values that we have
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
		url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/NewsSearchAPI"
		if month == 12:
			querystring = {"fromPublishedDate":f"{month}/01/{self.year}",f"toPublishedDate":f"{month}/31/{self.year}", "autoCorrect":"false","pageNumber":page,"pageSize":f"{self.pages}","q":self.term,"safeSearch":"false"}
		else:
			querystring = {"fromPublishedDate":f"{month}/01/{self.year}",f"toPublishedDate":f"{month+1}/01/{self.year}", "autoCorrect":"false","pageNumber":page,"pageSize":f"{self.pages}","q":self.term,"safeSearch":"false"}
		headers = {
		    'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
		    'x-rapidapi-key': "94ed915629msh28a8aee42e9c89dp1cdc6ejsn5fed886c6b11"
		    }
		#gets the page that we want
		response = requests.request("GET", url, headers=headers, params=querystring)

	
		#converts response into json format
		response_json = loads(response.text)

		print(response.headers)

		return response_json	
		





if __name__ == '__main__':

	years = [2018, 2019]
	coins = ['bitcoin', 'ethereum', 'zcash', 'litecoin']
	for coin in coins:
		for year in years:
			scraper = contextual_news_scraper(coin, year, pages=50)
			news_df = scraper.get_news_df()
			news_df.to_csv(f'../data/news_data/{year}/{year}_{coin}_dataframe.csv')

			print('News Data Frame sucessfully saved to disk!')