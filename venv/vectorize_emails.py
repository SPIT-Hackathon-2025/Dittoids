import os
import base64
import openai
import pymongo
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
MONGO_URI = os.getenv("MONGO_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def get_email_content(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        headers = message['payload']['headers']
        subject = ''
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
                break
        if 'parts' in message['payload']:
            parts = message['payload']['parts']
            data = parts[0]['body'].get('data', '')
        else:
            data = message['payload']['body'].get('data', '')
        if data:
            text = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            text = "No content"
        return subject, text
    except Exception as error:
        print(f"An error occurred: {error}")
        return None, None

def vectorize_text(text):
    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return response['data'][0]['embedding']

def main():
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId="me", maxResults=10, q="in:inbox").execute().get("messages", [])
        if not results:
            print("No messages found.")
            return

        client = pymongo.MongoClient(MONGO_URI)
        db = client.Dittoids
        collection = db.vectordb

        for message in results:
            subject, content = get_email_content(service, "me", message["id"])
            if subject and content:
                vector = vectorize_text(content)
                collection.insert_one({
                    "subject": subject,
                    "content": content,
                    "vector": vector
                })
                print(f"Stored email with subject: {subject}")

        print("All emails have been processed and stored in MongoDB.")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()