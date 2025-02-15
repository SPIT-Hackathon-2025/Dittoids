# import os
# import sqlite3
# import json
# from datetime import datetime, timedelta
# from openai import OpenAI
# import asyncio
# from notionagent import NotionManager
# from dotenv import load_dotenv

# load_dotenv()

# # Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Initialize NotionManager
# manager = NotionManager()

# async def create_database_if_not_exists(database_id):
#     """Create the database if it doesn't exist and return the database ID."""
#     parent_page_id = os.getenv('NOTION_PAGE_ID')
#     if not database_id:
#         database_id = await manager.create_database(parent_page_id)
#     return database_id

# async def create_task_in_notion(database_id, task_data):
#     """Create a task in Notion and return the task ID."""
#     database_id = await create_database_if_not_exists(database_id)
#     manager.database_id = database_id
#     task_id = await manager.create_task(task_data)
#     return task_id

# def get_bottommost_email():
#     """Retrieve the bottommost email from mail.db."""
#     conn = sqlite3.connect('mail.db')
#     cursor = conn.cursor()
    
#     try:
#         # Print the schema of the emails table for debugging
#         cursor.execute("PRAGMA table_info(emails)")
#         columns = cursor.fetchall()
#         print("Emails table schema:")
#         for column in columns:
#             print(column)
        
#         # Fetch the most recent email
#         cursor.execute("SELECT subject, body FROM emails ORDER BY ROWID DESC LIMIT 1")
#         email = cursor.fetchone()
#         return email
#     except sqlite3.Error as e:
#         print(f"Database error: {e}")
#         return None
#     finally:
#         conn.close()

# def parse_email_with_llm(subject, content):
#     """Parse the email content using OpenAI's GPT model to extract task details."""
#     prompt_template = f"""
#     You are an AI that extracts potential work-related tasks from emails.
#     Email Subject: {subject}
#     Email Content: {content}
    
#     If the email describes a work-related task, return a JSON object with:
#     {{
#       "title": "A short name",
#       "description": "A brief description",
#       "status": "Not Started|In Progress|Completed|On Hold",
#       "priority": "High|Medium|Low",
#       "due_date": "A realistic date *only* in the date format yyyy-MM-dd or 'None'",
#       "tags": ["tag1", "tag2"],
#       "progress": 0
#     }}
#     If the email does not describe a work-related task, return an empty object. Return only the JSON no text following or preceding it.
#     """
    
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4-turbo-preview",  # or another appropriate model
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant that extracts task information from emails."},
#                 {"role": "user", "content": prompt_template}
#             ],
#             temperature=0.5
#         )
        
#         # Extract the response content
#         content = response.choices[0].message.content.strip()
#         print(f"Raw LLM response: {content}")  # Debug print
        
#         # Parse the JSON response
#         try:
#             return json.loads(content)
#         except json.JSONDecodeError:
#             print("Failed to parse LLM response as JSON")
#             return {}
            
#     except Exception as e:
#         print(f"Error in LLM processing: {e}")
#         return {}

# async def main():
#     try:
#         # Get the bottommost email
#         email = get_bottommost_email()
#         if not email:
#             print("No emails found in mail.db.")
#             return
        
#         subject, content = email
#         print(f"Processing email with subject: {subject}")

#         # Parse the email content with LLM
#         task_data = parse_email_with_llm(subject, content)

#         if not task_data:
#             print("No task found in the email content.")
#             return

#         # Create task in Notion
#         database_id = os.getenv('NOTION_DATABASE_ID')
#         task_id = await create_task_in_notion(database_id, task_data)
#         if task_id:
#             print(f"Task created successfully with ID: {task_id}")
#         else:
#             print("Failed to create task in Notion.")

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     asyncio.run(main())
import os
import sqlite3
import json
from datetime import datetime, timedelta
from openai import OpenAI
import asyncio
from notionagent import NotionManager
from dotenv import load_dotenv
import time
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize NotionManager
manager = NotionManager()

async def create_database_if_not_exists(database_id):
    """Create the database if it doesn't exist and return the database ID."""
    parent_page_id = os.getenv('NOTION_PAGE_ID')
    if not database_id:
        database_id = await manager.create_database(parent_page_id)
    return database_id

