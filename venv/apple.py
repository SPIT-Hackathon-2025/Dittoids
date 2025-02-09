# import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

def fetch_last_5_rows():
    conn = sqlite3.connect('mail.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT my_email, sender_email, timestamp, subject, body, priority
        FROM emails
        ORDER BY ROWID DESC
        LIMIT 5
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_openai_response(prompt1):
    prompt2="User promInput="+prompt1+"This is the email content. You are a professional task manager , you make sure to guide the user based on the context ."
    rows = fetch_last_5_rows()
    context = "\n\n".join([f"From: {row[1]}\nSubject: {row[3]}\nBody: {row[4]}" for row in rows])
    prompt=prompt2 + "Context="+context
    
    response = client.chat.completions.create(
        model="gpt-4",  # changed from gpt-4o-mini to gpt-4
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content  # Updated to use .message.content instead of ['content']

def main():
    # st.title("Email Chatbot")

    # Fetch the last 5 rows from the database
    rows = fetch_last_5_rows()
    context = "\n\n".join([f"From: {row[1]}\nSubject: {row[3]}\nBody: {row[4]}" for row in rows])

    # Display fetched rows in text form
    # st.subheader("Fetched Rows from Database")
    # st.text(context)

    # Chatbot interface
    # with st.form(key="chat_form"):
    #     user_input = st.text_input("You:")
    #     submit_button = st.form_submit_button(label="Send")

    # if submit_button and user_input:
        # final_context = f"{context}\nUser Input: {user_input}"
        # response = get_openai_response(final_context)
        # st.write(f"Bot: {response}")

if __name__ == "__main__":
    main()