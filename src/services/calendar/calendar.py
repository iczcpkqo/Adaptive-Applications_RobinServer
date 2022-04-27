from src.services.calendar.auth import Auth

import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

_CREDENTIALS_TOKEN_PATH = 'src/services/calendar/credentials/token.json'
_CREDENTIALS_PATH = 'src/services/calendar/credentials/credentials.json'

class Calendar():
    
    def __init__(self):
        self.auth = Auth(_CREDENTIALS_PATH, _CREDENTIALS_TOKEN_PATH, SCOPES)
        self.__credentials = self.auth.get_auth_credentials()
        self.auth_url = self.auth.get_auth_url()
        self.cal_service = None
        
    def check_authorization(self):
        return self.auth.check_login_stat()
    
    def login_with_token(self, code):
        if not self.check_authorization() and self.auth.is_auth_session_in_progress() and self.auth.authorize(code):
            self.__credentials = self.auth.get_auth_credentials()
        return self.check_authorization()
    
    def get_cal_service(self):
        if self.cal_service == None:
            self.cal_service = build('calendar', 'v3', credentials=self.__credentials)
        return self.cal_service
    
    def read(self):
        try:
            print(f'Getting events:')
            events_result = self.get_cal_service().events().list(
                    calendarId='primary', 
                    timeMin='2022-01-01T00:00:00Z',
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
            events = events_result.get('items', [])
            return events
        except HttpError as error:
            print(f'HTTP Error: {error}')
            
    def create_event(self, event):
        try:
            event = self.get_cal_service().events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
            return True
        except HttpError as error:
            print(f'HTTP Error: {error}')
            return False
        
                
        
    
'''

calendar -
    logged in
        calendar actions
    
    not logged in
        start auth session
        calendar actions


'''
            
            