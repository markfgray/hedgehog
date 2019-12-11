from nltk.tokenize import word_tokenize  
from nltk.corpus import stopwords  
from collections import Counter
import json

def generate(comments):
	words = []
	for comment in comments:
		tokens = word_tokenize(comment)
		words.extend(tokens)

	stop_words = set(stopwords.words('english'))
	
	qual_words = {
	"good", "lovely", "nice", "great", "terrible", "awful", "bad", "decent", "bit",
	"very", "really"
	}
	for i in qual_words:
		stop_words.add(i)
	
	words = [word.lower() for word in words if word.lower() not in stop_words and len(word)>2]

	words_freq = Counter(words)
	
	words_json = [{'text': word, 'weight': count} for word, count in words_freq.items()]

	# json.dumps is used to convert json object i.e. dictionary or list into a string
	return json.dumps(words_json)