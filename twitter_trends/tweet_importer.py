from pattern.web import *
from pattern.en import *

"""
Tokens removed from github push
"""


def tweet_importer():
	"""
	Obtains tweets from twitter and stores them in a text file to be used by another program
	"""

	liscense["Twitter"] = (
	CONSUMER_KEY, # OAuth (key, secret, token)
	CONSUMER_SECRET,(OATH_TOKEN, OAUTH_TOKEN_SECRET))


def get_tweets(search_term):
	"""
	gets tweets from twitter using a specific search term and writes the result to a text
	file. It puts a label on each section of tweets according to the search term and
	prints a new line each time.
	"""

	t = Twitter()
	i = None
	tweet_file = open("tweet_file2.txt", "a")
	tweet_file.write(search_term + '\n')
	tweet_file.close()
	for j in range(3):
		for tweet in t.search(search_term, start = 1, count = 3):
			tweet_file = open("tweet_file2.txt", "a")
			tweet_file.write(tweet.text + '\n')
			i = tweet.id
			tweet_file.close()	


"""
The following code is written the way it is because I wanted to import tweets 
one keyword at a time. 
"""

#search_terms = ['barack obama','jeb bush','hillary clinton','john boehner','joe biden','scott walker','chris christie']
#get_tweets('barack obama')
#time.sleep(3*60)

#get_tweets('jeb bush')
#time.sleep(3*60)
#get_tweets('hillary clinton')
#time.sleep(3*60)
#get_tweets('john boehner')
#time.sleep(3*60)
#get_tweets('scott walker')
#time.sleep(3*60)
#get_tweets('joe biden')
#get_tweets('chris christie')

