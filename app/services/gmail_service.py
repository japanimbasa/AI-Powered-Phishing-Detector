from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from flask import url_for
import base64

class GmailService:
    def __init__(self, credentials_path):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.credentials_path = credentials_path
        
    def initialize_flow(self):
        """Initialize OAuth2 flow"""
        return Flow.from_client_secrets_file(
            self.credentials_path,
            scopes=self.SCOPES,
            redirect_uri=url_for('main.oauth2callback', _external=True)
        )
        
    def get_emails(self, credentials, max_results=10):
        """Fetch recent emails using Gmail API"""
        service = build('gmail', 'v1', credentials=credentials)
        results = service.users().messages().list(
            userId='me', maxResults=max_results
        ).execute()
        
        messages = []
        for message in results.get('messages', []):
            msg = service.users().messages().get(
                userId='me', id=message['id'], format='full'
            ).execute()
            
            content = self._get_email_content(msg)
            messages.append({
                'id': message['id'],
                'subject': self._get_header(msg, 'Subject'),
                'from': self._get_header(msg, 'From'),
                'date': self._get_header(msg, 'Date'),
                'content': content
            })
            
        return messages
    
    def _get_email_content(self, message):
        """Extract email content from message payload"""
        if 'data' in message['payload']['body']:
            content = base64.urlsafe_b64decode(
                message['payload']['body']['data']
            ).decode('utf-8')
        else:
            parts = message['payload'].get('parts', [])
            content = ""
            for part in parts:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    content += base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8')
        return content
    
    def _get_header(self, message, header_name):
        """Extract header value from email message"""
        headers = message['payload']['headers']
        for header in headers:
            if header['name'] == header_name:
                return header['value']
        return ''
