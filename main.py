import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# -----------------------------
# Database Config
# -----------------------------
db_user = os.environ.get("MYSQL_USER", "root")
db_pass = os.environ.get("MYSQL_PASSWORD", "")
db_host = os.environ.get("MYSQL_HOST", "localhost")
db_port = os.environ.get("MYSQL_PORT", "3306")  # Keep as string
db_name = os.environ.get("MYSQL_DATABASE", "portfolio")

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -----------------------------
# Mail Config
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME", "")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD", "")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME", "")

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
    if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
        try:
            msg = Message(
                subject=f"📩 New Contact Form Submission from {name}",
                recipients=[app.config['MAIL_DEFAULT_SENDER']],
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
        except Exception as e:
            print("Email sending failed:", e)

    return jsonify({"status": "success", "message": "Saved in DB ✅ & Email Sent 📧"})

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
