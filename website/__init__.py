from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
engine = create_engine('sqlite:///D:/pythonProject1/Flask trading app/instance/database.db')
Session = sessionmaker(bind=engine)
session = Session()

db = SQLAlchemy()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 's,,c3,c;g2qks0'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .crypto import crypto
    from .portfolio import portofilo_blueprint
    from .trade import trade_blueprint

    app.register_blueprint(views,url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/')
    app.register_blueprint(crypto,url_prefix = '/')
    app.register_blueprint(portofilo_blueprint,url_prefix = '/')
    app.register_blueprint(trade_blueprint,url_prefix = '/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return session.query(User).get(int(id))
    return app
def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')