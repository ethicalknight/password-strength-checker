from flask import Flask, render_template, request

import re

app = Flask(__name__)

def check_password_strength(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ !@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password) is None

    errors = {
        "length": not length_error,
        "digit": not digit_error,
        "uppercase": not uppercase_error,
        "lowercase": not lowercase_error,
        "symbol": not symbol_error
    }

    strength = "Weak"
    if all(errors.values()):
        strength = "Strong"
    elif sum(errors.values()) >= 3:
        strength = "Moderate"

    return strength, errors

@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    strength = ""
    errors = {}

    if request.method == "POST":
        password = request.form["password"]
        strength, errors = check_password_strength(password)

    return render_template("index.html", password=password, strength=strength, errors=errors)

if __name__ == "__main__":
    app.run(debug=True)
