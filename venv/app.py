from flask import jsonify,Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from openAITest import *
import assemblyai as aai
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB setup
client = MongoClient(os.getenv("MONGO_CONN_STR"))
db = client['auth_db']
collection = db.users

@app.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template('sign_up.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    notionUsername=request.form.get('notionUsername')
    
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
    collection.insert_one({'email': email, 'password': hashed_password,'notionUsername':notionUsername})
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
    tdb=client['Dittoids']
    coll=tdb[session['email']]
    
    arr=coll.find()
    meetings=[]
    print(arr)
    for a in arr:
        print(a)
        meetings.append(a['Subject'])
    print(meetings)
    return render_template('dashboard.html',meetings=meetings)

@app.route('/chatbot',methods=['GET',"POST"])
def chatbot():
    user_message = request.json.get('message')
    print(session['username'])
    print(session['email'])
    obj=generateTask(user_message,session['username'],session['email'])
    create_zendesk_ticket(obj['subject'],obj['description'],obj['requester_name'],obj['requester_email'],obj['assigneeEmail'],obj['collaboratorEmails'],obj.get('Meeting Time'))
    
    if('Meeting Time' in obj):
        resp="Your ticket has been successfully created!\nAfter reviewing everyone's schedule, I have scheduled the meeting for " +obj['Meeting Time'] +"\nI have also informed all relevant parties of the same via email"
    else:
        resp="Your ticket has been successfully created!\nThe message has been sent to all relevant parties via email."
    
    return jsonify({"response":resp})




aai.settings.api_key = os.getenv("ASSEMBLY_API_KEY")

def transcribe_audio(audio_data):
    audio_io = io.BytesIO(audio_data)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_io)
    
    if transcript.status == aai.TranscriptStatus.error:
        return f"Transcription failed: {transcript.error}"
    return transcript.text



@app.route('/record', methods=['POST'])
def record_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400
    
    audio_file = request.files['audio']
    audio_data = audio_file.read()
    
    transcript_text = transcribe_audio(audio_data)
    return jsonify({'transcription': transcript_text})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)