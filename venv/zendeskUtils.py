import requests
import json
from dotenv import load_dotenv
import os
from pymongo import *

load_dotenv()

TOKEN = os.getenv("ZENDESK_API_KEY")
DOMAIN = os.getenv("DOMAIN")
EMAIL = os.getenv("EMAIL")


client = MongoClient(os.getenv("MONGO_CONN_STR"))
db = client['Dittoids']  # Create or access the database



def create_zendesk_ticket(
    subject, description, requester_name, requester_email, assigneeEmail
):
    assigneeID=get_agent_id_by_email(assigneeEmail)
    url = f"https://{DOMAIN}.zendesk.com/api/v2/tickets.json"
    headers = {"Content-Type": "application/json"}
    # data = {
    #     "request": {
    #         "subject": subject,
    #         "comment": {"body": "Hey, this ticket was assigned to you for resolution. Please follow up on it as soon as possible.\n\nCheers,\nYour Favourite Task Management Agent,\nPavlov\n\n"+description},
    #         "requester": {
    #             "name": requester_name,
    #             "email": requester_email,
    #         },
    #         "assignee_id": assigneeID
    #         # to assign it to someone in particular
    #     }
    # }
    # if(assigneeID):
    data={
        "ticket": {
            "subject": subject,
            "comment": {"body": "Hey, this ticket was assigned to you for resolution. Please follow up on it as soon as possible.\n\nCheers,\nYour Favourite Task Management Agent,\nPavlov\n\n"+description},
            "requester": {
                "name": requester_name,
                "email": requester_email,
            },
            "assignee_id": assigneeID
        }
    }
    # else:
    #     data={
    #         "ticket": {
    #             "subject": subject,
    #             "comment": {"body": "Hey, this ticket was assigned to you for resolution. Please follow up on it as soon as possible.\n\nCheers,\nYour Favourite Task Management Agent,\nPavlov\n\n"+description},
    #             "requester": {
    #                 "name": requester_name,
    #                 "email": requester_email,
    #             },
    #         }
    #     }

    response = requests.post(
        url,
        headers=headers,
        auth=(f"{EMAIL}/token", TOKEN),
        json=data,
    )
    task={
        "ID":response.json()['ticket']['id'],
        "Status":"new",        
        "Subject":subject
    }
    collection = db[assigneeEmail]
    collection.insert_one(task)
    
    print(response.json())

    return response



def get_ticket_status(ticket_id):
    url = f"https://{DOMAIN}.zendesk.com/api/v2/tickets/{ticket_id}.json"
    response = requests.get(
        url, auth=(f"{EMAIL}/token", TOKEN)
    )
    print(response.json()['ticket']['status'])

    return response.json()['ticket']['status']


def refreshAll(email):
    collection = db[email]
    all_documents = list(collection.find()) 
    collection.delete_many({})
    
    for document in all_documents:
        document['Status']=get_ticket_status(document['ID'])
    
    collection.insert_many(all_documents)
    


def get_agent_id_by_email(email):
    url = f"https://{DOMAIN}.zendesk.com/api/v2/users/search.json?query={email}"
    response = requests.get(url, auth=(f"{EMAIL}/token", TOKEN))
    # print(response.json())
    if response.status_code == 200:
        users = response.json()["users"]
        if users:
            agent_id = users[0]["id"]
            return agent_id
        else:
            print("No user found with the email:", email)
            return None
    else:
        print(f"Error fetching user details: {response.status_code}")
        return None


create_zendesk_ticket("Subject","apple","Siddhesh","siddhesh.shrawne22@spit.ac.in","siddhesh.shrawne22@spit.ac.in")
# print(get_agent_id_by_email("siddhesh.shrawne22@spit.ac.in"))