# Imports
from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
)
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from . import appDB
from flask_login import login_user, login_required, logout_user, current_user

# Create a blueprint for a collection of routes for the websites authentication components
auth = Blueprint("auth", __name__)


# login page is set to the website route /login
@auth.route("/login", methods=["GET", "POST"])
def login():
    # Check if the request is a post - A submitted form
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")

        # Check if a user exist with the username entered
        user = User.query.filter_by(username=username).first()
        if user:
            # Check the password entered and the password stored by checking the hash
            if check_password_hash(user.password, password):
                # If the details are correct notify the user and log them in
                flash("Log in success", category="Success")
                login_user(user, remember=True)
                current_app.logger.info("User successfully logged in")
                # Redirect the user to the view assets page
                return redirect(url_for("views.viewAssets"))
            else:
                current_app.logger.warning("User not logged in - Incorrect password")
                # If the details are incorrect notify the user of an incorrect password
                flash("Incorrect password", category="Information")
            # endif
        else:
            # If the user does not exist then notify the user and do not log in
            current_app.logger.warning("User not logged in - Username does not exist")
            flash("User does not exist with that username", category="Information")
        # endif

    # Render the login template with no parameters
    return render_template("login.html")


# logout page is set to the website route /logout
@auth.route("/logout", methods=["GET", "POST"])
# Require the user to be logged in to access
@login_required
def logout():
    # Check if the request is a post - A submitted form
    if request.method == "POST":
        # Check the logout choice selected
        if request.form.get("logoutChoice") == "Yes":
            # If the user has chosen to log out then log out the current user and redirect to the home page
            logout_user()
            current_app.logger.info("User logged out - sent to home page")
            return redirect(url_for("views.homePage"))
        else:
            # If the user would like to log out then redirect the user to their view assets page
            current_app.logger.info("User not logged out - returned to view asset page")
            return redirect(url_for("views.viewAssets"))
        # endif
    # endif

    # Render the login template and send one parameter
    return render_template("logout.html", username=current_user.username)


# signup page is set to the website route /signup
@auth.route("/signup", methods=["GET", "POST"])
def signUp():
    # Check if the request is a post - A submitted form
    if request.method == "POST":
        formData = request.form
        username = formData.get("username").lower()
        password = formData.get("password")
        confPassword = formData.get("confPassword")

        user = User.query.filter_by(username=username).first()
        # Validation for user signing up
        if user:
            # If the user with the username already exists then notify the user
            current_app.logger.warning("Signup failed - user already exists")
            flash(
                "User already exists with this username, please choose another username",
                category="Information",
            )
        elif len(username) < 4:
            # If the username is too short then notify the user
            current_app.logger.warning("Signup failed - username too short")
            flash("Username must be larger than 4 characters", category="Information")
        elif password != confPassword:
            # If the passwords do not match then notify the user
            current_app.logger.warning("Signup failed - password do not match")
            flash("Input password do not match", category="Information")
        elif len(password) < 7:
            # If the password is too short then notify the user
            current_app.logger.warning("Signup failed - password too short")
            flash("Password must be larger than 7 characters", category="Information")
        elif not any(char in ["!", "@", "#", "$", "£"] for char in password):
            # If the password does not contain symbols then notify the user
            current_app.logger.warning(
                "Signup failed - password does not include symbols"
            )
            flash(
                "The password must include at least one of the following symbols: !, @, #, $, £",
                category="Information",
            )
        elif not any(char.isdigit() for char in password):
            # If the password does not include a digit then notify the user
            current_app.logger.warning(
                "Signup failed - password does not include a digit"
            )
            flash(
                "The password must include at least one digit", category="Information"
            )
        elif not any(char.isupper() for char in password):
            # If the password does not include an uppercase letter then notify the user
            current_app.logger.warning(
                "Signup failed - password does not include an uppercase character"
            )
            flash(
                "The password must include at least one uppercase letter",
                category="Information",
            )
        else:
            # If the details are valid then create the users account and log them in
            new_user = User(
                username=username,
                password=generate_password_hash(password, method="sha256"),
            )
            appDB.session.add(new_user)
            appDB.session.commit()
            login_user(new_user, remember=True)
            current_app.logger.info("Signup successful")
            # Notify the user and redirect them to the view assets page
            flash("Account created successfully", category="Success")
            return redirect(url_for("views.viewAssets"))
        # endif

    # Render the sign up template with no parameters
    return render_template("signup.html")
