#Text Cleaning Scripts

##text_cleaning.py
This file will be doing all the necessary preprocessing for a NLP type project. It does the following:

1. removes all punctuation from the data
2. removes stopwords from data (i.e. the, a, an, etc). Words that don't have any inherent meaning to them
3. Lemmatizes the words. This changes past and future tenses to the present tense. (i.e decreasing -> decrease, increased -> increase, etc)
4. removes HTML tags like <b>.

##datetime_editor.py
This file converts all the datetime data into a usable format, and extracts meaningful information out of it, i.e. what day of the week it was published on, whether or not it was a weekend, etc.
