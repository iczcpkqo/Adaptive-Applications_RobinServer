from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

class Auth():
    def __init__(self, credentials_path, credentials_token_path, scopes):
        self.__credentials = None
        self.auth_session = None
        self.CREDENTIALS_PATH = credentials_path
        self.CREDENTIALS_TOKEN_PATH = credentials_token_path
        self.SCOPES = scopes
    
    def is_credentials_valid(self):
        if not self.__credentials or not self.__credentials.valid:
            return False
        return True
    
    def check_login_stat(self):
        if os.path.exists(self.CREDENTIALS_TOKEN_PATH):
            self.__credentials = Credentials.from_authorized_user_file(self.CREDENTIALS_TOKEN_PATH, self.SCOPES)

        return self.is_credentials_valid()
        
        
    def get_auth_url(self):
        if not self.check_login_stat():
            flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_PATH, self.SCOPES)
            flow.redirect_uri = flow._OOB_REDIRECT_URI
            auth_url, _ = flow.authorization_url(prompt='consent')
            self.auth_session = {"flow": flow, "auth_url": auth_url, "in_Progress": True}
            return auth_url
        return None
    
    def is_auth_session_in_progress(self):
        if (self.auth_session and "in_Progress" in self.auth_session and self.auth_session["in_Progress"]):
            return True
        return False
    
    def authorize(self, code):
        if self.is_auth_session_in_progress():
            self.auth_session["flow"].fetch_token(code=code)
            self.__credentials = self.auth_session["flow"].credentials
        
        if self.is_credentials_valid():
            with open(self.CREDENTIALS_TOKEN_PATH, 'w') as token:
                token.write(self.__credentials.to_json())
            self.auth_session = None
            return True
        return False   
    
    def get_auth_credentials(self):
        if self.check_login_stat():
            return self.__credentials
        return None