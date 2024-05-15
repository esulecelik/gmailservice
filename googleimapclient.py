from imaplib import IMAP4_SSL
from jsonfileoperation import JSONFileOperation
from oauth2 import RefreshToken,GeneratePermissionUrl,AuthorizeTokens,GenerateOAuth2String
from datetime import datetime,timedelta
from imapmailbox import IMAPMailBox
import os
import ssl
import threading

class GoogleIMAPClient():
    
    imap_conn: IMAP4_SSL
    client_id: str
    client_secret: str
    tfile: JSONFileOperation
    email: str
    mailbox: IMAPMailBox
    
    __access_token: str | None
    __refresh_token: str | None
    __expires_in: str | None
    __granted_on: str | None
    
    def __init__(self, email, client_id, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.email = email
        
        self.tfile = JSONFileOperation('tokens')
        
        if not self.__get_tokens():
            self.__grant_token()
        
        if not self.__is_access_token_valid():
            self.__refresh_granted_token()
        
        self.connect_gmail()
        
         
    
    def connect_gmail(self):
        
        imap_oauth_str = GenerateOAuth2String( self.email,self.__access_token,False)
        self.imap_conn = IMAP4_SSL('imap.gmail.com', ssl_context=ssl.create_default_context())
        self.imap_conn.debug = 0   
        self.imap_conn.authenticate('XOAUTH2', lambda x: imap_oauth_str) 
        self.mailbox = IMAPMailBox( self.imap_conn )
        
    def get_connection(self):
        return self.imap_conn
        
    
    def __is_access_token_valid(self) -> bool:
        
        now =  datetime.now()
        
        granted_on = datetime.strptime( self.__granted_on, "%d/%m/%Y, %H:%M:%S")
        expire_on =  granted_on + timedelta(seconds = self.__expires_in)
           
        if now > expire_on:
            return False
        
        return True
    
    
    def __refresh_granted_token(self):
        
        response = RefreshToken(self.client_id,self.client_secret, self.__refresh_token)
        response['granted_on'] = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        response['refresh_token'] = self.__refresh_token
        
        self.__access_token = response['access_token']
        self.__refresh_token = response['refresh_token']
        self.__expires_in = response['expires_in']
        self.__granted_on =response['granted_on']
        
        
        self.tfile.write(response)
    

    def __grant_token(self):
        print('  %s' % GeneratePermissionUrl( self.client_id ))
        authorization_code = input('Enter verification code: ')
        response = AuthorizeTokens( self.client_id, self.client_secret, authorization_code)
        
        response['granted_on'] = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        
        self.__access_token = response['access_token']
        self.__refresh_token = response['refresh_token']
        self.__expires_in = response['expires_in']
        self.__granted_on =response['granted_on']

        
        self.tfile.write(response)

    
    def __get_tokens(self) -> bool:
        
        if self.tfile.is_exist():
            self.tfile.read()
            
            self.__access_token = self.tfile.get( 'access_token' )[0]
            self.__refresh_token = self.tfile.get( 'refresh_token' )[0]
            self.__expires_in = self.tfile.get( 'expires_in' )[0]
            self.__granted_on = self.tfile.get( 'granted_on' )[0]

            if None not in ( self.__access_token, self.__refresh_token, self.__expires_in, self.__granted_on ):
                return True
        
        
        
        return False
             

        
        