from nltk.tokenize import RegexpTokenizer


class EmailParser:
	"""
	The email to be parsed could be either passed through the filename
	or given directly as text
	i)	to read from file, the class takes the name of the file during instantiation, followed by 
		the user call to the member function 'split_mail'
	ii) 	to pass the mail content directly, call the 'tokenize_mail' member function
	"""

	def __init__(self,filename=''):
		self.filename = filename

	
	def read_file(self):
		"""
			reads the file and returs a string containing the mailcontent
		"""
		with open(self.filename,'r') as f:
			mailtext = f.readlines()
			mailtext = ''.join(mailtext)
			return mailtext


	def tokenize_mail(self,mailtext):
		"""
		this function uses the RegexpTokeniser to split the mail text on the pattern defined
		Each split is a separate mail. 
		Returns a list of mails contained in the given mailtext
		"""
		
		mails = []
	
		#splits entire mail into parts matching the 'On <Date Time> <person@mail.com> wrote:' pattern
		tokenizer = RegexpTokenizer('\n[>|\s]*On[\s]* ([a-zA-Z0-9, :/<>@\.\"\[\]\r\n]*[\s]* wrote:)',gaps = True)
		mail_indices = tokenizer.span_tokenize(mailtext)
		
		#uses the splits' offset information from span_tokenize to split the actual mailcontent
		#stores each split as an element of a list named 'mails'
		start = end = 0
		for index in mail_indices:
			end = index[1]+1
			mails.append(mailtext[start:end])
			start = end

		return mails	#list of the contained mails within a single mailtext


	def write_mail(self,mails):
		"""
		creats a separate file for each of the contained mails
		extracts the Date and Sender information from the individual contained mail
		writes the info to the file 
		"""
		index = 0

		for text in mails:
			Date_tokenizer = RegexpTokenizer('[A-Za-z0-9:, ]+(AM|PM)')
			From_tokenizer = RegexpTokenizer('[A-Za-z0-9._]+@(([a-zA-Z])+.)+([a-zA-Z])+')
				
			with open('mail_'+str(index)+'.txt','w') as f:	
				f.write("Date :"+  str(Date_tokenizer.tokenize(text)) +"\n");
				f.write("From :"+ str(From_tokenizer.tokenize(text)) +"\n");
				f.write(text)
	
			index+=1

			
	def split_mail(self):
		"""
			this function consolidates the actions of the EmailParser class.
			It reads the mail content from mail, tokenises it to separate mails
			and writes the individual mails to separate files
		"""
		mailtext = self.read_file()
		mails = self.tokenize_mail(mailtext)
		self.write_mail(mails)


	
	
			

