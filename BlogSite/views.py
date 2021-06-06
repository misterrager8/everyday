from flask import render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

from BlogSite import app, db, login_manager
from BlogSite.models import User, Post


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html", current_user=current_user)


@app.route("/login", methods=["POST", "GET"])
def user_login():
    if request.method == "POST":
        username = request.form["username"]
        passwd = request.form["passwd"]

        user_: User = User.query.filter_by(username=username).first()
        if user_ and check_password_hash(generate_password_hash(user_.password), passwd):
            login_user(user_)
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/account")
def account():
    return render_template("account.html")


@app.route("/profile")
def profile():
    id_: int = request.args.get("id_")
    return render_template("profile.html", person=db.session.query(User).get(id_))


@app.route("/people")
def people():
    return render_template("people.html", ppl=db.session.query(User).all())


@app.route("/favorites")
def favorites():
    return render_template("favorites.html")


@app.route("/posts")
def posts():
    order_by: str = request.args.get("order_by", default="posts.date_created desc")
    return render_template("posts.html", posts_=db.session
                           .query(Post)
                           .join(User)
                           .order_by(text(order_by))
                           .all(), order_by=order_by)


@app.route("/post")
def post():
    id_: int = request.args.get("id_")
    return render_template("post.html", post_=db.session.query(Post).get(id_))


@app.route("/logout")
def user_logout():
    logout_user()
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        _ = User(username=request.form["username"], password=request.form["passwd"])
        db.session.add(_)
        db.session.commit()

        login_user(_)
        return redirect(url_for("index"))

    return render_template("signup.html")


@app.route("/editor", methods=["POST", "GET"])
@login_required
def editor():
    if request.method == "POST":
        _ = Post(request.form["title"], request.form["content"], True)
        current_user.posts.append(_)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("editor.html")
