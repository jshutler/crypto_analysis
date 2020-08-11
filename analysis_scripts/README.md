#analysis Scripts

##merge_news_and_minute.py
Script merges the crypto data and the news data with a left outer join with the crypto minute data as the left database


##sentiment_analyzer.py
This file takes the processed data files and calculates their sentiment polarity and subjectivity score using the TextBlob Library


##OLS_regression_analysis.py
###Warning, this script is old, and the syntax isn't pretty. I will be touching it up in the near future. 
Calculates a linear regression model using the following formula syntax: "y-hat ~ x1 + x2 + ... + xn"

Regressions I ran:
1. log_return ~ sent_polarity
2. log_return ~ sent_polarity + sent_polarity^2
3. log_return ~ sent_polarity + sent_polarity^3
4. log_return ~ sent_polarity + [high_sent_polarity] //dummy variable signifying sentiments of values higher than .5

##get_regresssion_results.py
###Warning, this script is old, and the syntax isn't pretty. I will be touching it up in the near future. 
A script to view the regression model and saves it to a pickle file (saved python object)

##plot_regression_results.py
###Warning, this script is old, and the syntax isn't pretty. I will be touching it up in the near future. 
Makes a plot of the regression coefficients side by side to look for effectiveness.
