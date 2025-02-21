from flask import Blueprint, render_template, jsonify, session, url_for, redirect, request
from google.oauth2.credentials import Credentials
from app.services.gmail_service import GmailService
from app.services.detector_service import PhishingDetector
import os

bp = Blueprint('main', __name__)
gmail_service = GmailService('credentials.json')

@bp.route('/')
def index():
    if 'credentials' not in session:
        return render_template('login.html')
    return render_template('dashboard.html')

@bp.route('/authorize')
def authorize():
    flow = gmail_service.initialize_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@bp.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = gmail_service.initialize_flow()
    
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('main.index'))

@bp.route('/analyze', methods=['POST'])
def analyze_emails():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    credentials = Credentials(**session['credentials'])
    detector = PhishingDetector(os.getenv('OPENAI_API_KEY'))
    
    try:
        emails = gmail_service.get_emails(credentials)
        results = []
        
        for email in emails:
            analysis = detector.analyze_email(email['content'])
            results.append({
                'email': email,
                'analysis': analysis
            })
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500