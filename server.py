from flask import Flask, flash, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, validators
from wtforms.validators import DataRequired
import main
from functools import wraps


app = Flask(__name__)
app.config["SECRET_KEY"] = "abcdefg"
authorized = False
user = None


# we need to create a form class
class NamerForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Submit")
    password = PasswordField("Password", [
        validators.DataRequired()])


class BookReviewForm(FlaskForm):
    id = StringField("id")
    book_id = StringField("book_id")
    reviewer_name = StringField("reviewer_name")
    content = StringField("content")
    rating = StringField("rating")
    published_date = DateField("published_date")
    submit = SubmitField("Create")


class BookEntryForm(FlaskForm):
    title = StringField("title")
    author = StringField("author")
    publish_date = DateField("publish_date")
    isbn = StringField("isbn")
    submit = SubmitField("create")


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
                    request.form['password'] == main.check_user(request.form["username"])[3]:
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


@app.route("/content_management", )
# @login_required
def content_management():
    review_form = BookReviewForm()
    book_creation_form = BookEntryForm()

    return render_template("content_management.html", review_form=review_form, book_creation_form=book_creation_form)


@app.route("/bookcreation", methods=["POST"])
def bookcreation():
    review_form = BookReviewForm()
    book_creation_form = BookEntryForm()

    if book_creation_form.is_submitted():
        if book_creation_form.is_submitted():
            book_creation_info = [book_creation_form.title.data,
                                  book_creation_form.author.data,
                                  book_creation_form.publish_date.data,
                                  book_creation_form.isbn.data]
            book_creation_form.title.data, \
            book_creation_form.author.data, \
            book_creation_form.publish_date.data, \
            book_creation_form.isbn.data = "", "", "", ""
            print(book_creation_info)
    return render_template("content_management.html", review_form=review_form, book_creation_form=book_creation_form)


@app.route("/review_creation", methods=["POST"])
def review_creation():
    review_form = BookReviewForm()
    book_creation_form = BookEntryForm()

    if review_form.is_submitted():
        if review_form.is_submitted():
            review_info = [review_form.id.data,
                           review_form.book_id.data,
                           review_form.reviewer_name.data,
                           review_form.content.data,
                           review_form.rating.data,
                           review_form.published_date.data
                           ]
            review_form.id.data, \
            review_form.book_id.data, \
            review_form.reviewer_name.data, \
            review_form.content.data, \
            review_form.rating.data, \
            review_form.published_date.data = "", "", "", "", "", ""
            main.create_book_review(review_info[2], review_info[3], review_info[4], review_info[5])

    return render_template("content_management.html", review_form=review_form, book_creation_form=book_creation_form)


@app.route("/user_management", methods=['GET', 'POST'])
# @login_required
def user_management():
    user = None
    form = NamerForm(request.form)
    if request.method == "POST" and form.submit():
        new_user = [form.username.data, form.password.data]
        main.create_user(new_user[0], new_user[1])
        user = new_user[0].capitalize()
        form.username.data = ""
        form.password.data = ""
        flash(f"{user} added to database!")
    return render_template("user_management.html",
                           form=form, user=user)


@app.route("/forms")
def index():
    userform = NamerForm()
    bookform = BookEntryForm()
    return render_template("formtest.html", userform=userform, bookform=bookform)


@app.route("/name", methods=["GET", "POST"])
# @login_required
def name():
    name = None
    form = NamerForm()
    if form.is_submitted():
        name = form.username.data
        form.username.data = ""
    return render_template("name.html", name=name, form=form)


if __name__ == "__main__":
    app.run(debug=True)
