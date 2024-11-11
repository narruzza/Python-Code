# app.py
from flask import Flask, render_template, request, flash, session, jsonify
from wekzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User

app = Flask(__name__)
app.secret_key = '69691234'

# Set up database + session
engine = create_engine("sqlite:///users.db")
Session = sessionmaker(build=engine)
db_session = Session()

# Define user details
username = "admin"
password = "admin123"

# Hash the password
hashed_password = generate_password_hash(password)

# Create a new user instance
new_user = User(username=username, password=hashed_password)

# Add the new user to the database
db_session.add(new_user)
db_session.commit()
print("User added to the database")

# Route for singup page
@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template('static', 'signup.html')

# Route for login page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Query the database for the user
        user = db_session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash("You have successfully logged in", "success")
            session['user_id'] = user.id
        else:
            flash("Invalid username or password", "danger")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
