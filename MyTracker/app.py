from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_db import User, ToDo
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = '69691234'



# Set up database + session
engine = create_engine("sqlite:///todo.db")
Session = sessionmaker(bind=engine)
db_session = Session()



@app.route('/')
def index():
    return render_template('index.html')

# Route for login page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db_session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login Successful", "info")
            return redirect(url_for("todo_list"))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html')

# Route for signup page
@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template('signup.html')

@app.route('/todo_list')
def todo_list():
    if "user_id" not in session:
        flash("Please login to view that page", "warning")
        return redirect(url_for("login"))
    # Retrieve the user's tasks from the database
    user_id = session["user_id"]
    user = db_session.query(User).get(user_id)
    return render_template("todo_list.html", user_id=session["user_id"], username=session["username"])

@app.route('/logout')
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)