This is my ongoing Research Senior Project at Cal Poly San Luis Obispo that I'm performing with Professor Pratish Patel and Professor Ziemowit Bednarek.

All code thus far has been written by me exclusively.

The main idea behind this project is to see if we can find any correlation between news articles written about a given cryptocurrency and the return on the currency itself. I gathered data for Bitcoin, Ethereum, Litecoin, and ZCash

To accomplish this, I first used the contextual News Search API (https://rapidapi.com/contextualwebsearch/api/web-search?endpoint=5b8644c1e4b09cbc25b00140) to gather news articles which have the given cryptocurrency mentioned in it. This data had the following information:

1. Title of Article
2. URL to Article
3. Language
4. Article Publisher
5. Datetime Published (UTC time)
6. The Article itself

Prelimnary Analysis was already done to see if the sentiment of the article title (Calculated using the TextBlob Library) had any correlation to the returns. I used OLS in the Statsmodels Library to look for correlation, but no correlation was found.

The next steps of the project are as follows:
1. See if/when the articles gathered were ever published to Twitter. (Completed) [Used GetOldTweets3 Library]
2. Run the same analysis, but to see if the time published to Twitter is more impactful on the return, as Twitter has a larger audience to spread the article to more people have the ability to impact the price.
3. Create more features from the dataset.
  a. Create Word Embeddings of all the article titles from the dataset.
  b. Use those Word Embeddings to K-Means Cluster the data to put the articles in meaningful classifactions
4. Perform more OLS, and potentially other estimators to see if a correlation can be created with the new data.

This is an ongoing project 
