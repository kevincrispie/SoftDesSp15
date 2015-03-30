from pattern.web import *
from pattern.en import *
import matplotlib.pyplot as plt 
import numpy as np
import urllib
import math

"""
This is a sentiment analyzer than takes a text file of tweets that I imported using 
another python program (tweet_importer.py), and creates graphs of a sentiment and
emotional analysis of different political search terms.
"""


#dang, nice job with all those readable function names. those short, concise functions are a beautiful beautiful sight.
def twitter_fetch(input_file):
	"""
	returns input file as list of tweets
	"""

	with open (input_file, "r") as myfile:
	 	twitter_data = myfile.readlines()
	for x in range(len(twitter_data)):
	 	twitter_data[x] = twitter_data[x].rstrip('\n')

	return twitter_data


def list_stripper(data_list, keyword):
	""" 
	strips the keyword from each list_of_all_tweets
	"""

	i = 0
	while i < len(data_list):
		if data_list[i] == keyword:
			del(data_list[i])
			i += 1
	return data_list


def keyword_remover(data_list_of_lists,keywords):
	"""
	removes labels from a list of lists given list of labels
	"""
	stripped_data_list_of_lists = []
	for x in range(len(keywords)):
		stripped_data_list_of_lists.append(list_stripper(data_list_of_lists[x], keywords[x]))
	return stripped_data_list_of_lists


def list_splitter(data_list, keyword):
	"""
	splits the list into 2 lists given a keyword
	"""

	for x in range(len(data_list)):
		if data_list[x] == keyword:
			new_list = data_list[x::]
			data_list = data_list[0:x]
			return data_list, new_list


def iterated_list_splitter(data_list, keywords):
	"""
	splits lists given a list of keywords
	"""

	list_of_all_tweets = []
	list_to_split = data_list
	for keyword in keywords:
		produced_list, list_to_split = list_splitter(list_to_split,keyword)
		list_of_all_tweets.append(produced_list)

	list_of_all_tweets.append(list_to_split)
	return list_of_all_tweets


def sentiment_analyzer(text):
	""" Analyzes the sentiment of a statement
	
	input: text, a string to be analyzed
	returns: sent_index, a numerical rating of the sentiment of a statement
	"""

	lower_text = text.lower()
		
	hashtag_scaling = 0.3
	exclamation_scaling = 0.5
	uppercase_scaling = 0.2


	sent_index = 0

	for x in range(len(positive_words)):
		sent_index += lower_text.count(positive_words[x])
	for x in range(len(negative_words)):
		sent_index -= lower_text.count(negative_words[x])
	if '!' in text:
		sent_index *= exclamation_scaling * lower_text.count('!') + 1
	if '#' in text:
		sent_index *= hashtag_scaling * lower_text.count('#') + 1
	sent_index *= uppercase_scaling * sum(1 for c in text if c.isupper())
		
	sent_index = (sent_index/len(text)) * 15

	return sent_index


def passion_analyzer(text):
	""" Analyzes how much passion is in a statement
	
	input: text, a string to be analyzed
	returns: passion_index, a numerical rating of the passion in a statement
	"""

	lower_text = text.lower()

	hashtag_scaling = 0.3
	exclamation_scaling = 0.5
	uppercase_scaling = 0.2


	passion_index = 0

	for x in range(len(positive_words)):
		passion_index += (lower_text.count(positive_words[x]))**2
	for x in range(len(negative_words)):
		passion_index += (lower_text.count(negative_words[x]))**2
	if '!' in text:
		passion_index *= exclamation_scaling * lower_text.count('!') + 1
	if '#' in text:
		passion_index *= hashtag_scaling * lower_text.count('#') + 1
	passion_index *= uppercase_scaling * sum(1 for c in text if c.isupper())

	passion_index = math.sqrt(passion_index)/len(text)

	return passion_index


def get_sentiments(tweets):
	"""
	creates a list of sentiments given a list of tweets
	"""

	sentiments = []

	for x in range(len(tweets)):
		sentiments.append(sentiment_analyzer(tweets[x]))
	
	return sentiments


def get_passions(tweets):
	"""
	creates a list of passion indices given a list of tweets
	"""

	passions = []

	for x in range(len(tweets)):
		passions.append(passion_analyzer(tweets[x]))
	
	return passions

