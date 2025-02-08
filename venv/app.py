from flask import jsonify,Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from openAITest import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB setup
client = MongoClient(os.getenv("MONGO_CONN_STR"))
db = client.auth_db
collection = db.users

@app.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template('sign_up.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if not email or not password or not confirm_password:
        flash('All fields are required!', 'danger')
        return redirect(url_for('sign_up'))
    
    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('sign_up'))
    
    existing_user = collection.find_one({'email': email})
    if existing_user:
        flash('Email already registered', 'danger')
        return redirect(url_for('sign_up'))
    
    hashed_password = generate_password_hash(password)
    collection.insert_one({'email': email, 'password': hashed_password})
    flash('Account created successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        flash('All fields are required!', 'danger')
        return redirect(url_for('login'))
    
    user = collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        session['email'] = user['email']
        session['username']=request.form.get('name')
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    
    flash('Invalid credentials', 'danger')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/chatbot',methods=['GET',"POST"])
def chatbot():
    user_message = request.json.get('message')
    print(session['username'])
    print(session['email'])
    obj=generateTask(user_message,session['username'],session['email'])
    create_zendesk_ticket(obj['subject'],obj['description'],obj['requester_name'],obj['requester_email'],obj['assigneeEmail'],obj['collaboratorEmails'],obj.get('Meeting Time'))
    return jsonify({"response": "Your ticket has been successfully created!"})

if __name__ == '__main__':
    app.run(debug=True)
