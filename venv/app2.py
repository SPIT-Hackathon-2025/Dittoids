# # # from agents import main_agent
# # # from swarm import Swarm
# # # import streamlit as st
# # # import os
# # # from dotenv import load_dotenv

# # # load_dotenv()

# # # api_key = os.getenv("OPENAI_API_KEY")
# # # if not api_key:
# # #     st.error("Missing OpenAI API Key. Ensure it's set in a .env file or system environment.")
# # #     raise ValueError("Missing OpenAI API Key. Set it in a .env file or system environment.")
# # # print(api_key)

# # # if __name__ == '__main__':
# # #     swarm_client = Swarm()
# # #     agent = main_agent

# # #     st.title('Calendar Agent')

# # #     if 'messages' not in st.session_state:
# # #         st.session_state.messages = []
    
# # #     for message in st.session_state.messages:
# # #         with st.chat_message(message['role']):
# # #             st.markdown(message['content'])

# # #     if prompt := st.chat_input('Enter ypur prompt here'):
# # #         st.session_state.messages.append({'role': 'user', 'content': prompt})

# # #         with st.chat_message('user', avatar='🧑🏼‍💻'):
# # #             st.markdown(prompt)

# # #         with st.chat_message('ai', avatar='🤖'):
# # #             response = swarm_client.run(
# # #                 agent=agent,
# # #                 debug=False,
# # #                 messages = st.session_state.messages
# # #             )
# # #             st.markdown(response.messages[-1]['content'])
# # #         st.session_state.messages.append({'role': 'assistant', 'content': response.messages[-1]['content']})

# # from flask import Flask, render_template, request, jsonify
# # import os
# # from dotenv import load_dotenv
# # from swarm import Swarm
# # from agents import main_agent

# # # Load environment variables
# # load_dotenv()
# # api_key = os.getenv("OPENAI_API_KEY")

# # if not api_key:
# #     raise ValueError("Missing OpenAI API Key. Set it in a .env file or system environment.")

# # # Initialize Flask app
# # app = Flask(__name__)

# # # Swarm client
# # swarm_client = Swarm()

# # # Store conversation history
# # messages = []

# # @app.route("/")
# # def index():
# #     return render_template("index.html", messages=messages)

# # @app.route("/send", methods=["POST"])
# # def send_message():
# #     print("Check")
# #     user_message = request.json.get("message")
# #     print(user_message)
# #     if not user_message:
# #         return jsonify({"error": "No message provided"}), 400

# #     # Store user message
# #     messages.append({"role": "user", "content": user_message})

# #     # Get AI response
# #     response = swarm_client.run(agent=main_agent, debug=False, messages=messages)
# #     ai_message = response.messages[-1]['content']
# #     print(ai_message)
# #     # Store AI response
# #     messages.append({"role": "assistant", "content": ai_message})

# #     return jsonify({"response": ai_message})

# # if __name__ == "__main__":
# #     app.run(debug=True)

# from flask import Flask, render_template, request, jsonify
# from agents import main_agent
# from swarm import Swarm
# from dotenv import load_dotenv
# import os

# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")

# if not api_key:
#     raise ValueError("Missing OpenAI API Key. Set it in a .env file or system environment.")


# app = Flask(__name__)
# swarm_client = Swarm()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json['message']
#     response = swarm_client.run(agent=main_agent, debug=False, messages=[{'role': 'user', 'content': user_input}])
#     bot_response = response.messages[-1]['content']
#     return jsonify({'message': bot_response})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify
from agents import main_agent
from swarm import Swarm
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Ensure API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OpenAI API Key. Set it in a .env file or system environment.")

swarm_client = Swarm()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Process the chatbot response
    response = swarm_client.run(
        agent=main_agent,
        debug=False,
        messages=[{"role": "user", "content": user_message}]
    )

    bot_reply = response.messages[-1]["content"]

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
