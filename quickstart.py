
import os.path
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

def get_gemini_response(message):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY  # Google Gemini API uses a query param, not an Authorization header
    }
    data = {
        "contents": [{"parts": [{"text": message}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response received.")
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Connection error occurred: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Timeout error occurred: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        return f"An error occurred: {req_err}"

def get_body(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif part['mimeType'] == 'multipart/alternative':
                return get_body(part)
    else:
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

def save_email_to_db(email_data):
    conn = sqlite3.connect('mail.db')
    cursor = conn.cursor()
    
    # Check for duplicate entry based on the body
    cursor.execute('''
        SELECT body FROM emails ORDER BY ROWID DESC LIMIT 1
    ''')
    latest_entry = cursor.fetchone()
    if latest_entry and latest_entry[0] == email_data['Body']:
        print("Duplicate entry")
        conn.close()
        return
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            my_email TEXT,
            sender_email TEXT,
            timestamp TEXT,
            subject TEXT,
            body TEXT,
            priority INTEGER
        )
    ''')
    cursor.execute('''
        INSERT INTO emails (my_email, sender_email, timestamp, subject, body, priority)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (email_data['my_email'], email_data['From'], email_data['Date'], email_data['Subject'], email_data['Body'], email_data['Priority']))
    conn.commit()
    conn.close()

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        while True:
            messages = service.users().messages().list(userId="me", q="is:unread", maxResults=1).execute().get("messages", [])
            if messages:
                message = service.users().messages().get(userId="me", id=messages[0]["id"]).execute()
                headers = message['payload']['headers']
                email_data = {'my_email': 'myemail@example.com'}  # Replace with your email
                for header in headers:
                    if header['name'] == 'Date':
                        email_data['Date'] = header['value']
                    if header['name'] == 'From':
                        email_data['From'] = header['value']
                    if header['name'] == 'Subject':
                        email_data['Subject'] = header['value']
                email_data['Body'] = get_body(message['payload'])
                
                # Get priority from Gemini API
                context = f"From: {email_data['From']}\nSubject: {email_data['Subject']}\nBody: {email_data['Body']} . This is the information of an email , from a scale of 1 to 5 rate its priority , where 5 is the highest priority and 1 is the lowest priority.Make sure to answer only in one single digit number"
                priority_response = get_gemini_response(context)
                try:
                    email_data['Priority'] = int(priority_response.strip())
                except ValueError:
                    email_data['Priority'] = 1  # Default to 1 if the response is not a valid number
                
                save_email_to_db(email_data)
                print(f"Saved email from {email_data['From']} to database with priority {email_data['Priority']}.")
            else:
                print("No unread messages found.")
            time.sleep(50)

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()