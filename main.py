from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# Enable CORS
CORS(app)

# -----------------------------
# MySQL / Database Config
# -----------------------------
# Use environment variables for local + cloud deploy
DB_USER = os.environ.get("MYSQL_USER", "root")        # default local
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")    # default local
DB_HOST = os.environ.get("MYSQL_HOST", "localhost")   # default local
DB_PORT = os.environ.get("MYSQL_PORT", 3306)          # default local
DB_NAME = os.environ.get("MYSQL_DATABASE", "portfolio")  # default local

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -----------------------------
# Email Config (Gmail)
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME", "")  # Gmail
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD", "")  # App Password
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME", "")  # Sender

mail = Mail(app)

# -----------------------------
# Database Model
# -----------------------------
class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON sent"}), 400

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    # Save in DB
    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    # Send email
    msg = Message(
        subject=f"📩 New Contact Form Submission from {name}",
        recipients=[os.environ.get("MAIL_USERNAME", "yourgmail@gmail.com")],
        body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    )
    mail.send(msg)

    return jsonify({"status": "success", "message": "Saved in DB ✅ & Email Sent 📧"})

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
