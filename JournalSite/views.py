import datetime

from flask import render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from JournalSite import app, login_manager, db
from JournalSite.models import Database, Entry, User

_ = Database()


@login_manager.user_loader
def load_user(user_id: int):
    return _.read(User, user_id)


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
    return render_template("index.html", entries=_.search(Entry,
                                                          filter_="entries.user=%s" % current_user.id) if not current_user.is_anonymous else [])


@app.route("/entry_add")
@login_required
def entry_add():
    new_entry = Entry(content="", date_created=datetime.datetime.now(), user=current_user.id)
    _.create(new_entry)

    return redirect(url_for("editor", id_=new_entry.id))


@app.route("/entry")
@login_required
def entry():
    entry_: Entry = _.read(Entry, request.args.get("id_"))

    return render_template("entry.html", entry=entry_)


@app.route("/editor", methods=["POST", "GET"])
@login_required
def editor():
    entry_: Entry = _.read(Entry, request.args.get("id_"))

    if request.method == "POST":
        entry_.content = request.form["content"]
        db.session.commit()

        return redirect(url_for("entry", id_=entry_.id))

    return render_template("editor.html", entry=entry_)


@app.route("/entry_delete")
@login_required
def entry_delete():
    entry_: Entry = _.read(Entry, request.args.get("id_"))
    _.delete(entry_)

    return redirect(request.referrer)
