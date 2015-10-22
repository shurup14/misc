import poplib
import re
import smtplib
from email import parser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
import email
import mimetypes
import os

class get_email:
    
    def __init__(self):
        self.stack = []
          
    def gettingletters(self,user,pasw,serv,port):
        
        # This function returns a list of emails that were in the subject of emeails
        
        Mailbox = poplib.POP3 (serv, port)
        Mailbox.user(user)
        Mailbox.pass_(pasw)
        resp, lst, octets = Mailbox.list()
        
        #print ("DEBUG: Total messages: %s" % ( len(lst))) #Debug info about count of letters in box.
        
        messages = [Mailbox.retr(i) for i in range(1, len(Mailbox.list()[1]) + 1)]
        messages = [b"\n".join(mssg[1]) for mssg in messages]
        messages = [parser.Parser().parsestr(mssg.decode( "utf-8" )) for mssg in messages]
        i=1
        
        #finding emails in subjects
        
        for message in messages:
            subject="{} \n".format(message['subject'])
            mailPattern=re.search(r'[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*', subject)
            if mailPattern is not None:
                self.profitMail = mailPattern.group(0)
                self.stack.append(mailPattern.group(0))
                
                #print ("DEBUG: Mail number %s : %s " % (i,mailPattern.group(0)))  #Debug info
                
                #Below we write logs of finded emails
                
                outf = open('logs.txt', 'a')
                outf.write(self.profitMail + '\n')
                outf.close()
                
         # Mailbox cleaning
         
        #for z in range(1,len(lst)+1):
         #       Mailbox.dele(z)
       # Mailbox.quit()
        print ("DEBUG: Consist of stack : %s" %(self.stack))
        
        return self.stack

    
    def send_email(self,user,pasw,serversmtp,portsmtp,list_mails,subj,attach_file,answer_text): 
        
        # Settings
            
        mail_coding = 'utf-8'

        #Read text of answer
        
        opensletter = open(answer_text,'r')
        letter=opensletter.read()
        opensletter.close()        

        multi_msg = MIMEMultipart()
        multi_msg['Subject'] = subj

        #Add text

        msg = MIMEText(letter, "html", "utf-8")
        msg.set_charset(mail_coding)
        multi_msg.attach(msg)

        #Add file
        
        if(os.path.exists(attach_file) and os.path.isfile(attach_file)):
            file = open(attach_file, 'rb')
            attachment = MIMEBase('application', "octet-stream")
            attachment.set_payload(file.read())
            email.encoders.encode_base64(attachment)
            file.close()
            only_name_attach = Header(os.path.basename(attach_file),mail_coding);
            attachment.add_header('Content-Disposition','attachment; filename="%s"' % only_name_attach)
            multi_msg.attach(attachment)
        else:
            if(attach_file.lstrip() != ""):
                print("File not found - " + attach_file)

         
        # Sending
        
        for i in list_mails:
            mailBoxout = smtplib.SMTP(serversmtp, portsmtp)
            mailBoxout.ehlo()
            mailBoxout.login(user, pasw)
            mailBoxout.sendmail(user, i, multi_msg.as_string())
            mailBoxout.quit()
