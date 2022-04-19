import datetime

from flask import render_template, current_app, request, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from moodJournal import login_manager
from moodJournal.ctrla import Database
from moodJournal.models import User, Entry

database = Database()


@login_manager.user_loader
def load_user(id_: int):
    return User.query.get(id_)


@current_app.route("/")
def index():
    return render_template("index.html")


@current_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@current_app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user_: User = User.query.filter(username == username).first()
    if user_ and check_password_hash(user_.password, password):
        login_user(user_)
        return redirect(url_for("index"))
    else:
        return "Failed."


@current_app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    user_ = User(username=username, password=generate_password_hash(password), date_created=datetime.datetime.now())
    database.add(user_)
    login_user(user_)

    return redirect(url_for("index"))


@current_app.route("/entry_add", methods=["POST"])
def entry_add():
    entry_ = Entry(mood=request.form["mood"],
                   content=request.form["content"],
                   date_created=datetime.datetime.now(),
                   user=current_user.id)

    database.add(entry_)
    return redirect(request.referrer)


@current_app.route("/entry_edit", methods=["POST"])
def entry_edit():
    entry_: Entry = database.get(Entry, int(request.form["id_"]))
    entry_.mood = request.form["mood"]
    entry_.content = request.form["content"]
    database.update()
    return redirect(request.referrer)


@current_app.route("/entry_delete")
def entry_delete():
    entry_: Entry = database.get(Entry, int(request.args.get("id_")))
    database.delete(entry_)
    return redirect(request.referrer)
