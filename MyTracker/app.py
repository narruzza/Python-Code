from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_db import User, ToDo

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
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the username already exists
        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            flash("Username already taken. Please choose another.",
            "danger")
            return redirect(url_for('signup'))
        
        # Hash the password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/todo_list')
def todo_list():
    if "user_id" not in session:
        flash("Please login to view that page", "warning")
        return redirect(url_for("login"))
    # Retrieve the user's tasks from the database
    user_id = session["user_id"]
    user = db_session.query(User).get(user_id)
    tasks = db_session.query(ToDo).filter_by(user_id=user_id).all()
    return render_template("todo_list.html", user_id=session["user_id"], username=session["username"], tasks=tasks)

@app.route('/logout')
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


@app.route('/add_todo', methods=["POST"])
def add_todo():
    # Ensure the user is logged in
    if "user_id" not in session:
        flash("Please log in to add a to-do.", "warning")
        return redirect(url_for('login'))
    
    # Retrieve task data from the form
    task_description = request.form.get("task-name")
    user_id = session["user_id"]

    # Create a new Task object and save it to the database
    new_task = ToDo(task=task_description, user_id=user_id)
    db_session.add(new_task)
    db_session.commit()
    flash("To-Do added successfully!", "success")
    return redirect(url_for('todo_list'))

@app.route('/delete_todo/<int:todo_id>', methods=["POST"])
def delete_todo(todo_id):
    # Ensure the user is logged in
    if "user_id" not in session:
        flash("Please log in to delete a to-do.", "warning")
        return redirect(url_for('login'))
    
    # Query the database for the task
    task = db_session.query(ToDo).get(todo_id)

    # Ensure the task exists and belongs to the logged-in user
    if task and task.user_id == session["user_id"]:
        db_session.delete(task)
        db_session.commit()
        flash("To-Do deleted successfully!", "success")
    else:
        flash("To-Do not found or access denied.", "danger")
    return redirect(url_for('todo_list'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)