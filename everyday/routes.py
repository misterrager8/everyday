from flask import current_app, send_from_directory, request

from everyday.models import Entry, Journal


@current_app.route("/")
def index():
    return send_from_directory(current_app.static_folder, "index.html")


@current_app.post("/test_route")
def test_route():
    success = True
    msg = ""

    try:
        pass
    except Exception as e:
        success = False
        msg = str(e)

    return {"success": success, "msg": msg}


@current_app.post("/get_journals")
def get_journals():
    success = True
    msg = ""
    journals_ = []

    try:
        journals_ = [i.todict() for i in Journal.all()]
    except Exception as e:
        success = False
        msg = str(e)

    return {"success": success, "msg": msg, "journals": journals_}


@current_app.post("/get_journal")
def get_journal():
    success = True
    msg = ""
    days_ = []

    try:
        journal_ = Journal(request.json.get("name"))
        days_ = journal_.get_calendar(
            int(request.json.get("month")), int(request.json.get("year"))
        )
    except Exception as e:
        success = False
        msg = str(e)

    return {"success": success, "msg": msg, "days": days_}


@current_app.post("/rename_journal")
def rename_journal():
    success = True
    msg = ""
    journals_ = []
    journal_ = None

    try:
        journal_ = Journal.rename(request.json.get("name"), request.json.get("newName"))

        journal_ = Journal(request.json.get("newName")).todict()
        journals_ = [i.todict() for i in Journal.all()]
    except Exception as e:
        success = False
        msg = str(e)

    return {
        "success": success,
        "msg": msg,
        "journal": journal_,
        "journals": journals_,
    }


@current_app.post("/add_entry")
def add_entry():
    success = True
    msg = ""
    journals_ = []
    journal_ = None

    try:
        journal_ = Journal(request.json.get("name"))
        journal_.add_entry()
        journal_ = journal_.todict()

        journals_ = [i.todict() for i in Journal.all()]
    except Exception as e:
        success = False
        msg = str(e)

    return {
        "success": success,
        "msg": msg,
        "journal": journal_,
        "journals": journals_,
    }


@current_app.post("/add_journal")
def add_journal():
    success = True
    msg = ""
    journals_ = []
    journal_ = None

    try:
        journal_ = Journal(request.json.get("name"))
        journal_.add()
        journal_ = journal_.todict()

        journals_ = [i.todict() for i in Journal.all()]
    except Exception as e:
        success = False
        msg = str(e)

    return {
        "success": success,
        "msg": msg,
        "journal": journal_,
        "journals": journals_,
    }


@current_app.post("/delete_entry")
def delete_entry():
    success = True
    msg = ""
    journals_ = []
    journal_ = None

    try:
        journal_ = Journal(request.json.get("journalName"))

        entry_ = Entry(request.json.get("path"))
        entry_.delete()

        journals_ = [i.todict() for i in Journal.all()]
        journal_ = journal_.todict()
    except Exception as e:
        success = False
        msg = str(e)

    return {
        "success": success,
        "msg": msg,
        "journals": journals_,
        "journal": journal_,
    }


@current_app.post("/delete_journal")
def delete_journal():
    success = True
    msg = ""
    journals_ = []
    journal_ = None

    try:
        journal_ = Journal(request.json.get("name"))
        journal_.delete()

        journals_ = [i.todict() for i in Journal.all()]
    except Exception as e:
        success = False
        msg = str(e)

    return {
        "success": success,
        "msg": msg,
        "journals": journals_,
    }


@current_app.post("/edit_entry")
def edit_entry():
    success = True
    msg = ""

    try:
        entry_ = Entry(request.json.get("path"))
        entry_.edit(request.json.get("content"))
    except Exception as e:
        success = False
        msg = str(e)

    return {
        "success": success,
        "msg": msg,
    }