def iterated_sent_and_passion(data_list_of_lists):
	sentiment_lists = []
	passion_lists = []
	for x in range(len(data_list_of_lists)):
		sentiment_lists.append(get_sentiments(data_list_of_lists[x]))
		passion_lists.append(get_passions(data_list_of_lists[x]))

	return sentiment_lists, passion_lists


#pulling negative and positive words for sentiment analysis

url_neg = 'http://www.unc.edu/~ncaren/haphazard/negative.txt'
url_pos = 'http://www.unc.edu/~ncaren/haphazard/positive.txt'

urllib.urlretrieve(url_neg,'negative.txt')
urllib.urlretrieve(url_pos,'positive.txt')

pos_sent = open("positive.txt").read()
positive_words = pos_sent.split('\n')
neg_sent = open("negative.txt").read()
negative_words = neg_sent.split('\n')

positive_words.append('yes')
negative_words.append('no')


#pulling tweets from twitter

data_list = twitter_fetch('tweet_file2.txt')
keywords = ['barack obama','jeb bush','hillary clinton','john boehner','joe biden','scott walker','chris christie']
list_of_all_tweets = iterated_list_splitter(data_list,keywords[1::])
list_of_all_tweets = keyword_remover(list_of_all_tweets,keywords)

#get the sentiment and classify it for each keyword

sentiment_lists, passion_lists = iterated_sent_and_passion(list_of_all_tweets)

obama_sentiment = sentiment_lists[0]
bush_sentiment = sentiment_lists[1]
clinton_sentiment = sentiment_lists[2]
boehner_sentiment = sentiment_lists[3]
biden_sentiment = sentiment_lists[4]
walker_sentiment = sentiment_lists[5]
christie_sentiment = sentiment_lists[6]

obama_passion = passion_lists[0]
bush_passion = passion_lists[1]
clinton_passion = passion_lists[2]
boehner_passion = passion_lists[3]
biden_passion = passion_lists[4]
walker_passion = passion_lists[5]
christie_passion = passion_lists[6]

#plotting graphs

#you ended up repeating yourself a lot here! It might have been better to write a function to do this, where you pass in passion_lists and a list of names to map to. Then you could automate this/avoid repeating yourself. If you find yourself copy and pasting, think about how you could write a function and a for loop instead!
plt.scatter(obama_sentiment,obama_passion)
plt.grid(True)
plt.title('Barack Obama Twitter Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Emotion Level')
plt.ylim(0,5)
plt.xlim(-6,6)
plt.savefig('obama_sentiment.png')
plt.show()

plt.scatter(bush_sentiment,bush_passion)
plt.grid(True)
plt.title('Jeb Bush Twitter Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Emotion Level')
plt.ylim(0,5)
plt.xlim(-6,6)
plt.savefig('bush_sentiment.png')
plt.show()

plt.scatter(clinton_sentiment,clinton_passion)
plt.grid(True)
plt.title('Hillary Clinton Twitter Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Emotion Level')
plt.ylim(0,5)
plt.xlim(-6,6)
plt.savefig('clinton_sentiment.png')
plt.show()

plt.scatter(boehner_sentiment,boehner_passion)
plt.grid(True)
plt.title('John Boehner Twitter Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Emotion Level')
plt.ylim(0,5)
plt.xlim(-6,6)
plt.savefig('boehner_sentiment.png')
plt.show()

plt.scatter(biden_sentiment,biden_passion)
plt.grid(True)
plt.title('Joe Biden Twitter Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Emotion Level')
plt.ylim(0,5)
plt.xlim(-6,6)
plt.savefig('biden_sentiment.png')
plt.show()

plt.scatter(walker_sentiment,walker_passion)
plt.grid(True)
plt.title('Scott Walker Twitter Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Emotion Level')
plt.ylim(0,5)
plt.xlim(-6,6)
plt.savefig('walker_sentiment.png')
plt.show()

plt.scatter(christie_sentiment,christie_passion)
plt.grid(True)
plt.title('Chris Christie Twitter Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Emotion Level')
plt.ylim(0,5)
plt.xlim(-6,6)
plt.savefig('christie_sentiment.png')
plt.show()
