from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
import main
from functools import wraps


app = Flask(__name__)
app.config["SECRET_KEY"] = "abcdefg"
authorized = False
user = None


# we need to create a form class
class NamerForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Submit")
    password = PasswordField("Password", validators=[DataRequired()])


class BookReviewForm(FlaskForm):
    id = StringField("id")
    book_id = StringField("book_id")
    reviewer_name = StringField("reviewer_name")
    content = StringField("content")
    rating = StringField("rating")
    published_date = StringField("published_date")
    submit = SubmitField("Create")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not authorized:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
# @login_required
def home():
    book_info = main.pick_book()
    user_info = main.fetch_all_user()
    review_info = main.fetch_all_reviews()
    return render_template("home.html",
                           user=user,
                           book_info=book_info,
                           user_info=user_info,
                           review_info=review_info)


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


@app.route("/content_management", methods=['GET', 'POST'])
# @login_required
def content_management():
    form = BookReviewForm()
    if form.is_submitted():
        review_info = [form.id.data,
                       form.book_id.data,
                       form.reviewer_name.data,
                       form.content.data,
                       form.rating.data,
                       form.published_date.data
                       ]
        form.id.data, \
        form.book_id.data, \
        form.reviewer_name.data, \
        form.content.data, \
        form.rating.data, \
        form.published_date.data = "", "", "", "", "", ""
        main.create_book_review(review_info[2],review_info[3],review_info[4], review_info[5])
    return render_template("content_management.html", form=form)


@app.route("/user_management", methods=['GET', 'POST'])
# @login_required
def user_management():
    form = NamerForm()
    message = None
    user = None
    if form.is_submitted():
        main.create_user(form.name.data)
        user = form.name.data.capitalize()
        form.name.data = ""
        message = " added to database!"
    return render_template("user_management.html",
                           form=form,
                           message=message, user=user)


@app.route("/name", methods=["GET", "POST"])
# @login_required
def name():
    name = None
    form = NamerForm()
    if form.is_submitted():
        name = form.name.data
        form.name.data = ""
    return render_template("name.html", name=name, form=form)


if __name__ == "__main__":
    app.run(debug=True)
