from imaplib import IMAP4_SSL
import email
from datetime import datetime

class IMAPMailBox():
    
    __imapclient:IMAP4_SSL
    __mail_ids:list
    
    def __init__(self, client:IMAP4_SSL) -> None:
        self.__imapclient = client
        
    
    def retrieve_mails_from(self,sender) -> bool:
        
        self.__imapclient.select('INBOX')
        status, search_data = self.__imapclient.search(None, '(FROM "{}")'.format(sender))
    
        if status == 'OK':
            self.__mail_ids = search_data[0].split()
            return True
        
        return False
    
    def get_latest_mail_id(self):
                               
        latest_email_id =  self.__mail_ids[-1:]  # get the latest 
        keys = map(int, latest_email_id)
        news_keys = sorted(keys, reverse=True)
        str_keys = [str(e) for e in news_keys] 
        return  str_keys[0]
    
    def get_email_subject(self,mail):
        return mail['Subject']
    
    def get_email_content(self,mail):
        body = ''
        
        if mail.is_multipart():
            for part in mail.walk():
                part_type = part.get_content_type()
                if part_type == 'text/plain':
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = mail.get_payload(decode=True).decode()      
        
        return body
    
    def get_email_date( self, mail ):
        date_str = mail['Date']
        date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        return date
    
    def parse_email( self,mail_id ):
        status, data = self.__imapclient.fetch( mail_id,'(RFC822)' )
        
        if status == 'OK':
            raw_email = data[0][1]
            email_content =  email.message_from_bytes(raw_email)
            return email_content
        
        return None