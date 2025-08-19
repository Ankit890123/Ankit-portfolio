from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")

# ✅ enable CORS for frontend <-> backend
CORS(app)

# ✅ MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:username@localhost/portfolio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ✅ Database model
class Contact(db.Model):
    __tablename__ = "contact"   # table name fix kar diya
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

# ✅ Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Contact POST route
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

    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"status": "success", "message": "Saved in DB ✅"})

if __name__ == "__main__":
    app.run(debug=True)
