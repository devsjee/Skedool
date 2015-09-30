import csv
import nltk 
from EmailParser import EmailParser
from nltk.corpus import stopwords
import random

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression


class learn_meeting_model:
	"""
	This class has member functions to read data from a 'csv' file, create feature sets out of it,
	train a logistic regression classifier on the featuresets and print the cross validated results.
	"""

	def __init__(self,filename,level=1):
		"""filename (for e.g., <location_data.csv> )is passed during instantiation of the class.
		level is the number of self-contained mails that has to be considered for training
		"""
		self.filename = filename
		data_table = self.read_csv()	#reads the datafile
		featuresets = self.create_featuresets(data_table,level)	#creates feature sets
		self.learn_model(featuresets)	#trains and tests a classifier
		

	def read_csv(self):		
		"""
		uses the csv package to read the data from csv file.
		stores the data internally in the form of list of lists
		"""
		data_table = []
		with open(self.filename,'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				data_table.append(row)
			
		return data_table



	def extract_mail(self,data_table,level=1):
		"""
		this function processes the data_table row by row and for each row(i.e. each mail) extracts the contained mail
		(upto the mentioned level) 

		Returns two variables : cleaned_data and all_words

		cleaned_data : a list of lists in the form [[(set of unique words in a mail),label of mail]]  --> extracts only the mailtext 
		and label from the original data_table read from the csv file
		
		all_words : the list containing all words across all mails for the purpose of finding out the most frequent words
		in the process of feature set creation
		"""

		cleaned_data = []
		all_words = []

		for row in data_table:
			mailtext = row[-2]
			category = row[-1]

			mailParser = EmailParser()
			mails= mailParser.tokenize_mail(mailtext)	#gets the contained mails within each mail
			
			row_words = set()

			for i in range(level):	#level of nesting of replies to be considered for feature creation
				mail_words = nltk.word_tokenize(mails[i].decode("utf8"))
				for word in mail_words:
					row_words.add(word)    #adding the words in current mail to a set to get unique tokens
					all_words.append(word) #cumulating the words for frequency counting

			cleaned_data.append([row_words,category]) #each item in cleaned data is [<set of words in mail>, label]

		return all_words,cleaned_data


	def remove_stopwords(self,all_words):
		"""
		Before using the most frequent words as features, it is processed to remove
		the stop words taken from nltk.corpus
		"""
		stop_words = stopwords.words('english')
		new_words = []
		for word in all_words:
			if word not in stop_words:
				new_words.append(word)

		return new_words


	def find_features(self,words,word_features):
		"""
		this function creates a feature vector(in the form of a dict) for each mail
		Each unique token in the mail is checked for it's presence in the word_features (most frequent words identified
		as features)
		"""
		features = {}
		
		for w in word_features:
			features[w] = (w in words)
		
		return features
		

	def create_featuresets(self,data_table,level=1):
		"""
		Forms the cleaned data out of orginal data_table
		Creates 'all_words' which is a collection of all words across all mails in tha data_table
		Removes stopwords from the 'all_words'
		Identifies the word_features based on frequency
		Creates and returns the featuresets for mails in the cleaned_data
		"""

		all_words,cleaned_data = self.extract_mail(data_table,level)
		all_words = self.remove_stopwords(all_words)

		all_words = nltk.FreqDist(all_words)
		word_features = list(all_words.keys())[:2000]

		featuresets = [(self.find_features(mail,word_features),label) for (mail,label) in cleaned_data]

		return featuresets

	def learn_model(self,featuresets):
		"""
		trains and tests the logistic regression classifier on the data
		"""
		random.shuffle(featuresets)
	
		limit = int(0.75*len(featuresets)) #partitioning 3:1 for train:test
		train_set = featuresets[:limit]
		test_set = featuresets[limit:]
	
		lr_classifier = SklearnClassifier(LogisticRegression())
		lr_classifier.train(train_set)
		
		print 'Logistic classifier Accuracy : ',str(nltk.classify.accuracy(lr_classifier,test_set)*100)


		#nb_classifier = nltk.NaiveBayesClassifier.train(train_set)
		
		#print 'Naive Bayes classifier Accuracy : ',str(nltk.classify.accuracy(nb_classifier,test_set)*100)
		#nb_classifier.show_most_informative_features(30)