async def create_task_in_notion(database_id, task_data):
    """Create a task in Notion and return the task ID."""
    database_id = await create_database_if_not_exists(database_id)
    manager.database_id = database_id
    task_id = await manager.create_task(task_data)
    return task_id

def get_bottommost_email():
    """Retrieve the bottommost email from mail.db."""
    conn = sqlite3.connect('mail.db')
    cursor = conn.cursor()
    
    try:
        # Print the schema of the emails table for debugging
        cursor.execute("PRAGMA table_info(emails)")
        columns = cursor.fetchall()
        print("Emails table schema:")
        for column in columns:
            print(column)
        
        # Fetch the most recent email
        cursor.execute("SELECT subject, body FROM emails ORDER BY ROWID DESC LIMIT 1")
        email = cursor.fetchone()
        return email
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()
def get_email_count():
    """Get the count of rows in the emails table."""
    conn = sqlite3.connect('mail.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM emails")
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0
    finally:
        conn.close()

def call_llm_for_field(prompt):
    """Call the LLM to extract a specific field from the email content."""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # or another appropriate model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts task information from emails."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        # Extract the response content
        content = response.choices[0].message.content.strip()
        print(f"Raw LLM response for field: {content}")  # Debug print
        return content
    except Exception as e:
        print(f"Error in LLM processing: {e}")
        return None

def parse_email_with_llm(subject, content):
    """Parse the email content using OpenAI's GPT model to extract task details."""
    task_data = {}

    # Extract title
    title_prompt = f"Extract the title from the following email content:\n\nEmail Subject: {subject}\nEmail Content: {content}\n\nTitle:"
    task_data["title"] = call_llm_for_field(title_prompt)

    # Extract description
    description_prompt = f"Extract the description from the following email content:\n\nEmail Subject: {subject}\nEmail Content: {content}\n\nDescription:"
    task_data["description"] = call_llm_for_field(description_prompt)

    # Extract status
    status_prompt = f"Extract the status from the following email content:\n\nEmail Subject: {subject}\nEmail Content: {content}\n\nStatus (Not Started|In Progress|Completed|On Hold):"
    task_data["status"] = call_llm_for_field(status_prompt)

    # Extract priority
    priority_prompt = f"Extract the priority from the following email content:\n\nEmail Subject: {subject}\nEmail Content: {content}\n\nPriority (High|Medium|Low):"
    task_data["priority"] = call_llm_for_field(priority_prompt)

    # Extract due date
    due_date_prompt = f"Extract the due date from the following email content:\n\nEmail Subject: {subject}\nEmail Content: {content}\n\nDue Date (yyyy-MM-dd or 'None'):"
    task_data["due_date"] = call_llm_for_field(due_date_prompt)

    # Extract tags
    tags_prompt = f"Extract the tags from the following email content:\n\nEmail Subject: {subject}\nEmail Content: {content}\n\nTags (comma-separated):"
    tags = call_llm_for_field(tags_prompt)
    task_data["tags"] = [tag.strip() for tag in tags.split(",")]

    # Set default progress
    task_data["progress"] = 0

    return task_data

async def main():
    previous_count = get_email_count()

    while True:
        try:
            current_count = get_email_count()
            if current_count > previous_count:
                previous_count = current_count

                # Get the bottommost email
                email = get_bottommost_email()
                if not email:
                    print("No emails found in mail.db.")
                    continue
                
                subject, content = email
                print(f"Processing email with subject: {subject}")

                # Parse the email content with LLM
                task_data = parse_email_with_llm(subject, content)

                if not task_data:
                    print("No task found in the email content.")
                    continue

                # Create task in Notion
                database_id = os.getenv('NOTION_DATABASE_ID')
                task_id = await create_task_in_notion(database_id, task_data)
                if task_id:
                    print(f"Task created successfully with ID: {task_id}")
                else:
                    print("Failed to create task in Notion.")
            else:
                print("No new emails to process.")
            
            # Sleep for a while before checking again
            time.sleep(10)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())