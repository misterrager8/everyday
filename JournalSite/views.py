import datetime
import random

from flask import render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from JournalSite import app, login_manager, db
from JournalSite.models import Database, Entry, User

database = Database()


@login_manager.user_loader
def load_user(user_id: int):
    return database.get(User, user_id)


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]

        user_: User = User.query.filter_by(username=username).first()
        if user_ and check_password_hash(generate_password_hash(user_.password), password):
            login_user(user_)
            return redirect(url_for("index"))
        else:
            return "Login failed."


@app.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/entry_create", methods=["POST"])
@login_required
def entry_create():
    new_entry = Entry(content=request.form["content"].capitalize(),
                      date_created=datetime.datetime.now(),
                      user=current_user.id,
                      color="#{:06x}".format(random.randint(0, 0xFFFFFF)))
    database.create(new_entry)

    return redirect(request.referrer)


@app.route("/entry_update", methods=["POST"])
@login_required
def entry_update():
    entry_: Entry = database.get(Entry, int(request.form["id_"]))
    entry_.content = request.form["content"]
    db.session.commit()

    return redirect(request.referrer)


@app.route("/entry_delete")
@login_required
def entry_delete():
    entry_: Entry = database.get(Entry, request.args.get("id_"))
    database.delete(entry_)

    return redirect(request.referrer)
