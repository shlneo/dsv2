from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12341234@localhost/sampledsdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['SECRET_KEY'] = 'your_secret_key' 

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User
    with app.app_context():
        db.create_all()  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
