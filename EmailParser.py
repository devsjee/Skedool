from nltk.tokenize import RegexpTokenizer


class EmailParser:
	def __init__(self,filename):
		self.filename = filename

	
	def read_file(self):
		with open(self.filename,'r') as f:
			mailtext = f.readlines()
			mailtext = ''.join(mailtext)
			return mailtext
			
	def split_mail(self):

		mailtext = self.read_file()
		mails = self.tokenize_mail(mailtext)
		self.write_mail(mails)


	def tokenize_mail(self,mailtext):
		mails = []
	
		#splits entire mail into three parts : original mail, header of contained reply, reply mail
		tokenizer = RegexpTokenizer('\n[>|\s]*On[\s]* ([a-zA-Z0-9, :/<>@\.\"\[\]\r\n]*[\s]* wrote:)',gaps = True)
		mail_indices = tokenizer.span_tokenize(mailtext)
		
		
		start = end = 0
		for index in mail_indices:
			end = index[1]+1
			mails.append(mailtext[start:end])
			start = end

		return mails

	def write_mail(self,mails):
		index = 0

		for text in mails:
			Date_tokenizer = RegexpTokenizer('[A-Za-z0-9:, ]+(AM|PM)')
			From_tokenizer = RegexpTokenizer('[A-Za-z0-9._]+@(([a-zA-Z])+.)+([a-zA-Z])+')
				
			with open('mail_'+str(index)+'.txt','w') as f:	
				f.write("Date :"+  str(Date_tokenizer.tokenize(text)) +"\n");
				f.write("From :"+ str(From_tokenizer.tokenize(text)) +"\n");
				f.write(text)
	
			index+=1

	
			

