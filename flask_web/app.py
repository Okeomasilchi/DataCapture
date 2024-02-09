from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin
from models import storage
from dotenv import load_dotenv
import requests as rq
import os

load_dotenv("./.env")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Define a User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        return User(user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_data = storage.exist(email, data=True)
        if user_data:
            user = User(user_data["id"])
            login_user(user)
            flash("Login successful!", "success")
            session["user_id"] = user_data["id"]  # Store user_id in session
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout", methods=["GET"], strict_slashes=False)
def logout():
    logout_user()
    session.pop("user_id", None)  # Remove user_id from session
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    if current_user.is_authenticated:
        user_id = session.get("user_id")  # Retrieve user_id from session
        r = rq.get(f"http://0.0.0.0:5000/api/v1/users/{user_id}")
        user = r.json()
        flash(f"Welcome back {user['first_name']}!", "success")
        
        if user_id:
            
            if r.status_code == 200:
                
                return render_template("home.html", user=user)
        else:
            flash("User ID not found in session.", "danger")
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT" + "1", 5001))
    app.run(host=host, port=port, debug=True, threaded=True)
