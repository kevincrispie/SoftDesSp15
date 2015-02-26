"""
This is a file where I researched and experimented using an API to pull tweets from twitter
The full Twitter analysis code is in twitter_trends.py
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pattern.en import *
from pattern import *

"""
get authorization from twitter (this has not been committed to GitHub)
"""

def get_sentiment(text):
	'''
	input: text, the text of a tweets
	returns: sentiment, objectivity, elements of a tuple that results from the sentiemnt test
	'''
	feeling, objectivity = sentiment(text)
	return feeling, objectivity

class listener(StreamListener):

    def on_data(self, data):
        tweet = data.split(',"text":"')[1].split('","source')[0]
        sentimentRating, objectivity = get_sentiment(tweet)

        saveMe = tweet+'::'+sentimentRating+"\n"
        output = open('output.csv','a')
        output.write(saveMe)
        output.close()
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["congress"])