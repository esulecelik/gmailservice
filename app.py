from jsonfileoperation import JSONFileOperation
from googleimapclient import GoogleIMAPClient
import time
from windows_toasts import WindowsToaster, Toast

if __name__ == '__main__':
    
    cfile = JSONFileOperation('oauth2client')
    
    if cfile.is_exist():
        cfile.read()
        email, cid, csecret = cfile.get( 'email', 'client_id', 'client_secret' )
        cimap = GoogleIMAPClient( email, cid, csecret )
        
        sender = 'no-reply@apply.42istanbul.com.tr'
      
        if cimap.mailbox.retrieve_mails_from(sender):
            latest_mail_id = cimap.mailbox.get_latest_mail_id()
            
        while True:
           
            current_latest_email_id: str
            
            if cimap.mailbox.retrieve_mails_from(sender):
                current_latest_email_id = cimap.mailbox.get_latest_mail_id()
               
               
            if current_latest_email_id != latest_mail_id:
                
                new_email = cimap.mailbox.parse_email(current_latest_email_id)
                
                subject = cimap.mailbox.get_email_subject(new_email)
                date = cimap.mailbox.get_email_date(new_email)               
         
                toaster = WindowsToaster(sender)
                newToast = Toast()
                newToast.text_fields = [subject]
                toaster.show_toast(newToast)
         
                latest_mail_id = current_latest_email_id 

            time.sleep(5)