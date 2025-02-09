from flask import Flask, request, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv
import docx

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_file(file_path):
    """Extract text from a TXT or DOCX file."""
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""

@app.route("/", methods=["GET", "POST"])
def index():
    minutes = None  # To store generated minutes
    transcript = None  # To store input transcript

    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file uploaded.")

        file = request.files["file"]

        if file.filename == "":
            return render_template("index.html", error="No file selected.")

        if file and file.filename.endswith((".txt", ".docx")):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            transcript = extract_text_from_file(file_path)

            if not transcript.strip():
                return render_template("index.html", error="Uploaded file is empty.")

            # Generate meeting minutes using OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Generate concise minutes of the meeting from this transcript."},
                    {"role": "user", "content": transcript}
                ]
            )
            minutes = response.choices[0].message.content

    return render_template("index.html", transcript=transcript, minutes=minutes)

if __name__ == "__main__":
    app.run(debug=True)
