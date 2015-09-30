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
			with open('mail_'+str(index)+'.txt','w') as f:	
				f.write(text)
			index+=1

	
			
		
		'''#rem

oving the '>' marker from trailing mail content
		if len(parts) > 1:
			trailing=re.split(r'\n>[\s|>]',parts[2])

			trailing = ''.join(trailing)
						
			return parts[0],parts[1]+trailing

		else:
			return parts[0],''
		'''


	'''def extract_features(self):
		
		#extracts the Date content from header of contained reply
		try:
			f.write("Date : "+re.search('[A-Za-z0-9:\s,]+(AM|PM)',parts[1]).group(0)+ "\n");
		except:
			f.write("Date : Not available\n");


		#extracts the sender details from header of contained reply
		try	:
			f.write('From : '+re.search('[A-Za-z0-9._]+@([a-zA-Z].)+([a-zA-Z])+',parts[1]).group(0) + '\n')
		except:
			f.write("From : Not available\n")
	'''
