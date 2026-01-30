import os 
import pickle
import datetime
import engine
import requests,json
import urllib
import webbrowser
import socket
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    try:
        # Check if credentials.json exists
        if not os.path.exists('credentials.json'):
            print("WARNING: credentials.json not found.")
            print("To enable Google Calendar features, please:")
            print("1. Go to https://console.cloud.google.com/")
            print("2. Create a new project and enable Google Calendar API")
            print("3. Create OAuth 2.0 credentials (Desktop app)")
            print("4. Download and save as 'credentials.json' in this directory")
            print("\nRunning without Google Calendar integration...\n")
            return None
        
        creds = None
    
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        
        return service

    except Exception as e:
        print(f"Authentication error: {e}")
        engine.speak("sorry master"+str(e))
        return None

    
