

from pattern.web import *
from pattern.en import *
import twitter
import json
import matplotlib.pyplot as plt 
import numpy as np

"""
get authorization from twitter (this has not been committed to GitHub)
"""

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

def twitter_fetch():
	twitter_api = twitter.Twitter(auth=auth)

	q = 'rick perry'
	count = 100

	search_results = twitter_api.search.tweets(q=q, count=count)

	statuses = search_results['statuses']

	for _ in range(5):
		print "Length of Statuses", len(statuses)
		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e:
			break

		kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])

		search_results = twitter_api.search.tweets(**kwargs)
		statuses += search_results['statuses']

	print json.dumps(statuses[0],indent=1)


def get_sentiment(text):
	'''
	input: text, the text of a tweets
	returns: sentiment, objectivity, elements of a tuple that results from the sentiemnt test
	'''
	feeling, objectivity = sentiment(text)
	return feeling, objectivity

def get_sentiments(tweets):
	sentiments = []
	for x in range(len(tweets)):
		feeling, objectivity = get_sentiment(tweets[x])
		sentiments.append(feeling)
	return sentiments

def get_objectivity(tweets):
	objectivities = []
	for x in range(len(tweets)):
		feeling, objectivity = get_sentiment(tweets[x])
		objectivities.append(objectivity)
	return objectivities

def get_average(sentiments):
	return sum(sentiments)/len(sentiments)

bob_tweets = ["bob is great","bob is nice", "bob is my friend", "bob is mean", "bob is evil","bob is the best ever","bob", "fred", "joe is cool"]
bob_sentiments = get_sentiments(bob_tweets)
bob_objectivity = get_objectivity(bob_tweets)
print bob_objectivity
print bob_sentiments
bob_opinion = get_average(bob_sentiments)

george_tweets = ["bob is great","bob is nice", "bob is my friend", "bob is mean"]
george_sentiments = get_sentiments(george_tweets)
george_objectivity = get_objectivity(george_tweets)
george_opinion = get_average(george_sentiments)

tim_tweets = ["bob is great","bob is nice", "bob is my friend", "bob is mean"]
tim_sentiments = get_sentiments(tim_tweets)
tim_objectivity = get_objectivity(tim_tweets)
tim_opinion = get_average(tim_sentiments)

jim_tweets = ["bob is great","bob is nice", "bob is my friend", "bob is mean"]
jim_sentiments = get_sentiments(jim_tweets)
jim_objectivity = get_objectivity(jim_tweets)
jim_opinion = get_average(jim_sentiments)

richard_tweets = ["bob is not great","bob is a terrible teacher", "bob is not my friend", "bob is really mean"]
richard_sentiments = get_sentiments(richard_tweets)
richard_objectivity = get_objectivity(richard_tweets)
richard_opinion = get_average(richard_sentiments)

leo_tweets = ["bob is great","bob is nice", "bob is my friend", "bob is mean"]
leo_sentiments = get_sentiments(leo_tweets)
leo_objectivity = get_objectivity(leo_tweets)
leo_opinion = get_average(leo_sentiments)

opinion = [bob_opinion,george_opinion, tim_opinion, jim_opinion, richard_opinion, leo_opinion]
objectivity = [bob_objectivity, get_objectivity, tim_objectivity, jim_objectivity, richard_objectivity, leo_objectivity]

people = ('bob','george','tim','jim','richard','leo')
#y_pos = np.arange(len(people))
#plt.barh(y_pos, opinion, align = 'center', alpha=0.4)
#plt.yticks(y_pos,people)
#plt.xlabel('Opinion')
#plt.title('Twitter Opinion')

#plt.show()


#plt.hist(leo_sentiments)
#plt.xlabel('opinion')
#plt.ylabel('frequency')
#plt.title('Historgram')

#plt.show()

plt.scatter(bob_sentiments,bob_objectivity)
plt.grid(True)
plt.xlabel('Sentiment')
plt.ylabel('Objectivity')
plt.show()


