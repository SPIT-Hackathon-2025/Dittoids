import base64
import re
from google_apis import create_service

CLIENT_SECRET = "client_secret.json"

# Create Gmail service
gmail_service = create_service(CLIENT_SECRET, "gmail", "v1", ["https://www.googleapis.com/auth/gmail.readonly"])

def get_latest_email():
    messages = gmail_service.users().messages().list(userId="me", maxResults=1, q="in:inbox").execute().get("messages", [])
    if not messages:
        return None

    message = gmail_service.users().messages().get(userId="me", id=messages[0]["id"]).execute()
    
    headers = {header["name"]: header["value"] for header in message["payload"]["headers"]}
    body = base64.urlsafe_b64decode(message["payload"]["body"]["data"]).decode("utf-8") if "data" in message["payload"]["body"] else "No body text"

    return {
        "Date": headers.get("Date", ""),
        "From": headers.get("From", ""),
        "Subject": headers.get("Subject", ""),
        "Body": body
    }

def extract_event_from_email(email_text):
    # Example: Detect an event with regex (Improve NLP model for better accuracy)
    event_match = re.search(r"Event: (.+)", email_text)
    date_match = re.search(r"Date: (\d{4}-\d{2}-\d{2})", email_text)
    time_match = re.search(r"Time: (\d{2}:\d{2})", email_text)
    action_match = re.search(r"Action: (add|update|delete)", email_text)

    if event_match and date_match and time_match and action_match:
        return {
            "summary": event_match.group(1),
            "start": {"dateTime": f"{date_match.group(1)}T{time_match.group(1)}:00", "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": f"{date_match.group(1)}T{str(int(time_match.group(1).split(':')[0]) + 1)}:00:00", "timeZone": "Asia/Kolkata"},
            "action": action_match.group(1)
        }
    return None
