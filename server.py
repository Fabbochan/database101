from flask import Flask, flash, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, validators
from wtforms.validators import DataRequired
import main
from functools import wraps
import webscraper


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


class TwitterUserSearchForm(FlaskForm):
    username = StringField("username")


class TwitterStringSearchForm(FlaskForm):
    search_string = StringField("Search_text")
    startdate = DateField("startdate")
    enddate = DateField("enddate")


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
                print(f"login successfull as {user[1]}, id: {user[0]}")
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
@login_required
def content_management():
    global user

    return render_template("content_management.html")


@app.route("/webparser", methods=["GET", "POST"])
@login_required
def webparser_content():
    global user
    print(user)
    twitter_user = None
    tweet_form = TwitterUserSearchForm()
    if request.method == "POST" and tweet_form.is_submitted():
        twitter_user = tweet_form.username.data
        tweet_form.username.data = ""
        print(twitter_user)

    tweet_info = webscraper.get_tweets_from_user(twitter_user)

    return render_template("webparser.html",
                           twitter_user=twitter_user,
                           tweet_form=tweet_form,
                           tweet_info=tweet_info)


@app.route("/book_creation")
@login_required
def book_creation():
    global user
    review_form = BookReviewForm()
    book_creation_form = BookEntryForm()
    print("access", user[1])
    return render_template("book_creation.html", review_form=review_form, book_creation_form=book_creation_form)


@app.route("/bookcreation", methods=["POST"])
@login_required
def bookcreation():
    global user
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
    return render_template("book_creation.html", review_form=review_form, book_creation_form=book_creation_form)


@app.route("/review_creation", methods=["POST"])
@login_required
def review_creation():
    global user
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

    return render_template("book_creation.html", review_form=review_form, book_creation_form=book_creation_form)


@app.route("/user_management", methods=['GET', 'POST'])
@login_required
def user_management():
    global user
    form = NamerForm(request.form)
    user_info = main.check_user_info(user)
    if request.method == "POST" and form.submit():
        new_user = [form.username.data, form.password.data]
        main.create_user(new_user[0], new_user[1])
        user = new_user[0].capitalize()
        form.username.data = ""
        form.password.data = ""
        flash(f"{user} added to database!")
    print("access", user[1])
    return render_template("user_management.html",
                           form=form, user=user, user_info=user_info)

@login_required
@app.route("/login_information", methods=["GET"])
def login_information():
    global user
    user_info = main.check_user_info(user)
    print("access", user[1])
    return render_template("login_information.html", user=user, user_info=user_info)


@app.route("/forms")
@login_required
def index():
    userform = NamerForm()
    bookform = BookEntryForm()
    return render_template("formtest.html", userform=userform, bookform=bookform)


@app.route("/name", methods=["GET", "POST"])
@login_required
def name():
    name = None
    form = NamerForm()
    if form.is_submitted():
        name = form.username.data
        form.username.data = ""
    return render_template("name.html", name=name, form=form)


if __name__ == "__main__":
    app.run(debug=True)
