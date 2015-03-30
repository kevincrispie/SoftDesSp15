"""
This file is where I experimented and wrote my own sentiment sentiment_analyzer
The full implementation is in twitter_trends.py
"""

import urllib
import math

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

def sentiment_analyzer(text):
	""" Analyzes hthe sentiment of a statement
	
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
		
	return sent_index


def classify_sentiment(sent_index):
	""" classifies the sentiemnt of a statement into positive, neutral, or negative

	input: sent_index, a numerical rating of the sentiment of a statement
	returns: a string classifying the sentiment
	"""

	if sent_index < -0.5:
		return 'negative'
	if sent_index <= 0.5 and sent_index >= -0.5:
		return 'neutral'
	if sent_index >= 0.5:
		return 'positive'


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
		passion_index -= (lower_text.count(negative_words[x]))**2
	if '!' in text:
		passion_index *= exclamation_scaling * lower_text.count('!') + 1
	if '#' in text:
		passion_index *= hashtag_scaling * lower_text.count('#') + 1
	passion_index *= uppercase_scaling * sum(1 for c in text if c.isupper())


		
	return math.sqrt(passion_index)

	

#best to put code that you mean to test inside a separate function, or at least under a if __name__ == '__main__': statement so that it doesn't run when imported.
print sentiment_analyzer('I am happy yes yes yes!!!! #awesome')
print
print sentiment_analyzer('I am a bad kid. I am bad bad bad')

print classify_sentiment(sentiment_analyzer('I am a bad kid. I am bad bad bad'))
print
print subjectivity_analyzer('this is a neutral statement')
