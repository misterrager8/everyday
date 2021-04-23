import os

import markdown
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def markdown_to_html(filename: str):
    _ = os.path.join(os.path.dirname(__file__), "./docs/%s" % filename)
    with open(_, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    return html


def markdown_to_text(filename: str):
    _ = os.path.join(os.path.dirname(__file__), "./docs/%s" % filename)
    with open(_, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    return text


@app.route("/")
def index():
    files = []
    for i in os.listdir("docs/"): files.append(i.split(".md")[0])
    return render_template("index.html", files=files)


@app.route("/note")
def note_pg():
    filename = request.args.get("filename")

    return render_template("note.html", content=markdown_to_html(filename), title=filename.split(".md")[0])


@app.route("/raw_note")
def raw_note_pg():
    filename = request.args.get("filename")

    return render_template("note_raw.html", content=markdown_to_text(filename), title=filename.split(".md")[0])


@app.route("/add_note", methods=["POST", "GET"])
def add_note():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        with open("./docs/%s.md" % title, "w") as f:
            f.write(content)

        return redirect(url_for("index"))

    return render_template("add_note.html")


@app.route("/edit_note", methods=["POST", "GET"])
def edit_note():
    filename = request.args.get("filename")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        with open("./docs/%s.md" % title, "w") as f:
            f.write(content)

        return redirect(url_for("index"))

    return render_template("edit_note.html", content=markdown_to_text(filename), title=filename.split(".md")[0])


@app.route("/delete_note")
def delete_note():
    filename = request.args.get("filename")
    os.remove("./docs/%s.md" % filename)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
