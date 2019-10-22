from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from myblog.config import Configuration


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from myblog.post.post import posts
    from myblog.auth.auth import auth

    app.register_blueprint(posts)
    app.register_blueprint(auth)

    return app
