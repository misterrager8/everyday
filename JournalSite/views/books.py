import datetime
import random

from flask import Blueprint, request, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from JournalSite.ctrla import Database
from JournalSite.models import Book

books = Blueprint("books", __name__)
database = Database()


@books.route("/create_book", methods=["POST"])
def create_book():
    _ = Book(name=request.form["name"],
             date_created=datetime.datetime.now(),
             color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
             user=current_user.id)
    database.create(_)

    return redirect(request.referrer)


@books.route("/books_")
def books_():
    return render_template("books.html")


@books.route("/book")
def book():
    book_: Book = database.get(Book, int(request.args.get("id_")))

    return render_template("book.html", book_=book_)


@books.route("/edit_book", methods=["POST"])
def edit_book():
    book_: Book = database.get(Book, int(request.form["id_"]))
    book_.name = request.form["name"]
    database.update()

    return redirect(request.referrer)


@books.route("/delete_book")
def delete_book():
    book_: Book = database.get(Book, int(request.args.get("id_")))
    database.delete_multiple([i for i in book_.entries])
    database.delete(book_)

    return redirect(request.referrer)
