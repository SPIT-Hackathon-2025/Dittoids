import os
import base64
import sqlite3
import time
import requests
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DB_FILE = "mail.db"  # Ensure consistent database file usage

def get_gemini_response(message):
    """Fetches priority rating from Gemini API."""
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": message}]}]}

    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "1").strip()
    except requests.RequestException as e:
        print(f"Gemini API Error: {e}")
        return "1"  # Default priority if API call fails

def get_body(payload):
    """Extracts email body from payload."""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif part['mimeType'] == 'multipart/alternative':
                return get_body(part)  # Recursive call for nested parts
    elif 'body' in payload and 'data' in payload['body']:
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    return ""

def setup_database():
    """Creates the emails table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            my_email TEXT,
            sender_email TEXT,
            timestamp TEXT,
            subject TEXT,
            body TEXT,
            priority INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_email_to_db(email_data):
    """Saves email data to the database, preventing duplicates."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check for duplicate entry
    cursor.execute("SELECT body FROM mail ORDER BY ROWID DESC LIMIT 1")
    latest_entry = cursor.fetchone()
    if latest_entry and latest_entry[0] == email_data['Body']:
        print("Duplicate entry detected, skipping.")
        conn.close()
        return
    
    cursor.execute('''
        INSERT INTO mail (my_email, sender_email, timestamp, subject, body, priority)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (email_data['my_email'], email_data['From'], email_data['Date'], email_data['Subject'], email_data['Body'], email_data['Priority']))
    
    conn.commit()
    conn.close()
    print(f"Saved email from {email_data['From']} to database with priority {email_data['Priority']}.")

def main():
    """Main function to check unread Gmail messages and store them in the database."""
    setup_database()
    creds = None

    # Load credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # Authenticate if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        
        while True:
            messages = service.users().messages().list(userId="me", q="is:unread", maxResults=1).execute().get("messages", [])
            
            if messages:
                msg_id = messages[0]["id"]
                message = service.users().messages().get(userId="me", id=msg_id).execute()
                headers = message['payload']['headers']

                email_data = {'my_email': 'myemail@example.com'}  # Replace with actual email
                for header in headers:
                    if header['name'] == 'Date':
                        email_data['Date'] = header['value']
                    if header['name'] == 'From':
                        email_data['From'] = header['value']
                    if header['name'] == 'Subject':
                        email_data['Subject'] = header['value']
                
                email_data['Body'] = get_body(message['payload'])
                
                # Generate priority score using Gemini API
                context = f"From: {email_data['From']}\nSubject: {email_data['Subject']}\nBody: {email_data['Body']} . This is the information of an email, from a scale of 1 to 5 rate its priority, where 5 is the highest priority and 1 is the lowest priority. Make sure to answer only in one single-digit number."
                priority_response = get_gemini_response(context)
                
                try:
                    email_data['Priority'] = int(priority_response) if priority_response.isdigit() else 1
                except ValueError:
                    email_data['Priority'] = 1  # Default to 1 if response is invalid
                
                save_email_to_db(email_data)
            else:
                print("No unread messages found.")

            time.sleep(300)

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
