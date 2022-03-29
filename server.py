from flask import Flask, render_template, request, redirect, url_for
import main
from functools import wraps


app = Flask(__name__)
authorized = False
user = None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not authorized:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@login_required
def home():
    return render_template("home.html", user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global authorized
    global user
    error = None
    if request.method == 'POST':
        try:
            if request.form['username'] == main.check_user(request.form["username"])[1] and \
                    request.form['password'] == 'admin':
                user = main.login_user(request.form["username"])
                authorized = True
                print("login successfull")
                return redirect(url_for("home", user=user))
        except TypeError:
            error = 'Invalid Credentials! Please try again.'
    return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    global authorized
    global user
    authorized = False
    user = None
    return redirect(url_for("login"))


@app.route("/user_management", methods=['GET', 'POST'])
@login_required
def user_management():
    all_user = main.fetch_all_user()
    if request.method == "POST":
        try:
            main.create_user(username=request.form["username"])
            return render_template("user_management.html", all_user=all_user)
        except TypeError as input_error:
            print(input_error)
    return render_template("user_management.html", all_user=all_user)


if __name__ == "__main__":
    app.run(debug=True)
