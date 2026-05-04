from flask import Flask, render_template, request, redirect, url_for, session
import re
from database import get_db, init_db, seed_db, get_user_by_email, create_user
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        errors = []

        # Validate name
        if not name or len(name) < 2:
            errors.append("Name is required and must be at least 2 characters")
        elif len(name) > 100:
            errors.append("Name must be less than 100 characters")
        elif not re.match(r"^[a-zA-Z\s'-]{2,100}$", name):
            errors.append("Name can only contain letters, spaces, hyphens, and apostrophes")

        # Validate email
        if not email:
            errors.append("Email is required")
        elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            errors.append("Please enter a valid email address")
        else:
            # Check if email already exists
            existing_user = get_user_by_email(email)
            if existing_user:
                errors.append("This email is already registered")

        # Validate password
        if not password:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters")
        elif len(password) > 128:
            errors.append("Password must be less than 128 characters")

        # If there are errors, render the form with error messages
        if errors:
            return render_template("register.html", error=errors[0], name=name, email=email)

        # Create the user
        try:
            user_id = create_user(name, email, password)
            if user_id:
                # Create session for the new user
                session["user_id"] = user_id
                session["user_name"] = name
                session["user_email"] = email
                return redirect(url_for("profile"))
            else:
                return render_template("register.html", error="An error occurred during registration. Please try again.", name=name, email=email)
        except Exception as e:
            return render_template("register.html", error="Database error. Please try again later.", name=name, email=email)

    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
