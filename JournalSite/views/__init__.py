import datetime

from flask import render_template, request, url_for, current_app
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from JournalSite import login_manager
from JournalSite.ctrla import Database
from JournalSite.models import User

database = Database()


@login_manager.user_loader
def load_user(user_id: int):
    return database.get(User, user_id)


@current_app.route("/login", methods=["POST"])
def login():
    user_: User = User.query.filter_by(username=request.form["username"]).first()
    if user_ and check_password_hash(user_.password, request.form["password"]):
        login_user(user_)
        return redirect(url_for("index"))
    else:
        return "Login failed."


@current_app.route("/signup", methods=["POST"])
def signup():
    _ = User(username=request.form["username"],
             password=generate_password_hash(request.form["password"]),
             date_created=datetime.datetime.now())
    database.create(_)
    login_user(_)
    return redirect(url_for("index"))


@current_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@current_app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")
    filter_ = request.args.get("filter_", default="")
    return render_template("index.html", order_by=order_by, filter_=filter_)
