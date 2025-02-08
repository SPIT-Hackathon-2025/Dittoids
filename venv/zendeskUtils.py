import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("ZENDESK_API_KEY")
DOMAIN = os.getenv("DOMAIN")
EMAIL = os.getenv("EMAIL")




def create_zendesk_ticket(
    subject, description, requester_name, requester_email, assigneeID
):

    url = f"https://{DOMAIN}.zendesk.com/api/v2/requests.json"
    headers = {"Content-Type": "application/json"}
    data = {
        "request": {
            "subject": subject,
            "comment": {"body": "Hey, this ticket was assigned to you for resolution. Please follow up on it as soon as possible.\n\nCheers,\nYour Favourite Task Management Agent,\nPavlov\n\n"+description},
            "requester": {
                "name": requester_name,
                "email": requester_email,
            },
            # "assignee_id": assigneeID
            # to assign it to someone in particular
        }
    }

    response = requests.post(
        url,
        headers=headers,
        auth=(f"{EMAIL}/token", TOKEN),
        json=data,
    )
    
    print(response.json())

    return response



def get_ticket_status(ticket_id):
    url = f"https://{DOMAIN}.zendesk.com/api/v2/tickets/{ticket_id}.json"
    response = requests.get(
        url, auth=(f"{EMAIL}/token", TOKEN)
    )
    print(response.json())

    return response

create_zendesk_ticket("Subject","Test","Siddhesh",EMAIL,0)
