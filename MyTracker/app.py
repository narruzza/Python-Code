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

# @app.route('/todo_list')
# def todo_list():
#     if "user_id" not in session:
#         flash("Please login to view that page", "warning")
#         return redirect(url_for("login"))
#     return render_template("todo_list.html", user_id=session["user_id"], username=session["username"])


# # Google OAuth login route
# @app.route("/google_login")
# def google_login():
#     if not google.authorized:
#         return redirect(url_for("google.login"))

#     resp = google.get("/plus/v1/people/me")
#     assert resp.ok, resp.text
#     email = resp.json()["emails"][0]["value"]

#     # Check if user already exists
#     user = db_session.query(User).filter_by(username=email).first()
#     if not user:
#         # Create a new user if it doesn't exist
#         new_user = User(username=email, password=generate_password_hash("default_password"))
#         db_session.add(new_user)
#         db_session.commit()

#     # Log in the user
#     session["user_id"] = user.id if user else new_user.id
#     session["username"] = email
#     flash("Google login successful!", "info")
#     return redirect(url_for("todo_list"))


# Run the app
if __name__ == '__main__':
    app.run(debug=True)