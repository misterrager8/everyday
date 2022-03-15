import datetime

from flask import Blueprint, request, render_template, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from JournalSite.ctrla import Database
from JournalSite.models import Entry

entries = Blueprint("entries", __name__)
database = Database()


@entries.route("/entries_")
def entries_():
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("entries.html", order_by=order_by)


@entries.route("/create_entry")
def create_entry():
    _ = Entry(content="",
              date_created=datetime.datetime.now(),
              user=current_user.id,
              book=request.args.get("book") or None)
    database.create(_)

    return redirect(url_for("entries.edit_entry", id_=_.id))


@entries.route("/edit_entry", methods=["POST", "GET"])
def edit_entry():
    if request.method == "POST":
        entry_: Entry = database.get(Entry, int(request.form["id_"]))
        entry_.content = request.form["content"]
        entry_.book = request.form["book"] or None
        database.update()

        return redirect(request.referrer)
    else:
        entry_: Entry = database.get(Entry, int(request.args.get("id_")))

        return render_template("entry.html", entry_=entry_)


@entries.route("/delete_entry")
def delete_entry():
    entry_: Entry = database.get(Entry, int(request.args.get("id_")))
    database.delete(entry_)

    return redirect(request.referrer)
