import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
import json5

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


# Initialize client
client = OpenAI()

prompt=f"""
You are a scheduling manager, responsible for scheduling meetings based on the clients convinience as
as well as employee availability. 
Your goal is to return a json object which represents a meeting between the relevant employees and the client based on the client's instructions
that does not conflict with any employee activities.

There are the employee names and their emails
Siddhesh Shrawne : siddhesh.shrawne22@spit.ac.in
Yash Desai : yash.desai22@spit.ac.in
Darsh Tulsiyan : darsh.tulsiyan22@spit.ac.in (Boss)
Omkar Surve : omkar.surve22@spit.ac.in

Here are some example requests/responses:

Request: Schedule a between me and Yash Desai and Siddhesh Shrawne on 9th Feb 2025 to discuss the
2024 Quarter 4 Financial Statements
Requester: Satyam Vyas
Requester Email: satyam.vyas22@spit.ac.in

Response:{{
    "subject":"Meeting Request with Satyam Vyas on 9th Feb 2025",
    "description":"The aim of the meet is to review the 2024 Quarter 4 financial statements",
    "requester_name":"Satyam Vyas",
    "requester_email":"satyam.vyas22@spit.ac.in",
    "assigneeEmail":"yash.desai22@spit.ac.in",
    "collaboratorEmails":["siddhesh.shrawne22@spit.ac.in",]
}}





Request: Schedule a between me and all employees on 18th March 2025 to discuss the new project's feasibility
Requester: Mahesh Panda
Requester Email: mahesh.panda22@spit.ac.in

Response:{{
    "subject":"Metting Request with Mahesh Panda on 18th March 2025",
    "description":"The aim of the meet is to discuss the feasibilty of the new project",
    "requester_name":"Mahesh Panda",
    "requester_email":"mahesh.panda22@spit.ac.in",
    "assigneeEmail":"darsh.tulsiyan22@spit.ac.in",
    "collaboratorEmails":[
        "siddhesh.shrawne22@spit.ac.in",
        "yash.desai22@spit.ac.in",
        "omkar.surve22@spit.ac.in"
    ]
}}
"""

def generateTask(text,requester_name,requester_email):
    full_prompt=prompt+text+f"""
        Requester: {requester_name}
        Requester Email: {requester_email}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": full_prompt},
        ],
    )
    
    resp=response.choices[0].message.content.strip("```").replace("json", "").strip().replace("Response:","").strip()
    print(resp)
    parsed_resp=json5.loads(resp)
    
    print(parsed_resp)

    
generateTask("Arrange a meeting between me and all employees on 8th Feb 2025 to discuss the quality of the food in SP Jain Mess Hall","Siddhesh Shrawne","siddheshshrawne10@gmail.com")

