import pymysql
from flask import Flask
from flask_login import LoginManager
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    Scss(app, asset_dir="JournalSite/static")

    with app.app_context():
        from JournalSite.views.books import books
        from JournalSite.views.entries import entries

        app.register_blueprint(entries)
        app.register_blueprint(books)

        db.create_all()

        return app
