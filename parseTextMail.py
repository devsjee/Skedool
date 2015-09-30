import re
import sys


def readFile(filename):
	'''
	Input : filename/filepath

	This functions opens the given filename in read mode and forms a single string
	of all lines in the file without stripping the \n and \r characters

	Returns the string of filetext
	'''
	try:
		f = open(filename,'r')
	except:
		print("Wrong file or file path")	
		return -1
	else:
		data = f.readlines()

		mailtext = ""
		for line in data:
			mailtext+=line
		return mailtext


def split(mailtext,output):
	'''
	Input : mailtext (output from readFile function)
	output : filename/filepath of the output file to which processed output is to be written
	
	This function separates the reply mails from current mail context along with the sender and sending time
	of the reply mail
	'''
	f = open(output,'w')

	#splits entire mail into three parts : original mail, header of contained reply, reply mail
	parts = re.split("On ([a-zA-Z0-9, :/<>@\.\"\[\]\r\n]* wrote:)",mailtext)

	#writes the original mail to output file
	f.write(parts[0])

	f.write("-----------------\n Separate Structure\n-----------------\n{")


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

	#writes the contained reply to output file after removing the '>' marker
	f.write('Text : ')
	try:
		oldmail = re.split(r'\s>\s',parts[2])
		for line in oldmail:
			f.write(line)
	except:
		f.write("--- Not available---")	
		
	f.write('\n}')
	f.close()


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print 'Usage : parseTextMail.py <input_filename> <output_filename>'
	else:
		mail = readFile(str(sys.argv[1]))	#reads the input file
		if mail!=-1:
			split(mail,str(sys.argv[2]))	#splits the mailtext and writes to output file
