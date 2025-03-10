from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from os import path
import os

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO(app, cors_allowed_origins="*")

DB_NAME = "database.db"

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(path.dirname(__file__), DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['SECRET_KEY'] = os.urandom(30).hex()
    app.config['DEBUG'] = True
    

    
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    login_manager.login_view = 'auth.sign'

    from .models import User
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()  

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth
    from .chat import chat

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(chat, url_prefix='/')

    with app.app_context():
        create_database(app)
        
    return app

def add_data_in_db():
    return 0

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        add_data_in_db()

