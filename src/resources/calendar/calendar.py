from src.resources.calendar.auth import Auth

import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

_CREDENTIALS_TOKEN_PATH = 'src/resources/calendar/credentials/token.json'
_CREDENTIALS_PATH = 'src/resources/calendar/credentials/credentials.json'

class Calendar():
    
    def __init__(self):
        self.auth = Auth(_CREDENTIALS_PATH, _CREDENTIALS_TOKEN_PATH, SCOPES)
        self.__credentials = self.auth.get_auth_credentials()
        self.auth_url = self.auth.get_auth_url()
        
    def check_authorization(self):
        return self.auth.check_login_stat()
    
    def login_with_token(self, code):
        if not self.check_authorization() and self.auth.is_auth_session_in_progress() and self.auth.authorize(code):
            self.__credentials = self.auth.get_auth_credentials()
        return self.check_authorization()
    
    def read(self, next_n_events=10):
        try:
            service = build('calendar', 'v3', credentials=self.__credentials)
            print(f'Getting the upcoming {next_n_events} events:')
            events_result = service.events().list(
                    calendarId='primary', 
                    timeMin=datetime.datetime.utcnow().isoformat() + 'Z',
                    maxResults=10, 
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
            events = events_result.get('items', [])
            return events
        except HttpError as error:
            print(f'HTTP Error: {error}')
            
    def create_event(self, event):
        try:
            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
        except HttpError as error:
            print(f'HTTP Error: {error}')
        
                
        
    
'''

calendar -
    logged in
        calendar actions
    
    not logged in
        start auth session
        calendar actions


'''
            
            