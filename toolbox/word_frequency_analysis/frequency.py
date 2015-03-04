""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string
import collections

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	f = open(file_name, 'r')
	lines = f.read()
		
	start_string = 'START OF THIS PROJECT GUTENBERG EBOOK'
	end_string = 'END OF THIS PROJECT GUTENBERG EBOOK'
	lines = lines[lines.find(start_string)+len(start_string):lines.find(end_string)]


	
	lines = lines.translate(string.maketrans("",""), string.punctuation)

	word_list = lines.split()

	return word_list

def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""

	d = collections.defaultdict(int)
	for word in word_list:
		d[word] += 1

	sorted_d = sorted(d.items(), key=lambda x:x[1]) 
	sorted_ascending = sorted_d[::-1]

	top_words = sorted_ascending[0:n]

	return top_words

word_list = get_word_list("the_prince.txt")
top_words = get_top_n_words(word_list,100)

print 'The top 100 words in The Prince are:\n'
i = 1
for top_word in top_words:
	print i, top_word[0]
	i += 1


