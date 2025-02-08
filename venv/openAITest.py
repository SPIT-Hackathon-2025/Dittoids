import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
import json5
from zendeskUtils import *

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


# Initialize client
client = OpenAI()

prompt=f"""
You are a scheduling manager, responsible for scheduling meetings based on the clients convinience as
as well as employee availability. 
Your goal is to return a json object which represents a meeting between the relevant employees and the client based on the client's instructions
that does not conflict with any employee activities.
The schedules for each employee will be given to you in the form of a json object. You may assume that each meeting is
an hour long and the employee will be free 1 hour after the time mentioned in the object.
For example, if the time 10th October 2025, 9 am is mentioned for an employee, you may schedule a meeting at 10 am for the same employee on the same date.
Only schedule meetings between 9 am and 5 pm.
Do not include any reasoning, formatting or any extra text other than the json object. Strictly stick to the output format.

There are the employee names and their emails
Siddhesh Shrawne : siddhesh.shrawne22@spit.ac.in
Yash Desai : yash.desai22@spit.ac.in
Darsh Tulsiyan : darsh.tulsiyan22@spit.ac.in (Boss)
Omkar Surve : omkar.surve22@spit.ac.in

Here are some example requests/responses:

Sample Request:

Schedule a between me and Yash Desai and Siddhesh Shrawne on 9th Feb 2025 to discuss the
2024 Quarter 4 Financial Statements
Requester: Satyam Vyas
Requester Email: satyam.vyas22@spit.ac.in

{{
    "darsh":["2nd Feb 2025, 9 AM"],
    "siddhesh":["9th February 2025, 11 am"],
    "omkar": [],
    "yash": [3rd March 2025, 1 pm]    
}}

Sample Response:

{{
    "subject":"Meeting Request with Satyam Vyas on 9th Feb 2025, 1 pm",
    "description":"The aim of the meet is to review the 2024 Quarter 4 financial statements",
    "requester_name":"Satyam Vyas",
    "requester_email":"satyam.vyas22@spit.ac.in",
    "assigneeEmail":"yash.desai22@spit.ac.in",
    "collaboratorEmails":["siddhesh.shrawne22@spit.ac.in",],
    "Meeting Required": 1
    "Meeting Time": "9th Feb 2025, 1 pm"
}}




Sample Request:

Schedule a between me and all employees on 18th March 2025 to discuss the new project's feasibility
Requester: Mahesh Panda
Requester Email: mahesh.panda22@spit.ac.in

{{
    "darsh":["9th Feb 2025, 9 AM", "12th Oct 2025, 10 am"],
    "siddhesh":["27th April 2025, 11 am"],
    "omkar": ["18th march 2025, 4 pm"],
    "yash": [3rd March 2025, 1 pm]    
}}


Sample Response:

{{
    "subject":"Metting Request with Mahesh Panda on 18th March 2025, 9 am",
    "description":"The aim of the meet is to discuss the feasibilty of the new project",
    "requester_name":"Mahesh Panda",
    "requester_email":"mahesh.panda22@spit.ac.in",
    "assigneeEmail":"darsh.tulsiyan22@spit.ac.in",
    "collaboratorEmails":[
        "siddhesh.shrawne22@spit.ac.in",
        "yash.desai22@spit.ac.in",
        "omkar.surve22@spit.ac.in"
    ],
    "Meeting Required": 1
    "Meeting Time": "18th March 2025,9 am"
}}






Sample Request:

Inform all employees to use gpt 4o mini instead of gpt due to cost reasons
Requester: Mahesh Panda
Requester Email: mahesh.panda22@spit.ac.in

{{
    "darsh":["9th Feb 2025, 9 AM", "12th Oct 2025, 10 am"],
    "siddhesh":["27th April 2025, 11 am"],
    "omkar": ["18th march 2025, 4 pm"],
    "yash": [3rd March 2025, 1 pm]    
}}


Sample Response:

{{
    "subject": "Friendly reminder for all employees",
    "description":"This is a friendly reminder to all employees to stop using gpt 40 and use gpt 4o mini instead",
    "requester_name":"Mahesh Panda",
    "requester_email":"mahesh.panda22@spit.ac.in",
    "assigneeEmail":"darsh.tulsiyan22@spit.ac.in",
    "collaboratorEmails":[
        "siddhesh.shrawne22@spit.ac.in",
        "yash.desai22@spit.ac.in",
        "omkar.surve22@spit.ac.in"
    ],
    "Meeting Required": 0
}}
"""

def generateTask(text,requester_name,requester_email):
    with open("schedules.json",'r') as file:
        data=json.load(file)
    full_prompt=prompt+text+f"""
        Requester: {requester_name}
        Requester Email: {requester_email}
    """+f"\n\n{data}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": full_prompt},
        ],
    )
    
    resp=response.choices[0].message.content.strip("```").replace("json", "").replace("Response:","").replace("Schedule:","").strip()
    # print(resp)
    print(resp)
    parsed_resp=json5.loads(resp)
    
    for collaborator in parsed_resp['collaboratorEmails']:
        data[collaborator].append(parsed_resp.get('Meeting Time'))
    data[parsed_resp['assigneeEmail']].append(parsed_resp.get('Meeting Time'))
    
    with open('schedules.json','w') as file:
        file.write(json.dumps(data))
    # print(data)
    
    print(parsed_resp)
    return parsed_resp

    
# obj=generateTask("Inform all employees to stop using window and switch to Mac","Siddhesh Shrawne","siddheshshrawne10@gmail.com")
# create_zendesk_ticket(obj['subject'],obj['description'],obj['requester_name'],obj['requester_email'],obj['assigneeEmail'],obj['collaboratorEmails'],obj.get('Meeting Time'))
