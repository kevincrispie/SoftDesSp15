import urllib
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
	if sent_index < -0.5:
		return 'negative'
	if sent_index <= 0.5 and sent_index >= -0.5:
		return 'neutral'
	if sent_index >= 0.5:
		return 'positive'

print sentiment_analyzer('I am happy yes yes yes!!!! #awesome')
print
print sentiment_analyzer('I am a bad kid. I am bad bad bad')

print classify_sentiment(sentiment_analyzer('I am a bad kid. I am bad bad bad'))

